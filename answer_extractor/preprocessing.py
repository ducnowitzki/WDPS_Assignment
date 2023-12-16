import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer

# Selected features after doing NLP analysis

# STOP WORDS
STOP_WORDS_NLTK = stopwords.words("english")

# hard coded stop words that should not be removed
NON_STOP_WORDS = [
    "yes",
    "no",
    "not",
    "isn't",
    "aren't",
    "wasn't",
    "weren't",
    "don't",
    "doesn't",
    "didn't",
    "won't",
    "wouldn't",
    "shan't",
    "shouldn't",
    "can't",
    "cannot",
    "couldn't",
    "mustn't",
    "needn't",
    "haven't",
    "hasn't",
    "hadn't",
]

# stop_word is stop_words_nltk - no_stop_words
STOP_WORDS = [word for word in STOP_WORDS_NLTK if word not in NON_STOP_WORDS]

# FEATURE WORDS
SELECTED_FEATURE_WORDS = [
    "yes",
    "surely",
    "hopefully",
    "no",
    "not",
    "n't",
    "actually",
    "answer",
]

# POS_FEATURES
SELECTED_POS_FEATURES = ["not=RB", "Yes=UH", "no=DT"]

# BIGRAM_FEATURES
SELECTED_BIGRAM_FEATURES = [
    "surely not",
    "yes ,",
    "surely .",
    ", yes",
    "surely !",
    "surely ,",
    "obviously .",
    "yes no",
]


def on_start_up():
    nltk.download("popular", quiet=True)
    nltk.download("punkt", quiet=True)
    nltk.download("averaged_perceptron_tagger", quiet=True)


def lower_case(texts: pd.Series):
    return texts.str.lower()


def get_all_words(texts: pd.Series):
    all_words = " ".join(texts).split()
    # remove special characters
    # all_words = [word for word in all_words if word.isalnum()]
    return all_words


def stop_word_removal(texts: pd.Series):
    stop_words_removed = []
    for text in texts:
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if w.lower() not in STOP_WORDS]
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
    def __init__(
        self,
        training=False,
        data: pd.DataFrame | None = None,
        pos_vectorizer=None,
        bigram_vectorizer=None,
    ):
        self.training = training
        self.pos_vectorizer = pos_vectorizer
        self.bigram_vectorizer = bigram_vectorizer

        data = data.dropna(subset=["Answer"])
        data["Answer_without_stop_words"] = stop_word_removal(data["Answer"])
        data["Answer_lowercase"] = lower_case(data["Answer_without_stop_words"])

        self.all_words = remove_special_character_words(
            get_all_words(data["Answer_without_stop_words"])
        )
        self.data = data

        # TODO: lemma, stemma

    def _calculate_word_counts(self):
        # new column named "count_" + feature_word for each row in self.data
        # that contains the count of feature_word in the answer
        for feature_word in SELECTED_FEATURE_WORDS:
            self.data["count_" + feature_word] = self.data["Answer"].str.count(
                feature_word
            )

    def _calculate_pos(self):
        def extract_pos(text):
            tokens = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(tokens)
            pos_dict = dict(pos_tags)
            return pos_dict

        pos_features = [
            extract_pos(text) for text in self.data["Answer_without_stop_words"]
        ]

        if self.training:
            vectorizer = DictVectorizer()
            pos_features_vectorized = vectorizer.fit_transform(pos_features)

            # pickle vectorizer
            pickle.dump(vectorizer, open("yesno_pos_vectorizer.pkl", "wb"))

        else:
            vectorizer = self.pos_vectorizer
            pos_features_vectorized = vectorizer.transform(pos_features)

        pos_features_df = pd.DataFrame(
            pos_features_vectorized.toarray(),
            columns=vectorizer.get_feature_names_out(),
        )

        # Only take selected pos features
        pos_features_df = pos_features_df.filter(items=SELECTED_POS_FEATURES)

        self.data = pd.concat([self.data, pos_features_df], axis=1)

    def _calculate_bigram(self):
        if self.training:
            vectorizer = CountVectorizer(ngram_range=(2, 2), tokenizer=word_tokenize)
            bigram_features = vectorizer.fit_transform(
                self.data["Answer_without_stop_words"].values.astype("U")
            )

            # pickle vectorizer
            pickle.dump(vectorizer, open("yesno_bigram_vectorizer.pkl", "wb"))

        else:
            vectorizer = self.bigram_vectorizer
            bigram_features = vectorizer.transform(
                self.data["Answer_without_stop_words"].values.astype("U")
            )

        bigram_features_df = pd.DataFrame(
            bigram_features.toarray(), columns=vectorizer.get_feature_names_out()
        )

        # Only take selected bigram features
        bigram_features_df = bigram_features_df.filter(items=SELECTED_BIGRAM_FEATURES)

        self.data = pd.concat([self.data, bigram_features_df], axis=1)

    def calculate_features(self):
        self._calculate_word_counts()
        self._calculate_pos()
        self._calculate_bigram()
