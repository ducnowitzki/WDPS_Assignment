# pip install -U spacy
# python -m spacy download en_core_web_sm

# Imports
from dataclasses import dataclass
import spacy
import requests
import requests

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
from pprint import pprint


@dataclass
class WikipediaEntity:
    object: str
    wikipedia_page: str
    dbpedia_page: str
    abstract: str


def clean_named_entity(entity):
    # print(entity)
    entity = entity.replace(" ", "_")
    entity = entity.replace(",", "")
    entity = entity.replace(".", "")

    # Mt. Everest -> Mt_Everest which does not return an entity

    # TODO:
    # remove "the_", maybe not optimal but sometimes necessary
    if entity.lower().startswith("the_"):
        entity = entity[4:]

    # print(entity)

    return entity


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
    return named_entities.values()


def get_wikipedia(entity):
    """
    Function to get candidates
    """

    print(entity)

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
        
        SELECT ?object ?label ?page ?type ?abstract
        WHERE {{ 
            dbr:{entity} rdfs:label ?object.
            dbr:{entity} foaf:isPrimaryTopicOf ?page.
            dbr:{entity} dbo:abstract ?abstract.
            FILTER(lang(?object) ='en')
            FILTER(lang(?abstract) ='en') 
            }}
        LIMIT 10
        """

    # Send SPARQL query to DBpedia
    response = requests.get(
        sparql_endpoint, params={"query": sparql_query, "format": "json"}
    )
    try:
        # Try to load JSON data if available
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        # Handle the case where the response is not valid JSON
        raise Exception(f"Error: Unable to decode JSON response for {entity}")

    candidates = [
        WikipediaEntity(
            object=result["object"]["value"],
            wikipedia_page=result["page"]["value"],
            dbpedia_page=f"http://dbpedia.org/resource/{entity}",
            abstract=result["abstract"]["value"],
        )
        for result in data["results"]["bindings"]
    ]

    # print(len(candidates))
    # print(candidates[0].object)

    # Extract candidate selections and their Wikipedia pages from the results
    # candidates = [
    #     {'object': result['object']['value']}
    #     for result in data['results']['bindings']
    # ]
    if not candidates:
        return []
    else:
        return candidates


def choose_best_candidate(candidates: WikipediaEntity, label: str):
    # TODO
    ...


def get_wikipedia_entities(text):
    named_entities = get_named_entities(text)

    wiki_entities = []
    for ent, label in named_entities:
        print(ent)
        candidates = get_wikipedia(ent)
        if len(candidates) > 0:
            wiki_entities.append(
                candidates[0]
                if len(candidates) == 1
                else choose_best_candidate(candidates, label)
            )

    return wiki_entities


# Testing
if __name__ == "__main__":
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

        print(entity)

        candidates = get_wikipedia(entity)
        pprint(candidates)
        print(candidates[0]["abstract"])
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
