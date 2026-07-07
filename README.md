# 📚 Catálogo de Livros API

API REST desenvolvida com **FastAPI**, **SQLAlchemy**, **SQLite** e **Redis** para gerenciamento de um catálogo de livros.

## 🚀 Funcionalidades

* Cadastro de livros.
* Listagem de livros com paginação.
* Atualização de informações dos livros.
* Exclusão de livros.
* Autenticação utilizando HTTP Basic Authentication.
* Persistência de dados com SQLite.
* Cache utilizando Redis para melhorar o desempenho das consultas.
* Endpoint para visualizar os dados armazenados no cache.

---

# 🛠 Tecnologias Utilizadas

* Python 3.14
* FastAPI
* SQLAlchemy
* SQLite
* Redis
* python-dotenv
* Docker
* Docker Compose
* Poetry

---

# 📂 Estrutura do Projeto

```text
BackendEbacPython/
│
├── main.py
├── pyproject.toml
├── poetry.lock
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

# ⚙️ Pré-requisitos

Antes de iniciar o projeto, tenha instalado:

* Python 3.14+
* Poetry
* Docker
* Docker Compose
* Redis
* Git

Verifique as instalações:

```bash
python --version
poetry --version
docker --version
docker compose version
redis-server --version
git --version
```

---

# 📥 Clonando o Repositório

```bash
git clone https://github.com/iuriolv/BackendEbacPython.git
```

Entre na pasta do projeto:

```bash
cd BackendEbacPython
```

---

# 📦 Instalando as Dependências

Caso utilize Poetry:

```bash
poetry install
```

Ative o ambiente virtual:

```bash
poetry shell
```

Ou execute diretamente:

```bash
poetry run uvicorn main:app --reload
```

---

# 🔐 Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto contendo:

```env
DATABASE_URL=sqlite:///./biblioteca.db
MEU_USUARIO=admin
MINHA_SENHA=123456
```

---

# 🔴 Redis

A aplicação utiliza o Redis para armazenar em cache:

* A listagem de livros (`GET /livros`)
* Livros cadastrados individualmente
* Remoção automática do cache ao excluir livros

Por padrão, o projeto conecta em:

```text
localhost:6379
```

Caso esteja utilizando Docker:

```bash
docker run -d --name redis -p 6379:6379 redis
```

Ou execute o servidor Redis localmente:

```bash
redis-server
```

---

# 🐳 Executando com Docker Compose

Construa e inicie os contêineres:

```bash
docker compose up --build -d
```

Verifique se estão em execução:

```bash
docker ps
```

Visualize os logs:

```bash
docker compose logs -f
```

---

# ▶️ Executando Localmente

Com o ambiente virtual ativo:

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://localhost:8000
```

---

# 📖 Documentação

Swagger:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# 🔑 Autenticação

Todos os endpoints utilizam **HTTP Basic Authentication**.

Exemplo utilizando cURL:

```bash
curl -u admin:123456 http://localhost:8000/livros
```

---

# 📚 Endpoints

## Listar livros

```http
GET /livros?page=1&limit=10
```

Retorna a lista paginada de livros.

As respostas ficam armazenadas em cache por **30 segundos**.

---

## Adicionar livro

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

Após o cadastro, o livro também é armazenado no Redis.

---

## Atualizar livro

```http
PUT /atualizar/{id_livro}
```

Atualiza as informações de um livro existente.

---

## Excluir livro

```http
DELETE /deletar/{id_livro}
```

Remove o livro do banco de dados e também do cache do Redis.

---

## Visualizar Cache

```http
GET /debug/redis
```

Endpoint utilizado para visualizar todas as chaves armazenadas no Redis, incluindo:

* chave
* conteúdo
* tempo restante de expiração (TTL)

---

# ⚡ Estratégia de Cache

A API utiliza o Redis para reduzir consultas repetidas ao banco de dados.

Fluxo da listagem de livros:

1. O cliente solicita `GET /livros`.
2. A API verifica se a resposta já existe no Redis.
3. Caso exista, retorna os dados diretamente do cache.
4. Caso contrário, consulta o banco SQLite.
5. O resultado é armazenado no Redis por 30 segundos antes de ser enviado ao cliente.

Essa estratégia reduz o número de consultas ao banco e melhora o desempenho da aplicação.

---

# 🛑 Encerrando a Aplicação

Parar os contêineres:

```bash
docker compose down
```

Remover também os volumes:

```bash
docker compose down -v
```

---

# 👨‍💻 Autor

**Iuri Oliveira**

GitHub: https://github.com/iuriolv

E-mail: [euree.olv@gmail.com](mailto:euree.olv@gmail.com)
