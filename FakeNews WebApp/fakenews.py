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
import webhoseio
from aylienapiclient import textapi
from urllib.parse import urlparse
import pdb
import webhoseio


app = Flask(__name__)

# web scraper credentials
webhoseio.config(token="456af32b-3c58-455d-b9f8-90875bfc8f58")
client = textapi.Client("4657dfa6", "bbfd5faa23a1020d92e946dd83bce6b7")

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

def get_title_and_site_url(url):
    # pdb.set_trace()
    extract = client.Extract({"url": url, "best_image": False})
    title = re.escape(extract['title'])
    site_url = re.sub('www.', '', urlparse(url).hostname)
    return title, site_url

def extract_article(url):
    title, site_url = get_title_and_site_url(url)
    output = webhoseio.query("filterWebData", {"q":"thread.title:(" + title + ") site:" + site_url})
    post = output["posts"][0]
    thread = post["thread"]
    social = thread["social"]["facebook"]
    uuid = post["uuid"]
    ord_in_thread = post["ord_in_thread"]
    author = post["author"]
    published = post["published"]
    title = post["title"]
    text = post["text"]
    language = post["language"]
    crawled = post["crawled"]
    site_url = thread["site"]
    country = thread["country"]
    domain_rank = thread["domain_rank"]
    thread_title = thread["title"]
    spam_score = thread["spam_score"]
    img = thread["main_image"]
    replies = thread["replies_count"]
    participants = thread["participants_count"]
    likes = social["likes"]
    comments = social["comments"]
    shares = social["shares"]
    data = [[uuid, ord_in_thread, author, published, title, text, language, crawled, site_url, country, domain_rank, thread_title, spam_score, img, replies, participants, likes, comments, shares, "N/A"]]
    article_extracted_df = pd.DataFrame(data, columns=cols)
    return article_extracted_df

def clean_article(article_df):
    article_df_clean = article_df
    article_df_clean = article_df_clean[cols]
    del article_df_clean['uuid']
    del article_df_clean['thread_title']
    del article_df_clean['spam_score']
    del article_df_clean['main_img_url']
    del article_df_clean['published']
    del article_df_clean['crawled']
    del article_df_clean['type']
    article_df_clean['title'].fillna('', inplace=True)
    article_df_clean['text'].fillna('', inplace=True)
    article_df_clean.fillna(0, inplace=True)
    title = title_cleaner(article_df_clean['title'][0])
    text = title_cleaner(article_df_clean['text'][0])
    title_tag = pos_tag(title.split())
    title_clean_wnl = ' '.join([wnl.lemmatize(w,pos=get_wordnet_pos(t)) for w,t in title_tag])
    text_tag = pos_tag(text.split())
    text_clean_wnl = ' '.join([wnl.lemmatize(w,pos=get_wordnet_pos(t)) for w,t in text_tag])
    le = joblib.load(u'label_encoder.pkl')
    # le = joblib.load(u'/home/quincyhuynh/FakeNewsApp/label_encoder.pkl')
    l = ['country','site_url','author','language']
    for col in l:
        le.fit(article_df_clean[col])
        article_df_clean[col] = le.transform(article_df_clean[col])
        article_df_clean[col] = article_df_clean[col].astype(float)
    article_df_clean['title'] = title_clean_wnl
    article_df_clean['text'] = text_clean_wnl
    return article_df_clean

@app.route('/')
def hello():
    return 'Fake News Detector Home Page'

@app.route('/predict', methods=['GET', 'POST'])
def fake_news():
    try:
        article_url = request.args['url']
        article_df = extract_article(article_url)
        article_df_clean = clean_article(article_df)
        classifier = joblib.load(u'classifier.pkl')
        # classifier = joblib.load(u'/home/quincyhuynh/FakeNewsApp/classifier.pkl')
        prediction = classifier.predict_proba(article_df_clean)[0]
        prob_notfake = str(prediction[1]*100)
        return str(prob_notfake) + '%  CERTAINTY'
    except:
        return "Sorry, could not determine trustworthiness of article"
