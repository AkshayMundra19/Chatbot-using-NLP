import json
import pickle
import random
import string
import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download("punkt")
nltk.download("stopwords")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb"))

with open(os.path.join(BASE_DIR, "intents.json"), encoding="utf-8") as f:
    intents = json.load(f)

def clean_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w not in string.punctuation]
    tokens = [w for w in tokens if w not in stopwords.words("english")]
    return " ".join(tokens)

def get_response(user_text):
    cleaned = clean_text(user_text)
    vector = vectorizer.transform([cleaned])
    probs = model.predict_proba(vector)[0]

    if max(probs) < 0.2:
        return "Sorry I didn't understand that."

    tag = model.classes_[probs.argmax()]

    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "Sorry I didn't understand that."
