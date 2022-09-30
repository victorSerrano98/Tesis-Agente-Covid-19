from elasticsearch import Elasticsearch
from fastapi import FastAPI
from pydantic import BaseModel

from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
import os
from haystack.pipeline import ExtractiveQAPipeline
from haystack.reader.farm import FARMReader
from haystack.retriever.sparse import ElasticsearchRetriever

ELASTIC_SEARCH_HOST =  os.environ.get('es_ip', 'localhost')
#ELASTIC_SEARCH_HOST =  os.environ.get('es_ip', '34.135.163.252')
ELASTIC_SEARCH_PORT =  os.environ.get('es_port', 9200)

document_store = ElasticsearchDocumentStore(host=ELASTIC_SEARCH_HOST,
                                            port= ELASTIC_SEARCH_PORT,
                                            username="", password="",
                                            index="document")

retriever = ElasticsearchRetriever(document_store=document_store, top_k=10)
#reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2-covid", use_gpu=True)
reader = FARMReader(model_name_or_path="JAlexis/ModelTT_Covid19", use_gpu=True, context_window_size=500)
#reader = FARMReader(model_name_or_path="Akert/test02", use_gpu=True, context_window_size=500)
pipe = ExtractiveQAPipeline(reader, retriever)



app = FastAPI()

class Queobj(BaseModel):
    question: str
    num_answers: int
    num_docs: int

@app.post('/query')
async def query(que_obj: Queobj):
    question = que_obj.question
    k_retriver = que_obj.num_docs
    k_reader = que_obj.num_answers
    prediction = pipe.run(query=question, top_k_retriever=k_retriver, top_k_reader=k_reader)

    return {'answer': prediction}
