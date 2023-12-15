import pandas as pd

romnick = pd.read_csv("questions_and_answers_romnick.csv")

keye = pd.read_csv("questions_and_answers_keye.csv")

# take line 0-499 from keye and 500-2000 from romnick
keye = keye.iloc[:500]
romnick = romnick.iloc[500:2000]

# merge keye and romnick
merged = pd.concat([keye, romnick])

# replace "n " with "n" in "Label"
merged["Label"] = merged["Label"].str.replace("n ", "n")

# print columns

# remove columns: Unnamed: 0, Column 1
merged = merged.drop(columns=["Unnamed: 0", "Column1"])

# Index from 0
merged["Index"] = merged.index

merged.to_csv("questions_and_answers_labeled.csv", index=False)
