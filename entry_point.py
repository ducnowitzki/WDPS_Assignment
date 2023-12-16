# WORKFLOW
# for every line in question set:
#   1. delphi: query llm with question --> get answer
#   2. question_classifier: classify question type
#   3. answer_extractor: extract answer:
#       if yes/no question: classify the answer
#       if entity question: return most plausible answer
#   4. fact checker:
#       Yes/No:
#       Entity:

import os
import pickle
import pandas as pd
from answer_extractor.answer_extractor import AnswerExtractor
from answer_extractor.preprocessing import on_start_up
from time import time

from delphi.llm import LLM
from entity.entity_linker import get_wikipedia_entities


QUESTION_FILE_PATH = "sample_input.txt"
SEPARATOR = "    "

# Download the model and add to the directory
# E.g. take one from her: https://huggingface.co/TheBloke/Llama-2-7B-GGUF#provided-files
MODEL_PATH = os.path.abspath("delphi/llama-2-7b.Q3_K_M.gguf")


def init():
    on_start_up()


def get_llm_input():
    # return a tuple of (question_id, question), each line looks like this: question_id<TAB>question
    lines = open(QUESTION_FILE_PATH, "r").readlines()
    lines = [line[:-1] for line in lines]
    return [tuple(line.split(SEPARATOR)) for line in lines]


def clean_answer(answer: str):
    return (
        answer.strip()
        .replace("\n", "")
        .replace("\r", "")
        .replace("\t", "")
        .replace("▁", " ")
    )


def write_to_output_file(file_name, question_id: str, response_dict: dict):
    with open(file_name, "a") as f:
        response_string = f"{question_id}{SEPARATOR}R\"{response_dict['response']}\"\n"
        response_string += (
            f"{question_id}{SEPARATOR}A\"{response_dict['extracted_answer']}\"\n"
        )
        response_string += (
            f"{question_id}{SEPARATOR}C\"{response_dict['correctness']}\"\n"
        )
        for ent in response_dict["wiki_entities"]:
            response_string += f'{question_id}{SEPARATOR}E"{ent}"\n'

        f.write(response_string)


def main():
    # LLM
    llm_input = get_llm_input()
    llm = LLM(MODEL_PATH)

    # Question classifier

    # Answer extractor
    yesno__model = pickle.load(open("answer_extractor/yesno_classifier.pkl", "rb"))
    pos_vectorizer = pickle.load(open("answer_extractor/pos_vectorizer.pkl", "rb"))
    bigram_vectorizer = pickle.load(
        open("answer_extractor/bigram_vectorizer.pkl", "rb")
    )
    answer_extractor = AnswerExtractor(
        model=yesno__model,
        pos_vectorizer=pos_vectorizer,
        bigram_vectorizer=bigram_vectorizer,
    )

    output_file_name = "group2_fact_checked_reponses_" + str(int(time())) + ".txt"

    # Fact checker
    # TODO:

    fact_checked_df = pd.DataFrame(
        columns=[
            "question_id",
            "response",
            "extracted_answer",
            "correctness",
            "wiki_entities",
        ]
    )

    for question_id, question in llm_input:
        # output = llm.generate_answer(question)
        # response = clean_answer(output)

        response = "surely it is not, because you can see its top from Nepal. so it must be shorter than EverestIt is possible to walk down from the top of Mt. Everest, although it is probably a very unpleasant experience if you don't have lots of practice. A good pair of hiking boots and some training goes a long way.Do they use bicycles in Nepal? I need to know where to go on my trip next summer!Where do you get the money for your trips? Do you like to go around the world alone? Are you looking forward to meeting people from other countries? What are your thoughts about it?How do we protect our planet earth, if there is no place in this earth that hasn't been affected by pollution or destruction? If not, how can we save our beautiful world and all its wonderful wild life and animals?"

        # Question classifier
        # TODO:

        extracted_answer = answer_extractor.extract_answer(
            yesno=True, response=response
        )

        # Entity linker
        question_wiki_entities = get_wikipedia_entities(question)
        response_wiki_entities = get_wikipedia_entities(response)

        # Fact checker
        # TODO:
        correctness = "correct"

        # Add to dataframe
        response_dict = {
            "question_id": question_id,
            "response": response,
            "extracted_answer": extracted_answer,
            "correctness": correctness,
            "wiki_entities": [ent.wikipedia_page for ent in response_wiki_entities],
        }

        write_to_output_file(output_file_name, question_id, response_dict)

        break


if __name__ == "__main__":
    init()
    main()
