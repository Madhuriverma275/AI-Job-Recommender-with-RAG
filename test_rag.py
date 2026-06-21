import unittest

from model import JobRecommender
from utils import extract_skills


class TestAIJobRecommender(unittest.TestCase):
    def test_extract_skills(self):
        text = "I have experience with Python, SQL, and machine learning."
        skills = extract_skills(text)

        self.assertIn("python", skills)
        self.assertIn("machine learning", skills)

    def test_recommend_jobs_returns_rows(self):
        recommender = JobRecommender.from_csv("jobs.csv")
        recommendations = recommender.recommend("python sql", top_n=3)

        self.assertEqual(len(recommendations), 3)
        self.assertIn("job_title", recommendations.columns)
        self.assertIn("skills", recommendations.columns)


if __name__ == "__main__":
    unittest.main()