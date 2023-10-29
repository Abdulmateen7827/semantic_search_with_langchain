from src.logger import logging
from src.exception import CustomException
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.chains import RetrievalQA,  ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory


class LoadDB:
    def __init__(self) -> None:
        logging.info('Initializing model name')
        self.llm_name = "gpt-3.5-turbo"

    def load_db(self, file, chain_type, k):
        self.file = file
        self.chain_type = chain_type
        self.k = k
        try:
            logging.info("Loading documents")
            self.loader = PyPDFLoader(self.file)
            self.documents = self.loader.load()
            
            logging.info("Split documents")

            self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
            self.docs = self.text_splitter.split_documents(self.documents)

            logging.info("Embedding")
            self.embeddings = OpenAIEmbeddings()

            logging.info("Creating vector database from data")

            self.db = DocArrayInMemorySearch.from_documents(self.docs, self.embeddings)
            logging.info("defining retriever")
            self.retriever = self.db.as_retriever(search_type="similarity", search_kwargs={"k": k})
            logging.info("Adding memory")
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            logging.info("Creating chatbot chain")

            qa = ConversationalRetrievalChain.from_llm(
                llm=ChatOpenAI(model_name=self.llm_name, temperature=0), 
                chain_type=self.chain_type, 
                retriever=self.retriever, 
                # return_source_documents=True,
                # return_generated_question=True,
                memory=memory
            )
            return qa
        except Exception as e:
            raise CustomException(e,sys)
