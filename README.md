# 📘 Eletrônica Rápida - Frontend

Sistema web de gestão de componentes eletrônicos - Módulo Frontend.

---

## 1. 🔧 Preparação do Ambiente

### a. Dependências Necessárias

- Python 3.12+
- pip
- Git
- Docker e Docker Compose (para execução conteinerizada)

#### Pacotes Python:
- `Django`
- `requests`
- `python-dotenv`

> Todas as dependências estão listadas no arquivo `requirements.txt`.

### b. Orientações por Sistema Operacional

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git docker.io docker-compose -y
```

#### Windows

1. Instale:
   - [Python](https://www.python.org/downloads/)
   - [Git](https://git-scm.com/download/win)
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. Verifique no terminal/cmd:

```bash
python --version
pip --version
git --version
docker --version
```

---

## 2. 🐳 Execução com Docker Compose

### a. Preparação

Certifique-se de ter o Docker e Docker Compose instalados.

### b. Instruções de Execução

#### i. Subir o ambiente

```bash
docker-compose up --build
```

#### ii. Parar o ambiente

```bash
docker-compose down
```

### c. Estrutura do `docker-compose.yml`

```yaml
version: '3.9'

services:
  frontend:
    build: .
    container_name: frontend_eletronica
    command: python manage.py runserver 0.0.0.0:8080
    volumes:
      - .:/app
    ports:
      - "8080:8080"
    depends_on:
      - backend
    env_file:
      - .env

  backend:
    image: backend_eletronica
    container_name: backend

networks:
  default:
    driver: bridge
```

---

## 3. 🖥️ Execução Manual (Sem Docker)

### a. Criação de Ambiente Virtual

```bash
python -m venv .venv
source .venv/bin/activate     # Linux/Mac
.venv\Scripts\activate      # Windows
```

### b. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### c. Configuração

Crie um arquivo `.env` com o seguinte conteúdo:

```env
API_URL=http://localhost:8000
SECRET_KEY=sua_chave_django
DEBUG=True
```

### d. Executando o Servidor

```bash
python manage.py runserver
```

Acesse em: [http://localhost:8000](http://localhost:8000)

---

## 📂 Estrutura de Pastas

```
.
├── login/
├── usuarios/
├── components/
├── dashboard/
├── templates/
├── static/
├── core/
├── requirements.txt
├── docker-compose.yml
└── manage.py
```

---

## ✍️ Contribuição

Sinta-se à vontade para abrir issues ou pull requests com sugestões de melhorias.

---

## 📄 Licença

Este projeto está sob a licença MIT.
