FROM python:3.12-slim-bookworm

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

ENTRYPOINT ["streamlit", "run", "front_app.py"]