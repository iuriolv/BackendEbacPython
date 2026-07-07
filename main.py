from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
import secrets
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import asyncio
import redis
import json

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

app = FastAPI(
    title="Catálago de Livros",
    description="API para gerenciar catálago de livros.",
    version="1.0.0",
    contact={
        "name": "Iuri Oliveira",
        "email": "euree.olv@gmail.com"
    }
)

MEU_USUARIO = os.getenv('MEU_USUARIO')
MINHA_SENHA = os.getenv('MINHA_SENHA')

security = HTTPBasic()

class LivroDB(Base):
    __tablename__ = "biblioteca"
    id = Column(Integer, primary_key=True, index=True)
    nome_livro = Column(String, index=True)
    autor = Column(String, index=True)
    ano = Column(Integer)

class Livro(BaseModel):
    nome_livro: str
    autor: str
    ano: int

Base.metadata.create_all(bind=engine)

def salvar_livro_no_cache(livro_id: int, livro: Livro):
    redis_client.set(f"livro:{livro_id}", json.dumps(livro.dict()))

def deletar_livro_do_cache(livro_id: int):
    redis_client.delete(f"livro:{livro_id}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"}
        )

@app.get("/debug/redis")
async def ver_livros_cache():
    chaves = redis_client.keys("livro:*")
    livros_cache = []
    for chave in chaves:
        valor = redis_client.get(chave)
        ttl = redis_client.ttl(chave)
        livros_cache.append({"chave": chave, "valor": json.loads(valor), "ttl": ttl})
    return livros_cache

@app.get("/livros")
async def get_livros(page: int = 1, limit: int = 10, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou Limit inválidos!!")

    cache_key = f"livros:page:{page}:limit:{limit}"
    cached_livros = redis_client.get(cache_key)

    if cached_livros:
        return json.loads(cached_livros)   
    
    livros = db.query(LivroDB).offset((page - 1) * limit).limit(limit).all()
    
    if not livros:
        return {"message": "Não existe nenhum livro!"}
    total_livros = db.query(LivroDB).count()
    reposta =  {
        "Page": page,
        "Limit": limit,
        "Total": total_livros,
        "Livros": [{'id': livro.id, 'nome_livro': livro.nome_livro, 'autor': livro.autor, 'ano': livro.ano} for livro in livros]
    }

    redis_client.setex(cache_key, 30, json.dumps(reposta))

    return reposta
    
@app.post("/adicionar")
async def post_livros(livro: Livro, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.nome_livro == livro.nome_livro, LivroDB.autor == livro.autor).first()
    if db_livro:
        raise HTTPException(status_code=400, detail="Esse livro já existe!")
    novo_livro = LivroDB(nome_livro=livro.nome_livro, autor=livro.autor, ano=livro.ano)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    salvar_livro_no_cache(novo_livro.id, livro)

    return {"message": "O livro foi criado com sucesso!"}
    
@app.put("/atualizar/{id_livro}")
async def put_livros(id_livro: int, livro: Livro, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado!")
    db_livro.nome_livro = livro.nome_livro
    db_livro.autor = livro.autor
    db_livro.ano = livro.ano
    db.commit()
    db.refresh(db_livro)

    return {"message": "As infromações foram atualizaas com sucesso!"}
    
@app.delete("/deletar/{id_livro}")
async def delete_livro(id_livro: int, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Esse livro não existe!")
    db.delete(db_livro)
    db.commit()

    deletar_livro_do_cache(id_livro)

    return {"message": "O livro foi excluido com sucesso!"}