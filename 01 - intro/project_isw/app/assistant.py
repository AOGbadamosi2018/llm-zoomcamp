import os
from elasticsearch import Elasticsearch
from openai import OpenAI

#from sentence_transformers import SentenceTransformer


MODEL_NAME = os.getenv("MODEL_NAME")
#model = SentenceTransformer(MODEL_NAME)


ELASTIC_URL = os.getenv('ELASTIC_URL', 'http://elasticsearch:9200')
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama:11434/v1/')


es_client = Elasticsearch(ELASTIC_URL)
# client = OpenAI(
#     base_url=OLLAMA_URL,
#     api_key='ollama'
# )

# def elastic_search_semantic(query, subject=None, index_name="isw-rebirth-faq"):
#     query=search_term
#     #vector_search_term=model.encode(search_term)
#     # knn_query = {
#     #     "field": "text_vector",
#     #     "query_vector": vector_search_term,
#     #     "k": 5,
#     #     "num_candidates": 100
#     # }

    
#     knn_query = {
#         "field": "text",
#         "query_vector": vector_search_term,
#         "k": 5,
#         "num_candidates": 100
#     }
    
#     if subject and subject in ["isw_general_faq", "qt_rebirth_faq"]:
#         response = es_client.search(
#             index=index_name,
#             query={
#                 "match": {"subject": f"{subject}"},
#             },
#             knn=knn_query,
#             size=5,
#             explain=True
#         )
#     else:
#         response = es_client.search(
#             index=index_name,
#             knn=knn_query,
#             size=5,
#             explain=True
#         )
#     return [hit['_source'] for hit in response['hits']['hits']]

def elastic_search(query, subject=None, index_name="course-questions"):

    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question", "text"],
                        "type": "best_fields"
                    }
                }
            }
        }
    }

    if subject and subject in ["isw_general_faq", "qt_rebirth_faq"]:
        search_query["query"]["bool"]["filter"] = {
            "term": {"subject": subject}
        }

    response = es_client.search(index=index_name, body=search_query)
    
    return [hit['_source'] for hit in response['hits']['hits']]
    
  


def build_prompt(query, search_results):
    prompt_template = """
You're a Financial Services application assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.
If the CONTEXT doesn't contain the answer , output NONE

QUESTION: {question}

CONTEXT: 
{context}
""".strip()

    context = "\n\n".join([f"question: {doc['question']}\nanswer: {doc['text']}" for doc in search_results])
    return prompt_template.format(question=query, context=context).strip()

# def llm(prompt):
#     response = client.chat.completions.create(
#         model='phi3',
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content

def llm(prompt):
    #client = OpenAI(api_key = os.environ['OPENAI_API_KEY'])
    client = OpenAI(api_key = os.getenv('OPENAI_API_KEY', 'somethingspecial'))
    response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{"role":'user', "content":prompt}])

    return response.choices[0].message.content

def get_answer(query, subject=None):
    search_results = elastic_search(query, subject=None)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer