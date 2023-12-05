# pip install -U spacy
# python -m spacy download en_core_web_sm

# Imports
import spacy
import requests
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pprint import pprint


def getNamedEntity(text):
    '''
    Fucnction to get all named enities
    '''
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Extract named entities
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]

    return named_entities

def namedEntityCleaner(entities):
    print("")

def getWikipedia(entity):
    '''
    Function to get candidates
    '''
    # DBpedia SPARQL endpoint
    sparql_endpoint = "http://dbpedia.org/sparql"

    # SPARQL query to retrieve candidate selections for the named entity
    # ?entity = <http://dbpedia.org/resource/{named_entity}>
    # CONTAINS(STR(?entity), "{entity}")
    sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbpedia: <http://dbpedia.org/resource/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT ?object ?label ?page ?type
        WHERE {{ 
            dbr:'{entity}' rdfs:label ?object.
            dbr:'{entity}' foaf:isPrimaryTopicOf ?page.
            }}
        LIMIT 10
        """

    # Send SPARQL query to DBpedia
    response = requests.get(sparql_endpoint, params={'query': sparql_query, 'format': 'json'})
    candidates = response.json()

    # Extract candidate selections and their Wikipedia pages from the results
    # candidates = [
    #     {'object': result['object']['value']}
    #     for result in data['results']['bindings']
    # ]

    return candidates

# def get_dbpedia_page_content(entity_uri):
#     # Function to get the content of a DBpedia page
#     # You may need to adjust this based on the actual structure of the DBpedia endpoint
#     dbpedia_endpoint = "http://dbpedia.org/data/" + entity_uri.split('/')[-1] + ".json"
#     response = requests.get(dbpedia_endpoint)
    
#     if response.status_code == 200:
#         data = response.json()
#         if data and entity_uri in data:
#             # Assume the content is in the 'abstract' field for simplicity
#             return data[entity_uri]['http://dbpedia.org/ontology/abstract'][0]['value']
    
#     return ""

# def rank_dbpedia_pages(named_entity, candidate_pages):
#     # Function to rank DBpedia pages using context-dependent features
    
#     # Step 1: Get the context (e.g., abstract) for the named entity
#     context = get_dbpedia_page_content(named_entity)
    
#     if not context:
#         print(f"Error: Unable to retrieve context for {named_entity}")
#         return
    
#     # Step 2: Extract features from the context and candidate pages
#     vectorizer = TfidfVectorizer()
#     features = vectorizer.fit_transform([context] + [get_dbpedia_page_content(page) for page in candidate_pages])
    
#     # Step 3: Calculate cosine similarity between the context and each candidate page
#     similarities = cosine_similarity(features[0], features[1:]).flatten()
    
#     # Step 4: Rank candidate pages based on similarity
#     ranked_pages = [(page, similarity) for page, similarity in zip(candidate_pages, similarities)]
#     ranked_pages.sort(key=lambda x: x[1], reverse=True)
    
#     return ranked_pages

    

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

# Testing linking
for i in range(1):#len(named_entities)):
    entity = named_entities[i][0]
    label = named_entities[i][1]

    print(entity)
    
    candidates = getWikipedia(entity)
    pprint(candidates)
    # dbpedia_links = [candidates[j]["entity"] for j in range(len(candidates))]
    # print(dbpedia_links)
    # result = rank_dbpedia_pages(entity, dbpedia_links)

    # # Print the ranked pages
    # for rank, (page, similarity) in enumerate(result, start=1):
    #     print(f"Rank {rank}: {page} (Similarity: {similarity})")
    # for candidate in candidates:
    #     print(f"Wikipedia Page: {candidate['page']}")
    #     # print(f"type: {candidate['type']}")
    #     # print(f"Entity: {candidate['entity']}")
    #     print("-" * 30)