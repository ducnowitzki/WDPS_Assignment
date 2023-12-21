import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer

# Selected features after doing NLP analysis

# FEATURE_WORDS
SELECTED_FEATURE_WORDS = [
    "is",
    "are",
    "was",
    "were",
    "will",
    "would",
    "can",
    "do",
    "does",
    "did",
    "have",
    "has",
    "had",
    "may",
    "might",
    "shall",
    "should",
    "must",
    "who",
    "what",
    "where",
    "when",
    "why",
    "how",
    "am",
]

# POS_FEATURES
SELECTED_POS_FEATURES = [
    "Is=VBZ",
    "Are=VBP",
    "Was=VBD",
    "Were=VBD",
    "Will=MD",
    "Would=MD",
    "Can=MD",
    "Do=VBP",
    "Does=VBZ",
    "Did=VBD",
    "Have=VBP",
    "Has=VBZ",
    "Had=VBD",
    "May=MD",
    "Might=MD",
    "Shall=MD",
    "Should=MD",
    "Must=MD",
    "am=VBP",
    "is=VBZ",
    "are=VBP",
    "was=VBD",
    "were=VBD",
    "will=MD",
    "would=MD",
    "can=MD",
    "do=VBP",
    "does=VBZ",
    "did=VBD",
    "have=VBP",
    "has=VBZ",
    "had=VBD",
    "may=MD",
    "might=MD",
    "shall=MD",
    "should=MD",
    "must=MD",
    "Who=WP",
    "What=WP",
    "Where=WRB",
    "When=WRB",
    "Why=WRB",
    "How=WRB",
    "who=WP",
    "what=WP",
    "where=WRB",
    "when=WRB",
    "why=WRB",
    "how=WRB",
]


def on_start_up():
    nltk.download("popular", quiet=True)
    nltk.download("punkt", quiet=True)
    nltk.download("averaged_perceptron_tagger", quiet=True)


def lower_case(texts: pd.Series):
    return texts.str.lower()


def remove_pronouns(text):
    pronouns = [
        "i",
        "you",
        "he",
        "she",
        "it",
        "we",
        "they",
        "me",
        "him",
        "her",
        "us",
        "I",
        "You",
        "He",
        "She",
        "It",
        "We",
        "They",
        "Me",
        "Him",
        "Her",
        "Us",
    ]

    text = " ".join([word for word in text.split() if word not in pronouns])
    return text


class Features:
    def __init__(
        self,
        training=False,
        data: pd.DataFrame | None = None,
        pos_vectorizer=None,
    ):
        self.training = training
        self.pos_vectorizer = pos_vectorizer

        data = data.dropna(subset=["Input"])
        data["Input_no_pronouns"] = data["Input"].apply(remove_pronouns)
        data["Input_lowercase"] = lower_case(data["Input_no_pronouns"])

        self.data = data

    def _count_feature_words(self):
        for feature_word in SELECTED_FEATURE_WORDS:
            self.data["count_" + feature_word] = self.data[
                "Input_no_pronouns"
            ].str.count(feature_word)

    def _count_question_marks(self):
        self.data["count_question_marks"] = self.data["Input_no_pronouns"].str.count(
            "\?"
        )

    def _calculate_pos(self):
        def extract_pos(text):
            tokens = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(tokens)
            pos_dict = dict(pos_tags)
            return pos_dict

        pos_features = [extract_pos(text) for text in self.data["Input_no_pronouns"]]

        if self.training:
            vectorizer = DictVectorizer()
            pos_features_vectorized = vectorizer.fit_transform(pos_features)

            # pickle vectorizer
            pickle.dump(vectorizer, open("question_pos_vectorizer.pkl", "wb"))

        else:
            vectorizer = self.pos_vectorizer
            pos_features_vectorized = vectorizer.transform(pos_features)

        pos_features_df = pd.DataFrame(
            pos_features_vectorized.toarray(),
            columns=vectorizer.get_feature_names_out(),
        )

        # Only take selected pos features
        # pos_features_df = pos_features_df.filter(items=SELECTED_POS_FEATURES)

        self.data = pd.concat([self.data, pos_features_df], axis=1)

    def calculate_features(self):
        self._count_feature_words()
        self._count_question_marks()
        self._calculate_pos()
