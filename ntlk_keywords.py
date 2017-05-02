# Adapted from: github.com/aneesha/RAKE/rake.py
from __future__ import division
import operator
import nltk
import string

def isPunct(word):
  return len(word) == 1 and word in string.punctuation

def isNumeric(word):
  try:
    float(word) if '.' in word else int(word)
    return True
  except ValueError:
    return False

class RakeKeywordExtractor:

  def __init__(self):
    self.stopwords = set(nltk.corpus.stopwords.words())
    self.top_fraction = 1 # consider top third candidate keywords by score

  def _generate_candidate_keywords(self, sentences):
    phrase_list = []
    for sentence in sentences:
      words = map(lambda x: "|" if x in self.stopwords else x,
        nltk.word_tokenize(sentence.lower()))
      phrase = []
      for word in words:
        if word == "|" or isPunct(word):
          if len(phrase) > 0:
            phrase_list.append(phrase)
            phrase = []
        else:
          phrase.append(word)
    return phrase_list

  def _calculate_word_scores(self, phrase_list):
    word_freq = nltk.FreqDist()
    word_degree = nltk.FreqDist()
    for phrase in phrase_list:
      degree = len(filter(lambda x: not isNumeric(x), phrase)) - 1
      for word in phrase:
        word_freq[word] += 1
        word_degree[word] += 1
        word_degree[word] += 1
        #word_freq.inc(word)
        #word_degree.inc(word, degree) # other words
    for word in word_freq.keys():
      word_degree[word] = word_degree[word] + word_freq[word] # itself
    # word score = deg(w) / freq(w)
    word_scores = {}
    for word in word_freq.keys():
      word_scores[word] = word_degree[word] / word_freq[word]
    return word_scores

  def _calculate_phrase_scores(self, phrase_list, word_scores):
    phrase_scores = {}
    for phrase in phrase_list:
      phrase_score = 0
      for word in phrase:
        phrase_score += word_scores[word]
      phrase_scores[" ".join(phrase)] = phrase_score
    return phrase_scores
    
  def extract(self, text, incl_scores=False):
    sentences = nltk.sent_tokenize(text)
    phrase_list = self._generate_candidate_keywords(sentences)
    word_scores = self._calculate_word_scores(phrase_list)
    phrase_scores = self._calculate_phrase_scores(
      phrase_list, word_scores)
    sorted_phrase_scores = sorted(phrase_scores.iteritems(),
      key=operator.itemgetter(1), reverse=True)
    n_phrases = len(sorted_phrase_scores)
    if incl_scores:
      return sorted_phrase_scores[0:int(n_phrases/self.top_fraction)]
    else:
      return map(lambda x: x[0],
        sorted_phrase_scores[0:int(n_phrases/self.top_fraction)])

def test():
  rake = RakeKeywordExtractor()
  keywords = rake.extract("""
President Donald Trump has stood by claims he was wiretapped under Barack Obama, telling visiting German Chancellor Angela Merkel: "At least we have something in common, perhaps."
US intelligence agencies under Mr Obama reportedly monitored Mrs Merkel's phone, sparking an angry response.
But both Republican and Democratic congressional leaders have said they do not believe Mr Trump was wiretapped.
Mr Trump and Mrs Merkel have discussed key issues including Nato and trade.
Her visit had been scheduled for Tuesday but was postponed due to a snowstorm.
Mr Trump made his wire-tapping jibe in a joint press conference with Mrs Merkel. She gave a quizzical look.
He was also asked about a comment by White House press secretary Sean Spicer that the UK's GCHQ spy agency had carried out wiretapping on Mr Trump during the US election campaign.

Media captionTrump's wiretap saga explained in two minutes
Mr Trump said Mr Spicer had been quoting a comment on Fox TV. The president said he had not offered an opinion on it, adding: "You shouldn't be talking to me, you should be talking to Fox."
Fox later read out a statement on air, saying: "Fox News knows of no evidence of any kind that the now president of the United States was surveilled at any time in any way, full stop."
GCHQ rejected the allegations against it as "nonsense" and Downing Street says it has been assured the US will not repeat the claims.
The US president was also asked if he regretted any of his regular tweets. He said "very seldom", adding that it was a way to "get round the media when it doesn't tell the truth".
The body language was at times awkward. In an earlier photo opportunity in the White House, Mrs Merkel asked him quietly: "Do you want a handshake?" He looked forwards with his hands clasped and did not reply.
  """, incl_scores=True)
  print keywords
  
if __name__ == "__main__":
  test()