import os
import uvicorn
import datetime
import pandas as pd
import requests
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from typing import Union
from fastapi import FastAPI
from fastapi import Header, Depends, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional
from config import config
from client.pipeline import clsPipeline

import traceback

app = FastAPI()
time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = None

class inferencePipeline(BaseModel):
    companyCik: str = Field(title='Company CIK')

@app.on_event('startup')
def startup_event():
    try:
        global vector_db
        print('Starting up...')
        vector_db = FAISS.load_local(config['VECTOR_DB_PATH'], embeddings)
        print('Vector db Startup complete!')
    except Exception as e :
        print(e)

def get_vector_db():
    return vector_db

@app.get("/api/healthcheck")
def healthcheck():
    """returns a health check message"""
    mssg = 'API is up and running ' + time_str
    return mssg

@app.post('/api/v1/getSimilarCompanies')
def inference(
        req_body: inferencePipeline,
        vector_db: FAISS = Depends(get_vector_db)
):
    """
    Entry Point for a code
    """
    try:
        companyCik = req_body.companyCik
        objPipeline = clsPipeline()
        json_output = objPipeline.run(companyCik,'./data',vector_db)
        
        return json_output
    except Exception as e:
        print(traceback.print_exc())
        return {"Error" : e}
       



if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8005, reload=True)


