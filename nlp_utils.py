from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import logging

# Initialize NLP tools
try:
    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    logging.error(f"Error initializing NLP tools: {e}")
    raise

def detect_emotions(content):
    try:
        scores = sid.polarity_scores(content)
        return {
            "Positive": scores['pos'],
            "Negative": scores['neg'],
            "Neutral": scores['neu']
        }
    except Exception as e:
        logging.error(f"Error in detect_emotions: {e}")
        raise

def extract_arguments(content):
    try:
        doc = nlp(content)
        arguments = {f"Argument {i+1}": 0.8 - (i * 0.1) for i, sent in enumerate(doc.sents)}
        return arguments
    except Exception as e:
        logging.error(f"Error in extract_arguments: {e}")
        raise

def get_topics(content):
    try:
        vectorizer = CountVectorizer(max_features=5, stop_words='english')
        X = vectorizer.fit_transform([content])
        return vectorizer.get_feature_names_out()
    except Exception as e:
        logging.error(f"Error in get_topics: {e}")
        raise
