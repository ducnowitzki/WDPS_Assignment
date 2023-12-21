# pip install -U spacy
# python -m spacy download en_core_web_sm

# Imports
from dataclasses import dataclass
import spacy
import requests
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
import string

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
from pprint import pprint

@dataclass
class WikipediaEntity:
    object: str
    wikipedia_page: str
    dbpedia_page: str
    abstract: str


def get_wikipedia_contains(entity):
    """
    Function to get candidates
    """
    endpoint_url = "http://dbpedia.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    ## Construct the SPARQL query
    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT DISTINCT ?entity ?label ?abstract ?dbpediaPage ?wikipediaPage
        WHERE {
            ?entity rdfs:label ?label .
            FILTER (LANG(?label) = "en" && regex(?label, "%s", "i"))
            ?entity dbo:abstract ?abstract FILTER(LANG(?abstract) = "en")
            ?entity foaf:isPrimaryTopicOf ?wikipediaPage .
        }
        LIMIT 10
        """ % entity

    # Set the query and request JSON format
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and process the results
    data = sparql.query().convert()

    candidates = [
        WikipediaEntity(
            object=result["label"]["value"],
            wikipedia_page=result["wikipediaPage"]["value"],
            dbpedia_page=result["entity"]["value"],
            abstract=result["abstract"]["value"],
        )
        for result in data["results"]["bindings"]
    ]

    if not candidates:
        return []
    else:
        return candidates

def get_wikipedia_exact(entity):
    """
    Function to get candidates
    """
    endpoint_url = "http://dbpedia.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)

    ## Construct the SPARQL query
    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT DISTINCT ?entity ?label ?abstract ?dbpediaPage ?wikipediaPage
        WHERE {
            ?entity rdfs:label ?label .
            FILTER (?label = "%s"@en)
            ?entity dbo:abstract ?abstract FILTER(LANG(?abstract) = "en")
            ?entity foaf:isPrimaryTopicOf ?wikipediaPage .
        }
        LIMIT 10
        """ % entity

    # Set the query and request JSON format
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and process the results
    data = sparql.query().convert()

    candidates = [
        WikipediaEntity(
            object=result["label"]["value"],
            wikipedia_page=result["wikipediaPage"]["value"],
            dbpedia_page=result["entity"]["value"],
            abstract=result["abstract"]["value"],
        )
        for result in data["results"]["bindings"]
    ]

    if not candidates:
        return []
    else:
        return candidates

def get_named_entities(text):
    """
    Fucnction to get all named enities
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Return only unique entities
    named_entities = {}
    # Extract named entities
    for entity in doc.ents:
        key = entity.text + entity.label_
        named_entities[key] = (clean_named_entity(entity.text), entity.label_)
    return list(named_entities.values())

def clean_named_entity(entity):
    # print(entity)
    entity = entity.translate(str.maketrans(" ", " ", string.punctuation))

    # remove "the_", maybe not optimal but sometimes necessary
    if entity.lower().startswith("the"):
        entity = entity[3:]

    return entity

import difflib

def choose_best_candidate(entity, candidates):
    if not candidates:
        return None
    
    else:
        # Store all candidates in list
        candidates_strings = [candidates[i].object for i in range(len(candidates))]
        candidates_strings = ['' if v is None else v for v in candidates_strings]

        # Use difflib to find the most similar string in the list
        similarity_scores = [difflib.SequenceMatcher(None, entity, s).ratio() for s in candidates_strings]
        print(similarity_scores)
        # Find the index of the string with the highest similarity score
        max_index = similarity_scores.index(max(similarity_scores))

        return candidates_strings[max_index]
    
text = (
        "surely it is but many do not know this fact that Italy was not always called as Italy."
        "Before Italy came into being in 1861, it had several names including Italian Kingdom,"
        "Roman Empire and the Republic of Italy among others. If we start the chronicle back in time,"
        "then Rome was the first name to which Romans were giving credit.,"
        "Later this city became known as Caput Mundi” or the capital of the world..."
    )

named_entities = get_named_entities(text)
# Testing linking
for i in range(len(named_entities)):
    entity = named_entities[i][0]
    label = named_entities[i][1]
    print(entity, label)

    candidates1 = get_wikipedia_contains(entity)
    candidates2 = get_wikipedia_exact(entity)

    print("candidates contains Function:")
    print([candidates1[i].object for i in range(len(candidates1))])
    print("candidates exact")
    print([candidates2[i].object for i in range(len(candidates2))])
    print('_______________________')



