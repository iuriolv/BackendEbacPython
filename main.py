from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os

app = FastAPI(
    title="Catálago de Livros",
    description="API para gerenciar catálago de livros.",
    version="1.0.0",
    contact={
        "name": "Iuri Oliveira",
        "email": "euree.olv@gmail.com"
    }
)

MEU_USUARIO = 'admin'
MINHA_SENHA = 'admin'

security = HTTPBasic()

biblioteca = {}

class Livro(BaseModel):
    nome_livro: str
    autor: str
    ano: int

def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW.Authenticate": "Basic"}
        )

@app.get("/")
def hello_world():
    return {"Hello": "World!"}

@app.get("/livros")
def get_livros(credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if not biblioteca:
        return {"message": "Não existe nenhum livro!"}
    else:
        return {"livros": biblioteca}
    
@app.post("/adicionar/{id_livro}")
def post_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id_livro in biblioteca:
        raise HTTPException(status_code=400, detail="Esse livro já existe!")
    else:
        biblioteca[id_livro] = livro.dict()
        return {"message": "o Livro foi criado com sucesso!"}
    
@app.put("/atualizar/{id_livro}")
def put_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    novo_livro = biblioteca.get(id_livro)
    if not novo_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado!")
    else:
        biblioteca[id_livro] = livro.dict()

        return {"message": "As infromações foram atualizaas com sucesso!"}
    
@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id_livro not in biblioteca:
        raise HTTPException(status_code=404, detail="Esse livro não existe!")
    else:
        del biblioteca[id_livro]

        return {"message": "O livro foi excluido com sucesso!"}