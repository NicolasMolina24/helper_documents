FROM python:3.12-slim-bookworm

RUN mkdir -p /myapp/rag_service

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /myapp/rag_service

# COPY . /myapp
COPY ./rag_service /myapp/rag_service

# Listar el contenido de /myapp1
# RUN echo "Contenido de /myapp:" && ls -l /myapp/rag_service

# Instala las dependencias necesarias para PostgreSQL y compilar extensiones
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r /myapp/requirements.txt


EXPOSE 8000

ENTRYPOINT ["uvicorn", "app.app", "--reload"]