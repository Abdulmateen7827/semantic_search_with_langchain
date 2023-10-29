from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline.data_ingestion import LoadDB
from langchain.prompts import PromptTemplate
import sys
import os
import openai
from fastapi import FastAPI, UploadFile, File, Form
import tempfile

sys.path.append(os.getcwd())

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

app = FastAPI(title="Semantic search on doc")


db = LoadDB()

class InferenceRequest(BaseModel):
    question: str


# Create an API endpoint for making inferences
@app.post("/predict/")
async def predict(request: str = Form(...),pdf: UploadFile=File(...)):

    data_point = request
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf.file.read())
    file_path = temp_file.name
    # Make the inference using your database and QA_CHAIN_PROMPT
    qa_chain = db.load_db(file=file_path,chain_type='stuff',k=4)

    result = qa_chain({"question": data_point})
    return {"result": result['answer']}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
