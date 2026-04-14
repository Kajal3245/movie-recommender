import streamlit as st
import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("movies_small.csv")

def convert(obj):
    try:
        return " ".join([i['name'] for i in ast.literal_eval(obj)])
    except:
        return ""

df['genres'] = df['genres'].apply(convert)

df['overview'] = df['overview'].astype(str)
df['tags'] = df['overview'] + " " + df['genres']

tfidf = TfidfVectorizer(stop_words='english')
vectors = tfidf.fit_transform(df['tags']).toarray()

def recommend(user_input):
    input_vec = tfidf.transform([user_input]).toarray()
    sim_scores = cosine_similarity(input_vec, vectors)[0]
    top_indices = sim_scores.argsort()[-5:][::-1]

    results = []
    for i in top_indices:
        title = df.iloc[i]['title']
        rating = df.iloc[i]['vote_average']
        score = sim_scores[i]
        results.append((title, rating, score))
    return results

st.title("🎬 Movie Recommender System")

user_input = st.text_input("Enter movie mood or description:")

if st.button("Recommend"):
    results = recommend(user_input)
    for title, rating, score in results:
        st.write(f"⭐ {title} ({rating})")
        st.write(f"Confidence: {round(score*100,2)}%")
        st.write("---")
