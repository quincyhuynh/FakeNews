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
from sklearn.model_selection import train_test_split
from sklearn import linear_model, datasets
from sklearn.externals import joblib
from flask import Flask, request, jsonify
import webhoseio


app = Flask(__name__)

# web scraper credentials
webhoseio.config(token="456af32b-3c58-455d-b9f8-90875bfc8f58")

# constructors, helpers and constants
wnl = WordNetLemmatizer()
cols = ["uuid",
		"ord_in_thread",
		"author",
		"published",
		"title",
		"text",
		"language",
		"crawled",
		"site_url",
		"country",
		"domain_rank",
		"thread_title",
		"spam_score",
		"main_img_url",
		"replies_count",
		"participants_count",
		"likes",
		"comments",
		"shares",
		"type"]

def title_cleaner(title):
    title = re.sub('[^a-zA-Z]',' ', title)
    title = title.lower()
    title = nltk.word_tokenize(title)
    eng_stopwords = set(stopwords.words("english"))
    title = [w for w in title if not w in eng_stopwords]
    title = ' '.join([word for word in title])
    return(title)

def get_wordnet_pos(treebank_tag):
    '''Treebank to wordnet POS tag'''
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return 'n' #basecase POS

# test_data = pd.read_table(u'./Data_3-31.csv')
test_data = pd.read_table(u'/home/quincyhuynh/FakeNewsApp/Data_3-31.csv')
test_data = test_data[cols][2:3]
del test_data['uuid']
test_data = test_data.reset_index()
del test_data['index']
del test_data['thread_title']
del test_data['spam_score']
del test_data['main_img_url']
del test_data['published']
del test_data['crawled']
del test_data['type']
test_data['title'].fillna('', inplace=True)
test_data['text'].fillna('', inplace=True)
test_data.fillna(0, inplace=True)
title = title_cleaner(test_data['title'][0])
text = title_cleaner(test_data['text'][0])
title_tag = pos_tag(title.split())
title_clean_wnl = ' '.join([wnl.lemmatize(w,pos=get_wordnet_pos(t)) for w,t in title_tag])
text_tag = pos_tag(text.split())
text_clean_wnl = ' '.join([wnl.lemmatize(w,pos=get_wordnet_pos(t)) for w,t in text_tag])
# le = joblib.load('./label_encoder.pkl')
le = joblib.load(u'/home/quincyhuynh/FakeNewsApp/label_encoder.pkl')
l = ['country','site_url','author','language']
for col in l:
    le.fit(test_data[col])
    test_data[col] = le.transform(test_data[col])
    test_data[col] = test_data[col].astype(float)
test_data['title'] = title_clean_wnl
test_data['text'] = text_clean_wnl

@app.route('/')
def hello():
    return 'Fake News Detector Home Page'

@app.route('/predict', methods=['GET', 'POST'])
def fake_news():
    article_url = request.args['url']
    # classifier = joblib.load('./classifier.pkl')
    classifier = joblib.load(u'/home/quincyhuynh/FakeNewsApp/classifier.pkl')
    prediction = classifier.predict_proba(test_data)[0]
    prob_fake = str(prediction[2]*100)
    amount_bias = str(prediction[1]*100)
    return str(request.args['url']) +  ' ' + str(prob_fake) +  ' ' + str(amount_bias)
