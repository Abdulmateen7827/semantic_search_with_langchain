# Document search with Langchain + Fastapi + docker

This project demonstrates how to create a End to End real time conversation with your documents using langchain document loaders.
It uses Fastapi to create a web server to interact with the application and spinned up with docker to get real time inferences.

## Project overview
The model used is the openai GPT-3.5-turbo model to create the chatbot.

- Document Loading
Documents are loaded from a specified file using the PyPDFLoader.
The loaded documents are split into smaller chunks for further processing.

- Embedding
The project uses OpenAIEmbeddings to generate embeddings for the document chunks.

- Vector Database
A vector database is created using DocArrayInMemorySearch, which allows for efficient document retrieval based on similarity.

- Chatbot Chain
A conversational retrieval chain is established. It uses the chatbot model, retriever, and a memory buffer to store conversation history.

## How to run the project?
1. Create a virtual env
2. Clone the repository
3. Install the dependencies:
`pip install -r requirements.txt`
4. Add your Openapi keyto the .env file
5. Start the fastapi server by running:
`uvicorn main:app --reload`
6. Then go to the fastapi swagger ui:
`http://127.0.0.1:8000/docs`
