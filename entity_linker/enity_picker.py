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

                if q_entity_page is not None:
                    q_entity_ngrams = set(ngrams(q_entity_page[0]['dbpedia_page'].split('/'), 1))
                    a_entity_ngrams = set(ngrams(a_entity_page[0]['dbpedia_page'].split('/'), 1))

                    similarity = jaccard_similarity(q_entity_ngrams, a_entity_ngrams)
                    cumulative_similarity += similarity

            if cumulative_similarity > max_similarity:
                max_similarity = cumulative_similarity
                related_entity = a_entity

    return related_entity

# Example usage
q_txt = '''Who is the director of Inception?'''
a_txt = '''Christopher Nolan hopefully not the same person who directed the dreadful 'The Prestige', a film that I found to be extremely disappointing.Why do you say "hopefully"? Nolan's career isn't going downhill or anything, so why hope he doesn't ruin something?Well for one thing, 'The Dark Knight' is one of the worst movies ever made, and 'Inception' has a lot to live up to. And I don't like the idea of Nolan doing a film set in the world of magic, because his approach to it will be so clinical, so technical...Well you have a point there. But then again, Nolan is an amazing visual director and has been pretty consistent with that side of things.I still haven't seen "The Dark Knight". I thought Batman Begins was cool, though, especially the Joker. But I don't like it when films try to be realistic and then have a magician character in them. It always seems so out of place...What about 'Harry Potter'?That series is full of magic, but there isn't really any focus on magic as an'''
q_clean_txt = q_txt.translate(str.maketrans(' ', ' ', string.punctuation))
a_clean_txt = a_txt.translate(str.maketrans(' ', ' ', string.punctuation))
result = most_related_entity(getNamedEntity(q_clean_txt)[0], getNamedEntity(a_clean_txt)[0])
print("Most related entity:", result)

print(q_clean_txt)

