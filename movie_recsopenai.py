from pymongo import MongoClient
import openai


open_ai_api_key:str = "<OPEN_API_KEY>"

openai.api_key = open_ai_api_key
db_client = MongoClient("<MONGODB_URI>")
collection = db_client.embedded_movies

def generated_embedding(text:str)->list[float]:
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response['data'][0]['embedding']

query = "imaginary characters from outer space at war"
results = collection.aggregate([
        {
        "$vectorSearch":{
            "queryVector": generated_embedding(query),
            "path": "<PATH_NAME>",
            "numCandidates":100,
            "limit": 4,
            "index": "<INDEX_NAME>"
        }
    }
])

for document in results:
    title = document["title"]
    plot = document["plot"]
    print(f"Movie Title : {title}.\n Movie Plot: {plot}\n")
