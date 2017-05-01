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
from flask import Flask

app = Flask(__name__)

@app.route('/')
def fake_news():
	train_data = pd.read_csv('train_data.csv')
	y_train_type = pd.read_csv('y_train_type.csv')
	x_train, x_test, y_train, y_test = train_test_split(train_data, y_train_type, test_size=0.50, random_state=42)
	y_train = y_train['0'].tolist()
	y_test = y_test['0'].tolist()
	forest = RandomForestClassifier(n_estimators = 50) 
	forest = forest.fit(x_train, y_train)
	x_test_pred = forest.predict(x_test)
	accuracy  = metrics.accuracy_score(y_test,x_test_pred)
	return str(accuracy)
