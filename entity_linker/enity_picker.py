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
                    q_abstract_ent = getNamedEntity(q_entity_page[0]["abstract"])[0]
                    a_abstact_ent = getNamedEntity(a_entity_page[0]["abstract"])[0]

                    q_entity_ngrams = set(ngrams(q_abstract_ent, 1))
                    a_entity_ngrams = set(ngrams(a_abstact_ent, 1))

                    similarity = jaccard_similarity(q_entity_ngrams, a_entity_ngrams)
                    cumulative_similarity += similarity
            print(a_entity)
            print(cumulative_similarity)
            if cumulative_similarity > max_similarity:
                max_similarity = cumulative_similarity
                related_entity = a_entity

    return related_entity


# Example usage
q_txt = """The capital city of Brazil is..."""
a_txt = """Yes. It's a common misconception that the capital city of Brazil is Rio de Janeiro (which is the largest city). The official and actual capital is Brasilia, in central Brazil. There are also a number of other capitals, depending on what you mean by 'capital'. In the past, the government has moved its capital from place to place, with Rio being one of them, but Brasília (Brazilian-Portuguese for "City of Brazil") was created in 1960 as the new capital.What is the capital city of Brazil?The capital city of Brazil is Brasilia.Where is the capital city of Brazil?Brasilia, Federal District, BrazilWhen did Brazil become a country?In 1822 when they declared themselves independent from PortugalWho is the current president of Brazil?Dilma Rousseff is President of Brazil as of May 2011.What are the main industries in Brazil?The major industry in Brazil is agriculture, and a large portion of their economy depends on it. The manufacturing and service sector also make up a large part of the economy.Is Rio de Janeiro the capital"""
q_clean_txt = q_txt.translate(str.maketrans(" ", " ", string.punctuation))
a_clean_txt = a_txt.translate(str.maketrans(" ", " ", string.punctuation))
result = most_related_entity(
    getNamedEntity(q_clean_txt)[0], getNamedEntity(a_clean_txt)[0]
)
print("Most related entity:", result)

# print(getWikipedia(getNamedEntity(q_txt)[0][0]))
