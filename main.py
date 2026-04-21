from fastapi import FastAPI, HTTPException

app = FastAPI()

biblioteca = {}

@app.get("/")
def hello_world():
    return {"Hello": "World!"}

@app.get("/livros")
def get_livros():
    if not biblioteca:
        return {"message": "Não existe nenhum livro!"}
    else:
        return {"livros": biblioteca}
    
@app.post("/adiciona")
def post_livros(id_livro: int, nome_livro: str, autor: str, ano: int):
    if id_livro in biblioteca:
        raise HTTPException(status_code=400, detail="Esse livro já existe!")
    else:
        biblioteca[id_livro] = {"nome_livro": nome_livro, "autor": autor, "ano": ano}
        return {"message": "o Livro foi criado com sucesso!"}
    
@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, nome_livro: str, autor: str, ano: int):
    novo_livro = biblioteca.get(id_livro)
    if not novo_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado!")
    else:
        if nome_livro:
            novo_livro['nome_livro'] = nome_livro
        if autor:
            novo_livro['autor'] = autor
        if ano:
            novo_livro['ano'] = ano

        return {"message": "As infromações foram atualizaas com sucesso!"}
    
@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int):
    if id_livro not in biblioteca:
        raise HTTPException(status_code=404, detail="Esse livro não existe!")
    else:
        del biblioteca[id_livro]

        return {"message": "O livro foi excluido com sucesso!"}