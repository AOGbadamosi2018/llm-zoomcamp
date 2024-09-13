import os
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm
from dotenv import load_dotenv

from db import init_db



load_dotenv()

ELASTIC_URL = os.getenv("ELASTIC_URL_LOCAL")
MODEL_NAME = os.getenv("MODEL_NAME")
INDEX_NAME = os.getenv("INDEX_NAME")


# Constants

BASE_URL = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main'


def fetch_documents():
    documents = []
    print("Fetching documents...")
    #relative_url = '03-vector-search/eval/documents-with-ids.json'
    #docs_url = f'{BASE_URL}/{relative_url}?raw=1'
    with open('/workspaces/llm-zoomcamp/01 - intro/project_isw/app/isw_rebirth_faq_document.json', 'r') as f_in:
        docs_raw = json.load(f_in)
    for isw_dict in docs_raw:
        for doc in isw_dict['documents']:
            doc['subject'] = isw_dict['subject']
            documents.append(doc)
    print(f"Fetched {len(documents)} documents", type(documents))
    


    return documents

# def fetch_ground_truth():
#     print("Fetching ground truth data...")
#     relative_url = '03-vector-search/eval/ground-truth-data.csv'
#     ground_truth_url = f'{BASE_URL}/{relative_url}?raw=1'
#     df_ground_truth = pd.read_csv(ground_truth_url)
#     df_ground_truth = df_ground_truth[df_ground_truth.course == 'machine-learning-zoomcamp']
#     ground_truth = df_ground_truth.to_dict(orient='records')
#     print(f"Fetched {len(ground_truth)} ground truth records")
#     return ground_truth

def load_model():
    print(f"Loading model: {MODEL_NAME}")
    return SentenceTransformer(MODEL_NAME)

def setup_elasticsearch():
    print("Setting up Elasticsearch...")
    es_client = Elasticsearch(ELASTIC_URL)
    
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "question": {"type": "text"},
                "subject": {"type": "keyword"} ,
                "text_vector": {"type": "dense_vector", "dims": 768, "index": True, "similarity": "cosine"},
            }
        }
    }

    es_client.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    es_client.indices.create(index=INDEX_NAME, body=index_settings)
    print(f"Elasticsearch index '{INDEX_NAME}' created")
    return es_client

def index_documents(es_client, documents, model):
    print("Indexing documents...")
    for doc in tqdm(documents):
        question = doc['question']
        text = doc['text']
        doc['text_vector'] = model.encode(text).tolist()
        es_client.index(index=INDEX_NAME, document=doc)
    print(f"Indexed {len(documents)} documents")

def main():
    print("Starting the indexing process...")
    
    documents = fetch_documents()
 #   ground_truth = fetch_ground_truth()
    model = load_model()
    es_client = setup_elasticsearch()
    index_documents(es_client, documents, model)
    
    print("Initializing database...")
    init_db()
    
    print("Indexing process completed successfully!")

if __name__ == "__main__":
    main()