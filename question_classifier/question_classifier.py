import pickle
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

from question_classifier.preprocessing import Features

# from preprocessing import Features


DROPPED_COLUMNS = [
    "Index",
    "Input",
    "Input_no_pronouns",
    "Input_lowercase",
    "Type",
]

LABEL_DECODING = {0: "Yes/No", 1: "Entity"}


def train_classifier():
    questions_df = pd.read_csv("questions.csv")
    features = Features(training=True, data=questions_df)
    features.calculate_features()

    data = features.data

    data["Type"] = data["Type"].map({"Yes/No": 0, "Entity": 1})

    data = data.dropna(subset=["Type"])

    print(data.head())

    X_train, X_test, y_train, y_test = train_test_split(
        data.drop(DROPPED_COLUMNS, axis=1),
        data["Type"],
        test_size=0.05,
        random_state=42,
    )

    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print(classification_report(y_test, y_pred))

    print(sorted(zip(clf.feature_importances_, X_train.columns), reverse=True)[:20])

    # pickle model
    pickle.dump(clf, open("question_classifier.pkl", "wb"))


class QuestionClassifier:
    def __init__(self, model, pos_vectorizer):
        self.model = model
        self.pos_vectorizer = pos_vectorizer

    def classify_question(self, question: str):
        # create dataframe with one row from answer, column called "Answer" filled with answer, and selected features columns filled with 0

        question_df = pd.DataFrame({"Input": [question]})

        feature_model = Features(
            training=False,
            data=question_df,
            pos_vectorizer=self.pos_vectorizer,
        )

        feature_model.calculate_features()
        data = feature_model.data.drop(columns=DROPPED_COLUMNS, errors="ignore")

        label = self.model.predict(data)

        return LABEL_DECODING[label[0]]


if __name__ == "__main__":
    # train_classifier()
    model = pickle.load(open("question_classifier.pkl", "rb"))
    pos_vectorizer = pickle.load(open("question_pos_vectorizer.pkl", "rb"))
    question_classifier = QuestionClassifier(model, pos_vectorizer)
    print(question_classifier.classify_question("obviously, will italy be a country?"))
