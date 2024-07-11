# DocChat a helpper document  
This repository contains a RAG (Retrieval-Augmented Generation) system for uploading and chatting with the documents of your choice. It integrates streamlit as front, a vector database and LangChain as a framework, this app allow users to upload files (pdf) and ask questions based on those files. The application also keeps track of the conversation history, stores it in a PostgreSQL database, and provides an API for querying.

![Front](https://github.com/NicolasMolina24/helper_documents/blob/main/imgs/conversation.jpg){width=600px}

## Table of Contents
- [Features](##Features)
- [Prerequisites](##Prerequisites)
- [Setup](#usage)
- [API Endpoints](#documentation)
- [Contributing](#authors)
- [License Status](#project-status)
- [Contact](#Contact)


## Features

- **File Upload:** Users can upload files to the application.
- **Question Answering:** Users can ask questions related to the uploaded files.
- **Conversation History:** The application keeps track of the last 5 questions and answers.
- **Persistent Storage:** Conversation history is stored in a PostgreSQL database.
- **API Access:** Simple API endpoint (`/api/query`) to perform queries. Optional support for querying specific documents.
- **Dockerized Deployment:** The entire application can be deployed using Docker Compose.

## Prerequisites

- Docker
- Docker Compose


## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/NicolasMolina24/helper_documents.git
   cd helper_documents
   ```

2. **Environment Variables:**
Create a file named `.env` in the root of the project following format:

    ```sh where
        - OPENAI_API_KEY = "*******YOUR*API*KEY*HERE*******"
        - POSTGRES_USER_DB = "postgres"
        - POSTGRES_PASSWORD_DB = "1234"
        - POSTGRES_DB_DB = "rag"
        - POSTGRES_HOST_DB = "localhost"
        - POSTGRES_PORT_DB = "5432"
        - MILVUS_URI = "./chroma_db"
        - BACKED_PORT = "8000"
        - BACKEND_HOST = "localhost"
    ```

where :
**OPENAI_API_KEY**: your OpenAi API key to access gpt models
**POSTGRES_USER_DB**: the user declared in postgres
**POSTGRES_PASSWORD_DB**: password declared in postgres
**POSTGRES_DB_DB**: name for the database
**POSTGRES_HOST_DB**: host of the database
**POSTGRES_PORT_DB**: port for database connection
**MILVUS_URI**: uri or path for vectorstorage
**BACKED_PORT**: backend port
**BACKEND_HOST**: backend host.

3. **Docker Compose:**

Run the following command to start the services:
   ```bash
    docker-compose up -d
```


## API Endpoints
![Backend](https://github.com/NicolasMolina24/helper_documents/blob/main/imgs/service.jpg){width=600px}

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/NicolasMolina24/helper_documents/blob/main/LICENSE) file for details.

## Contact

If you have any questions or need further assistance, please feel free to contact me at
- **Nicolás Alberto Molina** - [github](https://github.com/NicolasMolina24) - [Linkedin](https://www.linkedin.com/in/nicolas-molina-data/)

