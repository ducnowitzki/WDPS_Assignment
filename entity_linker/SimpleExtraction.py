import spacy

# Load the spaCy English NER model
nlp = spacy.load("en_core_web_sm")


# Extracting yes/no or entities using keyword matching
def extract_information(text):
    doc = nlp(text)
    for token in doc:
        if token.text.lower() in ["yes", "indeed", "certainly"]:
            return "yes"
        if token.text.lower() in ["no", "not"]:
            return "no"
        if token.ent_type_:
            return token.text
    return None


# Extracting information from each answer
file_path = "answers.txt"
with open(file_path, "r", encoding="utf-8") as file:
    # Extracting information from each line in the file
    for i, line in enumerate(file):
        result = extract_information(line.strip())
        print(f"Line {i + 1}: {result}")
