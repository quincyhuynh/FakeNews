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


def add_row(df, site_url, title):
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
    df_row = pd.DataFrame(data, columns=cols)
    df = df.append(df_row, ignore_index=True)
    return df


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

def preprocess_data(df, wnl):
    title_clean = title_cleaner(df['title'][0])
    text_clean = title_cleaner(df['text'])
    title_l = pos_tag(title_clean.split())
    text_l = pos_tag(text_clean.split())
    # title_clean_wnl = 



