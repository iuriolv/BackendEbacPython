from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

biblioteca = {}

class Livro(BaseModel):
    nome_livro: str
    autor: str
    ano: int

@app.get("/")
def hello_world():
    return {"Hello": "World!"}

@app.get("/livros")
def get_livros():
    if not biblioteca:
        return {"message": "Não existe nenhum livro!"}
    else:
        return {"livros": biblioteca}
    
@app.post("/adicionar")
def post_livros(id_livro: int, livro: Livro):
    if id_livro in biblioteca:
        raise HTTPException(status_code=400, detail="Esse livro já existe!")
    else:
        biblioteca[id_livro] = livro.dict()
        return {"message": "o Livro foi criado com sucesso!"}
    
@app.put("/atualizar/{id_livro}")
def put_livros(id_livro: int, livro: Livro):
    novo_livro = biblioteca.get(id_livro)
    if not novo_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado!")
    else:
        novo_livro[id_livro] = livro.dict()

        return {"message": "As infromações foram atualizaas com sucesso!"}
    
@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int):
    if id_livro not in biblioteca:
        raise HTTPException(status_code=404, detail="Esse livro não existe!")
    else:
        del biblioteca[id_livro]

        return {"message": "O livro foi excluido com sucesso!"}