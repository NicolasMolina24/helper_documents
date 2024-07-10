# helper_documents
This repository contains a RAG for uploading and chatting with the documents of your choice.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Authors](#authors)
- [Project Status](#project-status)



## Requirements
1.  Create a file named `.env` in `front` folder following format:

    - [OPENAI_API_KEY] = "*****************"
    - [MILVUS_URI] = "/myapp/milvus_demo.db"
    - [BACKEND_HOST] = "back_docchat"
    - [BACKED_PORT] = "8080"

    ```sh where


    ```

2.  Create a file named `.env` in `rag_service` folder following format:

    ```sh where
    - [OPENAI_API_KEY] = ""
    - [POSTGRES_USER_DB] = "postgres"
    - [POSTGRES_PASSWORD_DB] = "1234"
    - [POSTGRES_DB_DB] = "rag"
    - [POSTGRES_HOST_DB] = "postgres_rag"
    - [POSTGRES_PORT_DB] = "5432"
    - [MILVUS_URI] = "/myapp/milvus_demo.db"
    ```

## Requirements
1.  run `docker-compose` to create the container:

    ```docker compose up --build```