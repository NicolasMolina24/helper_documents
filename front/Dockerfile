FROM ubuntu:22.04

# Actualizar el sistema y luego instalar Python
RUN apt-get update && apt-get install -y python3 python3-pip

RUN mkdir -p /myapp/front

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /myapp/front

# COPY . /myapp
COPY ./front /myapp/front
# RUN echo "Contenido de /myapp/front:" && ls -l /myapp/front
RUN pip install -U pip
RUN pip install -r requirements.txt
# WORKDIR /myapp
EXPOSE 8501
# re install pymilvus to avoid error
RUN pip install pymilvus

ENTRYPOINT ["streamlit", "run", "front_app.py"]