from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils import clean_skills

class JobRecommender:
    def __init__(self, df, tfidf, tfidf_matrix):
        self.df = df.reset_index(drop=True)
        self.tfidf = tfidf
        self.tfidf_matrix = tfidf_matrix

    @classmethod
    def from_csv(cls, path="jobs.csv"):
        path = Path(path)
        df = pd.read_csv(path)
        df = df[['job_title', 'skills']].dropna()
        df['skills'] = df['skills'].apply(clean_skills)
        df = df[df['skills'].astype(bool)].copy()
        df['combined'] = df['job_title'].fillna("") + " " + df['skills']

        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(df['combined'])

        return cls(df, tfidf, tfidf_matrix)

    def recommend(self, user_input, top_n=5):
        if not user_input or not user_input.strip():
            return self.df.head(top_n).reset_index(drop=True)

        user_vec = self.tfidf.transform([user_input])
        similarity = cosine_similarity(user_vec, self.tfidf_matrix)[0]
        top_indices = similarity.argsort()[-top_n:][::-1]

        return self.df.iloc[top_indices].reset_index(drop=True)


_recommender = None

def get_recommender(path="jobs.csv"):
    global _recommender
    if _recommender is None:
        _recommender = JobRecommender.from_csv(path)
    return _recommender


def recommend_jobs(user_input, top_n=5):
    return get_recommender().recommend(user_input, top_n)
