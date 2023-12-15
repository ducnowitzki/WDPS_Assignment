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
    """
    Fucnction to get all named enities
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Extract named entities
    named_entities = [ent.text for ent in doc.ents]
    named_entities_labels = [ent.label_ for ent in doc.ents]
    return named_entities, named_entities_labels


def namedEntityCleaner(entity):
    entity = entity.replace(" ", "_")
    entity = entity.replace(",", "")
    entity = entity.replace(".", "")

    return entity


def getWikipedia(entity):
    """
    Function to get candidates
    """

    entity = namedEntityCleaner(entity)
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
        print(f"Error: Unable to decode JSON response for {entity}")
        return None

    candidates = [
        {
            "object": result["object"]["value"],
            "wikipedia_page": result["page"]["value"],
            "dbpedia_page": f"http://dbpedia.org/resource/{entity}",
            "abstract": result["abstract"]["value"],
        }
        for result in data["results"]["bindings"]
    ]

    # Extract candidate selections and their Wikipedia pages from the results
    # candidates = [
    #     {'object': result['object']['value']}
    #     for result in data['results']['bindings']
    # ]
    if not candidates:
        return None
    else:
        return candidates


"""
_____________________
TESTING FUNCTUINS
_____________________
"""
# # Testing named entities
# text = ("surely it is but many do not know this fact that Italy was not always called as Italy."
# "Before Italy came into being in 1861, it had several names including Italian Kingdom,"
# "Roman Empire and the Republic of Italy among others. If we start the chronicle back in time,"
# "then Rome was the first name to which Romans were giving credit.,"
# "Later this city became known as Caput Mundi” or the capital of the world...")
# named_entities = getNamedEntity(text)
# # Testing linking
# for i in range(len(named_entities)):
#     entity = named_entities[i][0]
#     label = named_entities[i][1]

#     print(entity)

#     candidates = getWikipedia(entity)
#     pprint(candidates)
#     print(candidates[0]['abstract'])
#     # dbpedia_links = [candidates[j]["entity"] for j in range(len(candidates))]
#     # print(dbpedia_links)
#     # result = rank_dbpedia_pages(entity, dbpedia_links)

#     # # Print the ranked pages
#     # for rank, (page, similarity) in enumerate(result, start=1):
#     #     print(f"Rank {rank}: {page} (Similarity: {similarity})")
#     # for candidate in candidates:
#     #     print(f"Wikipedia Page: {candidate['page']}")
#     #     # print(f"type: {candidate['type']}")
#     #     # print(f"Entity: {candidate['entity']}")
#     #     print("-" * 30)
