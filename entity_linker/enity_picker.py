from SPARQLWrapper import SPARQLWrapper, JSON
from nltk import ngrams
from NER_test import getWikipedia, getNamedEntity
import string

def jaccard_similarity(set1, set2):
    # Function to calculate Jaccard similarity between two sets
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0.0

def most_related_entity(question_entities, answer_entities):
    # Function to find the most related entity in the answer to entities in the question
    max_similarity = 0.0
    related_entity = None

    for a_entity in answer_entities:
        a_entity_page = getWikipedia(a_entity)

        if a_entity_page is not None:
            cumulative_similarity = 0.0

            for q_entity in question_entities:
                q_entity_page = getWikipedia(q_entity)

                if q_entity_page is not None and a_entity != q_entity:
                    q_entity_ngrams = set(ngrams(q_entity_page[0]['dbpedia_page'].split('/'), 1))
                    a_entity_ngrams = set(ngrams(a_entity_page[0]['dbpedia_page'].split('/'), 1))

                    similarity = jaccard_similarity(q_entity_ngrams, a_entity_ngrams)
                    cumulative_similarity += similarity

            if cumulative_similarity > max_similarity:
                max_similarity = cumulative_similarity
                related_entity = a_entity

    return related_entity

# Example usage
q_txt = '''Who painted 'Guernica'?'''
a_txt = '''everybody knows. It was Picasso. What they don’t know, however, is that the work was a collaboration between many artists; or rather, it was an act of solidarity with Spain by many artists all over the world. It began as a reaction against the bombing of Gernika in 1937 and ended up as one of the most powerful images of war ever made.The story begins in 1936 when, under Franco, the Spanish Civil War broke out. On 26 April 1937, the Republican-held town of Guernica in northern Spain was bombed by German and Italian aircraft. The attack lasted for hours and destroyed everything in its path. It was a horrific war crime that shocked the world: 100 people were killed immediately and an estimated 500 injured; 80% of the town was reduced to rubble.The bombing took place during the Spanish Civil War, which broke out in July 1936 after a failed coup led by army generals and right-wing politicians against the democratically elected government. The war pitted Franco’s Nationalists – who were supported by Naz'''
q_clean_txt = q_txt.translate(str.maketrans(' ', ' ', string.punctuation))
a_clean_txt = a_txt.translate(str.maketrans(' ', ' ', string.punctuation))
result = most_related_entity(getNamedEntity(q_clean_txt)[0], getNamedEntity(a_clean_txt)[0])
print("Most related entity:", result)

print(getNamedEntity(a_txt)[0])

