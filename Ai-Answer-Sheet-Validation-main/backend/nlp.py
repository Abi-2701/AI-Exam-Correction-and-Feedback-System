from aiohttp import web
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string, nltk
from sentence_transformers import SentenceTransformer, util

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

model = SentenceTransformer('all-MiniLM-L6-v2')

def preprocess(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]
    return tokens

def keyword_matching(keywords, user_answer):
    matched_keywords = [word for word in keywords if word in user_answer]
    return len(matched_keywords), matched_keywords

def semantic_similarity(reference, user_answer):
    embeddings = model.encode([reference, user_answer], convert_to_tensor=True)
    score = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
    return score

def grade_answer(keywords, reference_answer, user_answer, total_marks):
    keywords_processed = preprocess(' '.join(keywords))
    user_answer_processed = preprocess(user_answer)
    matched_count, matched_keywords = keyword_matching(keywords_processed, user_answer_processed)
    keyword_score = (matched_count / len(keywords_processed)) * total_marks
    similarity_score = semantic_similarity(reference_answer, user_answer)
    similarity_marks = similarity_score * total_marks
    final_score = (0.7 * keyword_score) + (0.3 * similarity_marks)
    rounded_score = round(final_score * 2) / 2
    return rounded_score, matched_keywords, similarity_score

