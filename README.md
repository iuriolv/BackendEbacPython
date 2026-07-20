# 📚 Catálogo de Livros API

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache-Kafka-231F20?logo=apachekafka&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-Task%20Queue-37814A?logo=celery&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-Dependency%20Manager-60A5FA?logo=poetry&logoColor=white)

API REST desenvolvida com **FastAPI** para gerenciamento de um catálogo de livros. O projeto integra banco de dados relacional, cache em Redis, mensageria com Apache Kafka e infraestrutura para processamento assíncrono utilizando Celery, além de disponibilizar todo o ambiente por meio do Docker Compose.

---

# ✨ Funcionalidades

- Cadastro de livros
- Listagem paginada de livros
- Atualização de livros
- Exclusão de livros
- Autenticação HTTP Basic
- Persistência utilizando SQLAlchemy
- Cache de consultas com Redis
- Publicação de eventos no Apache Kafka
- Ambiente containerizado com Docker Compose
- Documentação automática da API com Swagger e ReDoc

---

# 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|------------|
| Python 3.12+ | Linguagem principal |
| FastAPI | Framework da API |
| SQLAlchemy | ORM |
| SQLite | Banco de dados |
| Redis | Cache |
| Apache Kafka | Publicação de eventos |
| Celery | Processamento assíncrono |
| Poetry | Gerenciamento de dependências |
| Docker | Containerização |
| Docker Compose | Orquestração dos serviços |

---

# 🏗️ Arquitetura

```text
                 Cliente
                    │
                    ▼
              FastAPI (API)
                    │
      ┌─────────────┼──────────────┐
      │             │              │
      ▼             ▼              ▼
 SQLite        Redis Cache     Apache Kafka
      │
      ▼
 SQLAlchemy ORM

Redis também é utilizado como Broker/Backend do Celery.
```

---

# 📁 Estrutura do Projeto

```text
BackendEbacPython/
│
├── main.py
├── celery_app.py
├── kafka_producer.py
├── tasks.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
├── .env.example
└── README.md
```

---

# ⚙️ Pré-requisitos

Para executar o projeto localmente é necessário possuir:

- Python 3.12 ou superior
- Poetry
- Docker
- Docker Compose

---

# 📥 Clonando o projeto

```bash
git clone https://github.com/iuriolv/BackendEbacPython.git

cd BackendEbacPython
```

---

# 📦 Instalando as dependências

Utilizando Poetry:

```bash
poetry install
```

Ative o ambiente virtual:

```bash
poetry shell
```

---

# 🔐 Configuração

Crie um arquivo `.env`.

Exemplo:

```env
DATABASE_URL=sqlite:///./biblioteca.db

MEU_USUARIO=admin
MINHA_SENHA=admin

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_URL=redis://redis:6379/0

KAFKA_SERVER=kafka:9092
```

---

# 🐳 Executando com Docker

Suba todos os serviços:

```bash
docker compose up --build
```

Serão iniciados os seguintes containers:

| Serviço | Porta |
|----------|-------|
| FastAPI | 8000 |
| Redis | 6379 |
| Kafka | 9092 |
| Kafka UI | 8080 |
| Celery Worker | Interna |

Para executar em segundo plano:

```bash
docker compose up -d --build
```

---

# ▶️ Executando localmente

Caso deseje executar sem Docker:

```bash
poetry run uvicorn main:app --reload
```

A API ficará disponível em:

```
http://localhost:8000
```

---

# 📖 Documentação da API

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# 🔐 Autenticação

Os endpoints da API utilizam **HTTP Basic Authentication**.

Exemplo utilizando cURL:

```bash
curl -u admin:admin http://localhost:8000/livros
```

---

# 📚 Endpoints

## Listar livros

```http
GET /livros?page=1&limit=10
```

Retorna uma lista paginada de livros cadastrados.

---

## Adicionar livro

```http
POST /adicionar
```

Exemplo de payload:

```json
{
    "nome_livro": "Clean Code",
    "autor": "Robert C. Martin",
    "ano": 2008
}
```

Ao cadastrar um livro:

- os dados são persistidos no banco;
- um evento é publicado em um tópico Kafka.

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

Remove um livro do banco de dados e também do cache do Redis.

---

## Visualizar Cache

```http
GET /debug/redis
```

Lista todas as chaves atualmente armazenadas no Redis.

---

# ⚡ Cache com Redis

A listagem de livros utiliza Redis para reduzir consultas repetidas ao banco de dados.

O cache é criado por página utilizando uma chave semelhante a:

```
livros:page:1:limit:10
```

As respostas permanecem armazenadas por **30 segundos** antes de expirarem automaticamente.

Também são armazenadas informações individuais dos livros utilizando chaves no formato:

```
livro:{id}
```

---

# 📨 Publicação de Eventos com Kafka

Sempre que um novo livro é cadastrado, a aplicação publica um evento no tópico:

```
livros_eventos
```

Exemplo da mensagem enviada:

```json
{
    "acao": "livro_criado",
    "livro": {
        "nome_livro": "Clean Code",
        "autor": "Robert C. Martin",
        "ano": 2008
    }
}
```

---

# ⚙️ Celery

O projeto possui configuração para utilização do Celery utilizando o Redis como broker e backend.

Atualmente o worker encontra-se configurado para futuras tarefas assíncronas e pode ser iniciado automaticamente pelo Docker Compose.

---

# 🗄️ Banco de Dados

A aplicação utiliza SQLAlchemy para mapear a tabela:

```
biblioteca
```

Campos disponíveis:

| Campo | Tipo |
|--------|------|
| id | Integer |
| nome_livro | String |
| autor | String |
| ano | Integer |

---

# 📌 Próximos Passos

Algumas melhorias planejadas para futuras versões:

- Testes automatizados
- JWT Authentication
- CI/CD
- Logs estruturados
- Deploy em produção
- Docker Healthcheck
- Monitoramento
- Cobertura de testes

---

# 👨‍💻 Autor

**Iuri Oliveira**

GitHub: https://github.com/iuriolv

E-mail: euree.olv@gmail.com