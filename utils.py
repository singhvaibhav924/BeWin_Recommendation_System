import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from pymongo import MongoClient

def connector() :
    config = {
        "ATLAS_URI" : "",
        "DB_NAME" : ""
    }
    ids = []
    skills = []
    mongodb_client = MongoClient(config["ATLAS_URI"])
    database = mongodb_client[config["DB_NAME"]]
    collection = database["Candidates"]
    cursor = collection.find({}, {"id": 1, "skills": 1})
    for doc in cursor:
        ids.append(doc["id"])
        skills.append(doc["skills"])
    print("IDs:", ids)
    print("Skills:", skills)
    
    ids = ["a", "b", "c"]
    skills = [["HTML", "CSS", "JavaScript", "Reactjs", "Nodejs"], ["Java", "MySQL"], ["MachineLearning", "DeepLearning", "Numpy", "Pandas", "MySQL"]]
    return ids, skills

def generate_recommendations(skills, k=3):
    tfidf_vectorizer = TfidfVectorizer()
    skills_tfidf = tfidf_vectorizer.fit_transform([" ".join(skill) for skill in skills])
    print(skills_tfidf)
    knn_model = NearestNeighbors(n_neighbors=k, algorithm='brute', metric='cosine')
    knn_model.fit(skills_tfidf)
    return tfidf_vectorizer, knn_model

def get_recommendations(vectorizer, ids_arr, knn_model, skills) :
    user_skills_tfidf = vectorizer.transform([" ".join(skills)])
    distances, indices = knn_model.kneighbors(user_skills_tfidf)
    print(distances)
    print(indices)
    recommendations = []
    for idx in indices[0]:
        recommendations.append(ids_arr[idx])
    return recommendations
