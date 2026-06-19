# 📚 Catálogo de Livros API

API REST desenvolvida com **FastAPI**, **SQLAlchemy** e **SQLite** para gerenciamento de um catálogo de livros.

## 🚀 Funcionalidades

* Listar livros cadastrados com paginação.
* Adicionar novos livros.
* Atualizar informações de livros existentes.
* Excluir livros do catálogo.
* Autenticação utilizando HTTP Basic Authentication.
* Persistência de dados com SQLite.

---

## 🛠 Tecnologias Utilizadas

* Python 3.11+
* FastAPI
* SQLAlchemy
* SQLite
* Docker
* Docker Compose

---

## 📂 Estrutura do Projeto

```text
BackendEbacPython/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

## ⚙️ Pré-requisitos

Antes de iniciar, instale:

* Docker
* Docker Compose
* Git

Verifique as instalações:

```bash
docker --version
docker-compose --version
git --version
```

---

## 📥 Clonando o Repositório

Clone o projeto:

```bash
git clone https://github.com/iuriolv/BackendEbacPython.git
```

Entre na pasta do projeto:

```bash
cd BackendEbacPython
```

---

## 🔐 Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto contendo:

```env
DATABASE_URL=sqlite:///./livros.db
MEU_USUARIO=admin
MINHA_SENHA=123456
```

Você pode alterar os valores conforme necessário.

---

## 🐳 Executando com Docker Compose

### Construir e iniciar os contêineres

Execute o comando abaixo para construir as imagens e iniciar a aplicação em segundo plano:

```bash
docker-compose up --build -d
```

O parâmetro:

* `--build` força a reconstrução da imagem.
* `-d` executa os contêineres em background.

---

### Verificar os contêineres em execução

```bash
docker ps
```

---

### Visualizar logs da aplicação

```bash
docker-compose logs -f
```

---

## 🌐 Acessando a Aplicação

Após iniciar os contêineres, a API estará disponível em:

```text
http://localhost:8000
```

### Documentação Swagger

```text
http://localhost:8000/docs
```

### Documentação ReDoc

```text
http://localhost:8000/redoc
```

---

## 🔑 Autenticação

Todos os endpoints utilizam **HTTP Basic Authentication**.

Exemplo usando cURL:

```bash
curl -u admin:123456 http://localhost:8000/livros
```

---

## 📚 Endpoints Disponíveis

### Listar livros

```http
GET /livros?page=1&limit=10
```

### Adicionar livro

```http
POST /adicionar
```

Exemplo de payload:

```json
{
  "nome_livro": "Dom Casmurro",
  "autor": "Machado de Assis",
  "ano": 1899
}
```

### Atualizar livro

```http
PUT /atualizar/{id_livro}
```

### Excluir livro

```http
DELETE /deletar/{id_livro}
```

---

## 🛑 Parando a Aplicação

Para interromper e remover os contêineres:

```bash
docker-compose down
```

Para remover também os volumes associados:

```bash
docker-compose down -v
```

---

## 👨‍💻 Autor

**Iuri Oliveira**

* GitHub: https://github.com/iuriolv
* E-mail: [euree.olv@gmail.com](mailto:euree.olv@gmail.com)
