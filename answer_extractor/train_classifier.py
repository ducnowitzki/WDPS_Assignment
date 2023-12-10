import pandas as pd
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
# train test splot
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from preprocessing import Features

def train_classifier():
    raw_data = pd.read_csv("questions_and_answers.csv")
    features = Features(raw_data)
    features.calculate_features()

    data = features.data

    # encode lables
    data["Type"] = data["Type"].map({"Yes/No": 0, "Entity": 1})

    drop = ["Unnamed: 0", "Index", "Input", "Answer", "Type"]
    X_train, X_test, y_train, y_test = train_test_split(data.drop(drop, axis=1), data["Type"], test_size=0.2, random_state=42)

    # train model
    #clf = DecisionTreeClassifier()
    clf = XGBClassifier()
    clf.fit(X_train, y_train)

    # test model, print accuracy, precision, recall, f1-score
    y_pred = clf.predict(X_test)
    print(clf.score(X_test, y_test))
    #print(classification_report(y_test, y_pred))


# def test_on_1_new_question():
#     answer = "There is no definitive answer to this question as it is a deep philosophical inquiry that has been debated by scholars, theologians, scientists, and many others. It is a question that is open to interpretation, and there is no one definitive answer. It is a question that is closely tied to the concept of purpose and meaning in life, which is a fundamental concern for many people. Some people may argue that we exist to survive and thrive as a species, to find happiness and fulfillment, to contribute to society in meaningful ways, or to achieve spiritual enlightenment or a connection with a higher power. Ultimately, the answer to this question may be different for each person, depending on their personal beliefs, values, and experiences."
#     type = "Entity"
#     data = pd.DataFrame({"Answer": [answer], "Type": [type]})
#     features = Features(data)
#     features.calculate_features()

#     data = features.data

#     # encode lables
#     data["Type"] = data["Type"].map({"Yes/No": 0, "Entity": 1})

#     drop = ["Unnamed: 0", "Index", "Input", "Answer"]
#     clf.predict(data.drop(drop, axis=1))

if __name__ == "__main__":
    train_classifier()
    #test_on_1_new_question()