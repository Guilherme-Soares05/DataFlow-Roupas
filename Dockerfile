FROM alpine:3.19

RUN apk add --no-cache python3 py3-pip

WORKDIR /app

# Crie o ambiente virtual
RUN python3 -m venv /app/venv

# Ative o ambiente virtual e defina o PATH em comandos separados
RUN . /app/venv/bin/activate
ENV PATH="/app/venv/bin:$PATH"

# Copie os arquivos de requirements e instale as dependências dentro do ambiente virtual
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da sua aplicação
COPY . /app

# Exponha a porta em que a aplicação Flask será executada
EXPOSE 8000

# Defina a variável de ambiente FLASK_APP
ENV FLASK_APP=app.py

# Comando para iniciar a aplicação Flask
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]