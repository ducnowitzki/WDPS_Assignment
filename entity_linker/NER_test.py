# pip install -U spacy
# python -m spacy download en_core_web_sm

# Imports
import spacy
import wikipediaapi

# Function to get named entities from text
def getNamedEntity(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Extract named entities
    named_entities = [ent.text for ent in doc.ents]

    return named_entities

# def getWikipedia(entities):
    

text = ("surely it is but many do not know this fact that Italy was not always called as Italy."
"Before Italy came into being in 1861, it had several names including Italian Kingdom,"
"Roman Empire and the Republic of Italy among others. If we start the chronicle back in time,"
"then Rome was the first name to which Romans were giving credit.,"
"Later this city became known as Caput Mundi” or the capital of the world...")
named_entities = getNamedEntity(text)
print(named_entities)