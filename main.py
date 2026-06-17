from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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

@app.get("/livros")
def get_livros(page: int = 1, limit: int = 10, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou Limit inválidos!!")    
    
    livros = db.query(LivroDB).offset((page - 1) * limit).limit(limit).all()
    
    if not livros:
        return {"message": "Não existe nenhum livro!"}
    total_livros = db.query(LivroDB).count()
    return {
        "Page": page,
        "Limit": limit,
        "Total": total_livros,
        "Livros": [{'id': livro.id, 'nome_livro': livro.nome_livro, 'autor': livro.autor, 'ano': livro.ano} for livro in livros]
    }
    
@app.post("/adicionar")
def post_livros(livro: Livro, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.nome_livro == livro.nome_livro, LivroDB.autor == livro.autor).first()
    if db_livro:
        raise HTTPException(status_code=400, detail="Esse livro já existe!")
    novo_livro = LivroDB(nome_livro=livro.nome_livro, autor=livro.autor, ano=livro.ano)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return {"message": "o Livro foi criado com sucesso!"}
    
@app.put("/atualizar/{id_livro}")
def put_livros(id_livro: int, livro: Livro, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
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
def delete_livro(id_livro: int, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Esse livro não existe!")
    db.delete(db_livro)
    db.commit()

    return {"message": "O livro foi excluido com sucesso!"}