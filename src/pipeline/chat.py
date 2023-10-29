from src.logger import logging
from src.exception import CustomException
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os
import openai
import sys
from dataclasses import dataclass
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from src.pipeline.data_ingestion import LoadDB


logging.info("Getting openapi keys")
sys.path.append(os.getcwd())

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']




if __name__ == "__main__":


    file = '/Users/abdulmateen/tensorflow-test/langchain/notebook/data/MachineLearning-Lecture01.pdf'
    logging.info("Collecting question")
    question = "Is probability a class topic?"

    db = LoadDB()
    qa_chain = db.load_db(file=file,chain_type='stuff',k=4)
    result = qa_chain({"question": question})
    print(result["answer"])





