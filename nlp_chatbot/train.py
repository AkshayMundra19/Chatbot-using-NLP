import json
import pickle
import string
import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

nltk.download("punkt")
nltk.download("stopwords")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def clean_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w not in string.punctuation]
    tokens = [w for w in tokens if w not in stopwords.words("english")]
    return " ".join(tokens)

with open(os.path.join(BASE_DIR, "intents.json"), encoding="utf-8") as f:
    data = json.load(f)

X = []
y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        X.append(clean_text(pattern))
        y.append(intent["tag"])

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

pickle.dump(model, open(os.path.join(BASE_DIR, "model.pkl"), "wb"))
pickle.dump(vectorizer, open(os.path.join(BASE_DIR, "vectorizer.pkl"), "wb"))

print("Model trained successfully")
