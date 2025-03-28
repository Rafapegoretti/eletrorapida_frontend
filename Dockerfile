# Usa imagem oficial leve do Python
FROM python:3.12-slim

# Variáveis de ambiente básicas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Atualiza e instala libs do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia dependências
COPY requirements.txt .

# Instala pacotes do projeto
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todos os arquivos do projeto
COPY . .

# Expõe a porta da aplicação (não obrigatório, apenas para referência)
EXPOSE 8080

# Comando padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]