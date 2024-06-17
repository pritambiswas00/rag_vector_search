from pymongo import MongoClient, database, collection
from requests import post
from bson import objectid
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime


client: MongoClient = MongoClient("<MONGO_DB_URI>")
db: database.Database = client.sample_mflix
movie_collection: collection.Collection = db.movies
movie_items = movie_collection.find({ 'plot':{ "$exists":True } }).limit(50)



hugging_face_access_token:str = "<HUGGING_FACE_API>"
hugging_face_api_inference:str = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding(text:str)->list[float]:
    response = post(
        url=hugging_face_api_inference,
        headers={ "Authorization": f"Bearer {hugging_face_access_token}" },
        json={ "inputs": text }
    )
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code} : {response.text}")
    
    return response.json()


#For adding the embedding in the documents

# for movie in movie_items:
#     movie["plot_embedding_hf"] = generate_embedding(movie["plot"])
#     movie_collection.replace_one({ '_id':movie['_id'] }, movie)

# for doc in movie_collection.find({ 'plot': { "exists": True } }).limit(50):
#     print(doc)
    # doc["plot_embedding_hf"] = generate_embedding(doc["plot"])
    # movie_collection.replace_one({ '_id':doc['_id'] },doc)



query:str = "iron man"
results = movie_collection.aggregate([
    {
        "$vectorSearch":{
            "queryVector": generate_embedding(query),
            "path": "plot_embedding_hf",
            "numCandidates":100,
            "limit": 4,
            "index": "semantic_search"
        }
    }
])

for item in results:
    title = item["title"]
    plot = item["plot"]
    print(f"Movie Name: {title}, \nMovie Plot: {plot}\n")