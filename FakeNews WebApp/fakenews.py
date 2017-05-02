import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize
import re
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn import linear_model, datasets
from sklearn.externals import joblib
from flask import Flask, request, jsonify
from clean_article import *
import webhoseio


app = Flask(__name__)

# web scraper credentials
webhoseio.config(token="456af32b-3c58-455d-b9f8-90875bfc8f58")

# set up models
train_data = pd.read_csv('../train_data.csv')
y_train_type = pd.read_csv('../y_train_type.csv')
x_train, x_test, y_train, y_test = train_test_split(train_data, y_train_type, test_size=0.50, random_state=42)
y_train = y_train['0'].tolist()
y_test = y_test['0'].tolist()
forest = RandomForestClassifier(n_estimators = 50)
forest = forest.fit(x_train, y_train)

# set up prediction df
cols = ["uuid", "ord_in_thread", "author", "published", "title", "text", "language", "crawled", "site_url", "country", "domain_rank", "thread_title", "spam_score", "main_img_url", "replies_count", "participants_count", "likes", "comments", "shares", "type"]
df = pd.DataFrame(columns = cols)

# set up cleaning helpers


@app.route('/')
def hello():
    return 'hello'

@app.route('/predict', methods=['GET', 'POST'])
def fake_news():
    article_url = request.args['url']
    # articled_cleaned = process_article(article_url)
    x_test_pred = forest.predict(x_test)
    accuracy  = metrics.accuracy_score(y_test,x_test_pred)
    return str(request.args['url'])
