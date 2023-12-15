import pickle
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# from xgboost import XGBClassifier

from answer_extractor.preprocessing import Features

DROPPED_COLUMNS = [
    "Index",
    "Input",
    "Answer",
    "Answer_lowercase",
    "Answer_without_stop_words",
    "Type",
    "Label",
]
LABEL_ENCODING = {"y": 0, "n": 1}


def train_classifier():
    # on_start_up()

    raw_data = pd.read_csv("answer_extractor/questions_and_answers_labeled.csv")
    raw_data = raw_data.dropna(subset=["Type"])

    features = Features(training=True, data=raw_data)
    features.calculate_features()

    data = features.data

    # take only rows where type is Yes/No
    # and Label is either y or n
    data = data[(data["Label"].isin(["y", "n"]))]
    print(data.shape)

    # encode lables
    # data["Type"] = data["Type"].map({"Yes/No": 0, "Entity": 1})
    data["Label"] = data["Label"].map(LABEL_ENCODING)

    # print row where type is nan
    # print(data[data["Type"].isna()])
    # print(data.shape)
    # remove rows where type is nan
    data = data.dropna(subset=["Type"])

    # print column names that contain [,] or <
    # print(data.columns[data.columns.str.contains("[<>]")])
    ## remove columns that contain [,] or <
    # data = data.drop(columns=data.columns[data.columns.str.contains("[")])
    # data = data.drop(columns=data.columns[data.columns.str.contains("<")])
    # data = data.drop(columns=data.columns[data.columns.str.contains(">")])
    # data = data.drop(columns=data.columns[data.columns.str.contains("]")])

    X_train, X_test, y_train, y_test = train_test_split(
        data.drop(DROPPED_COLUMNS, axis=1),
        data["Label"],
        test_size=0.05,
        random_state=42,
    )

    # train model
    clf = DecisionTreeClassifier()
    # clf = XGBClassifier()
    clf.fit(X_train, y_train)

    # test model, print accuracy, precision, recall, f1-score
    y_pred = clf.predict(X_test)

    # print precision, recall, f1-score, AUC score, Average precision score, G mean
    print(classification_report(y_test, y_pred))

    # print top 20 features
    print(sorted(zip(clf.feature_importances_, X_train.columns), reverse=True)[:30])

    # pickle model
    pickle.dump(clf, open("yesno_classifier.pkl", "wb"))


if __name__ == "__main__":
    train_classifier()
