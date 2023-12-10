import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy
import pandas as pd
from collections import Counter

stop_words_nltk = stopwords.words('english')

# hard coded stop words that should not be removed
non_stop_words = ["yes", "no", "not", "isn't", "aren't", "wasn't", "weren't", "don't", "doesn't", "didn't", "won't", "wouldn't", "shan't", "shouldn't", "can't", "cannot", "couldn't", "mustn't", "needn't", "haven't", "hasn't", "hadn't"]

# stop_word is stop_words_nltk - no_stop_words
stop_words = [word for word in stop_words_nltk if word not in non_stop_words]

def on_start_up():
    nltk.download('popular')

def lower_case(texts: pd.Series):
    return texts.str.lower()


def get_all_words(texts: pd.Series):
    all_words = " ".join(texts).split()
    # remove special characters
    #all_words = [word for word in all_words if word.isalnum()]
    return all_words

def stop_word_removal(texts: pd.Series):
    stop_words_removed = []
    for text in texts:
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if w not in stop_words]
        stop_words_removed.append(" ".join(filtered_sentence))

    return stop_words_removed
    

def remove_special_character_words(words):
    new_words = []
    # only remove words that only contains special characters
    for word in words:
        if any(c.isalpha() for c in word):
            new_words.append(word)
    
    return new_words

class Features:
    def __init__(self, data: pd.DataFrame):
        data = data.dropna(subset=['Answer'])
        data['Answer'] = lower_case(data['Answer'])
        data['Answer'] = stop_word_removal(data['Answer'])

        self.all_words = remove_special_character_words(get_all_words(data['Answer']))
        self.data = data

    def _calculate_word_counts(self):
        feature_words = ["yes", "surely", "hopefully", "no", "not", "n't", "actually", "answer"]
        
        # new column named "count_" + feature_word for each row in self.data 
        # that contains the count of feature_word in the answer
        for feature_word in feature_words:
            self.data["count_" + feature_word] = self.data['Answer'].str.count(feature_word)

    def calculate_features(self):
        self._calculate_word_counts()