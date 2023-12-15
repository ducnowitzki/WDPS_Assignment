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
from answer_extractor.train_classifier import train_classifier

from delphi.llm import LLM


QUESTION_FILE_PATH = "sample_input.txt"
SEPARATOR = "    "

# Download the model and add to the directory
# E.g. take one from her: https://huggingface.co/TheBloke/Llama-2-7B-GGUF#provided-files
MODEL_PATH = os.path.abspath('delphi/llama-2-7b.Q3_K_M.gguf')

def init():
    on_start_up()

def get_llm_input():
    # return a tuple of (question_id, question), each line looks like this: question_id<TAB>question
    lines = open(QUESTION_FILE_PATH, "r").readlines()
    lines = [line[:-1] for line in lines]
    return [tuple(line.split(SEPARATOR)) for line in lines]

def clean_answer(answer: str):
    return answer.strip().replace('\n', '').replace('\r', '').replace('\t', '').replace('▁', ' ')


def main():
    # LLM
    llm_input = get_llm_input()
    llm = LLM(MODEL_PATH)

    # Question classifier

    # Answer extractor
    yesno__model = pickle.load(open("answer_extractor/yesno_classifier.pkl", "rb"))
    pos_vectorizer = pickle.load(open("answer_extractor/pos_vectorizer.pkl", "rb"))
    bigram_vectorizer = pickle.load(open("answer_extractor/bigram_vectorizer.pkl", "rb")) 
    answer_extractor = AnswerExtractor(model=yesno__model, pos_vectorizer=pos_vectorizer, bigram_vectorizer=bigram_vectorizer)
    
    # Fact checker

    fact_checked_df = pd.DataFrame(columns=["question_id", "extracted_answer", "correctness", "entities"])

    for question_id, question in llm_input:
        output = llm.generate_answer(question)
        response = clean_answer(output)
        
        # Entity linker
        # TODO:

        # Question classifier
        # TODO:

        extracted_answer = answer_extractor.extract_answer(yesno=True, response=response)
        print("Extracted answer:", extracted_answer)

        # Fact checker
        # TODO:
        break
        


if __name__ == "__main__":
    train_classifier()
    # init()
    # main()