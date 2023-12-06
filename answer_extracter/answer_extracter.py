import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import csv


file = open("../delphi/sample_questions_output.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()
answers = []
for _ in data:
    answers.append(_[3])
answers.pop(0)
print(answers)
corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first document?',
]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(answers)
vectorizer.get_feature_names_out()
print(X.toarray())
vectorizer2 = CountVectorizer(analyzer='word', ngram_range=(2, 2))
X2 = vectorizer2.fit_transform(answers)
vectorizer2.get_feature_names_out()
