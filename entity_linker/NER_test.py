# pip install -U spacy
# python -m spacy download en_core_web_sm

# Imports
import spacy
import requests

def getNamedEntity(text):
    '''
    Fucnction to get all named enities
    '''
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Extract named entities
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]

    return named_entities

def getWikipedia(entity):
    '''
    Function to get candidates
    '''
    # DBpedia SPARQL endpoint
    sparql_endpoint = "http://dbpedia.org/sparql"

    # SPARQL query to retrieve candidate selections for the named entity
    sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        
        SELECT ?entity ?label ?page ?type
        WHERE {{
            ?entity rdfs:label ?label.
            ?entity foaf:isPrimaryTopicOf ?page.
            ?entity rdf:type ?type.
            FILTER (
                CONTAINS(LCASE(?label), LCASE("{entity}"))
            )
        }}
        LIMIT 1000
    """

    # Send SPARQL query to DBpedia
    response = requests.get(sparql_endpoint, params={'query': sparql_query, 'format': 'json'})
    data = response.json()

    # Extract candidate selections and their Wikipedia pages from the results
    candidates = [
        {'entity': result['entity']['value'], 
         'label': result['label']['value'], 
         'page': result['page']['value'],
         'type': result['type']['value']}
        for result in data['results']['bindings']
    ]

    return candidates

    

"""
_____________________
TESTING FUNCTUINS
_____________________
"""
# Testing named entities
text = ("surely it is but many do not know this fact that Italy was not always called as Italy."
"Before Italy came into being in 1861, it had several names including Italian Kingdom,"
"Roman Empire and the Republic of Italy among others. If we start the chronicle back in time,"
"then Rome was the first name to which Romans were giving credit.,"
"Later this city became known as Caput Mundi” or the capital of the world...")
named_entities = getNamedEntity(text)
print(named_entities[0][0], named_entities[0][1])

# Testing linking
entity = named_entities[0][0]
label = named_entities[0][1]
candidates = getWikipedia(entity)
for candidate in candidates:
    print(f"Wikipedia Page: {candidate['page']}")
    print(f"type: {candidate['type']}")
    print(f"Entity: {candidate['entity']}")
    print("-" * 30)