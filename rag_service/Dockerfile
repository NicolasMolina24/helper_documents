FROM ubuntu:22.04

# Actualizar el sistema y luego instalar Python
RUN apt-get update && apt-get install -y python3 python3-pip

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

RUN pip install -r requirements.txt
# re install pymilvus to avoid error
RUN pip install pymilvus

EXPOSE 8080
RUN pip install pymilvus
ENTRYPOINT ["uvicorn", "app:app", "--reload"]
