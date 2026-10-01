# Imagem base com Python
FROM python:3.12-slim

# Diretorio de trabalho dentro do container
WORKDIR /app

# Instalacao das dependencias (copiadas antes para aproveitar o cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia dos arquivos da aplicacao
COPY . .

EXPOSE 5000

# Comando de inicializacao
CMD ["python", "app.py"]
