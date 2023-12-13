import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy
import pandas as pd
from collections import Counter
from sklearn.feature_extraction import DictVectorizer

stop_words_nltk = stopwords.words('english')

# hard coded stop words that should not be removed
non_stop_words = ["yes", "no", "not", "isn't", "aren't", "wasn't", "weren't", "don't", "doesn't", "didn't", "won't", "wouldn't", "shan't", "shouldn't", "can't", "cannot", "couldn't", "mustn't", "needn't", "haven't", "hasn't", "hadn't"]

# stop_word is stop_words_nltk - no_stop_words
stop_words = [word for word in stop_words_nltk if word not in non_stop_words]

def on_start_up():
    nltk.download('popular')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')


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
        filtered_sentence = [w for w in word_tokens if w.lower() not in stop_words]
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
        data['Answer_without_stop_words'] = stop_word_removal(data['Answer'])
        data['Answer_lowercase'] = lower_case(data['Answer_without_stop_words'])

        self.all_words = remove_special_character_words(get_all_words(data['Answer_without_stop_words']))
        self.data = data

        # TODO: lemma, stemma

    def _calculate_word_counts(self):
        feature_words = ["yes", "surely", "hopefully", "no", "not", "n't", "actually", "answer"]
        
        # new column named "count_" + feature_word for each row in self.data 
        # that contains the count of feature_word in the answer
        for feature_word in feature_words:
            self.data["count_" + feature_word] = self.data['Answer'].str.count(feature_word)

    def _calculate_pos(self):
        def extract_pos(text):
            tokens = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(tokens)
            pos_dict = dict(pos_tags)
            return pos_dict
 
        pos_features = [extract_pos(text) for text in self.data['Answer_without_stop_words']]
        vectorizer = DictVectorizer()
        pos_features_vectorized = vectorizer.fit_transform(pos_features)
        # remove emojis
        pos_features_vectorized = pos_features_vectorized[:, ~numpy.all(pos_features_vectorized.toarray() == 0, axis=0)]

        pos_features_df = pd.DataFrame(pos_features_vectorized.toarray(), columns=vectorizer.get_feature_names_out())
        self.data = pd.concat([self.data, pos_features_df], axis=1)

    def calculate_features(self):
        self._calculate_word_counts()
        self._calculate_pos()