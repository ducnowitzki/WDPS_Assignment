import pickle
import pandas as pd
from answer_extractor.preprocessing import Features, SELECTED_FEATURE_WORDS, SELECTED_POS_FEATURES, SELECTED_BIGRAM_FEATURES

from answer_extractor.train_classifier import DROPPED_COLUMNS

LABEL_DECODING = {0: "yes", 1: "no"}


class AnswerExtractor:
    def __init__(self, model, pos_vectorizer, bigram_vectorizer):
        self.model = model
        self.pos_vectorizer = pos_vectorizer
        self.bigram_vectorizer = bigram_vectorizer

    def _init_answer_df(self, answer: str):
        answer_df = pd.DataFrame({"Answer": [answer]})

        for feature_word in SELECTED_FEATURE_WORDS:
            answer_df["count_" + feature_word] = answer_df['Answer'].str.count(feature_word)

        for feature in SELECTED_POS_FEATURES + SELECTED_BIGRAM_FEATURES:
            answer_df[feature] = 0

        return answer_df

    def extract_answer(self, yesno: bool, response: str, question_entities: list = None, response_entities: list = None):
        if yesno: 
            # create dataframe with one row from answer, column called "Answer" filled with answer, and selected features columns filled with 0

            answer_df = self._init_answer_df(response)

            feature_model = Features(training=False, data=answer_df, pos_vectorizer=self.pos_vectorizer, bigram_vectorizer=self.bigram_vectorizer)
            data = feature_model.data.drop(columns=DROPPED_COLUMNS, errors="ignore")

            label = self.model.predict(data)
            
            return LABEL_DECODING[label[0]]
        else:
            # TODO: romnick
            ...
        

if __name__ == "__main__":
    model = pickle.load(open("yesno_classifier.pkl", "rb"))
    pos_vectorizer = pickle.load(open("pos_vectorizer.pkl", "rb"))   
    bigram_vectorizer = pickle.load(open("bigram_vectorizer.pkl", "rb"))

    extractor = AnswerExtractor(model=model, pos_vectorizer=pos_vectorizer, bigram_vectorizer=bigram_vectorizer)
    extractor.extract_answer(yesno=True, response="no, I am.")