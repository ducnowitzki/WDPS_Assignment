import os
import pickle
from time import time
from answer_extractor.answer_extractor import AnswerExtractor
from answer_extractor.preprocessing import on_start_up as answer_extractor_on_start_up
from delphi.llm import LLM
from entity.entity_linker import WikipediaEntity, get_wikipedia_entities
from fact_checker.fact_checker import FactChecker
from fact_checker.preprocessing import on_start_up as fact_checker_on_start_up
from question_classifier.question_classifier import QuestionClassifier
from nltk.stem import WordNetLemmatizer


QUESTION_FILE_PATH = "sample_input.txt"
SEPARATOR = "\t"
# SEPARATOR = "    "

# Download the model and add to the directory
# E.g. take one from her: https://huggingface.co/TheBloke/Llama-2-7B-GGUF#provided-files
MODEL_PATH = os.path.abspath("delphi/llama-2-7b.Q3_K_M.gguf")

# can be downloaded from here: https://www.kaggle.com/datasets/leadbest/googlenewsvectorsnegative300
WORD2VEC_MODEL_PATH = None
# WORD2VEC_MODEL_PATH = os.path.abspath("fact_checker/GoogleNews-vectors-negative300.bin")
WORD2VEC_ENABLED = False


def init():
    print("INFO: Initializing NLTK...")
    answer_extractor_on_start_up()
    fact_checker_on_start_up()


def get_llm_input():
    lines = open(QUESTION_FILE_PATH, "r").readlines()
    lines = [line[:-1] for line in lines]
    lines = [line for line in lines if line]
    return [tuple(line.split(SEPARATOR)) for line in lines]


def clean_answer(answer: str):
    return (
        answer.strip()
        .replace("\n", "")
        .replace("\r", "")
        .replace("\t", "")
        # .replace("▁", " ")
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
    print("INFO: Starting...")

    # LLM
    print("INFO: LLM: Loading model...")
    llm_input = get_llm_input()
    llm = LLM(MODEL_PATH)

    # Question classifier
    print("INFO: Question classifier: Loading models...")
    question_model = pickle.load(
        open("question_classifier/question_classifier.pkl", "rb")
    )
    question_pos_vectorizer = pickle.load(
        open("question_classifier/question_pos_vectorizer.pkl", "rb")
    )
    question_classifier = QuestionClassifier(
        model=question_model, pos_vectorizer=question_pos_vectorizer
    )

    # Answer extractor
    print("INFO: Answer extractor: Loading models...")
    yesno__model = pickle.load(open("answer_extractor/yesno_classifier.pkl", "rb"))
    yesno_pos_vectorizer = pickle.load(
        open("answer_extractor/yesno_pos_vectorizer.pkl", "rb")
    )
    yesno_bigram_vectorizer = pickle.load(
        open("answer_extractor/yesno_bigram_vectorizer.pkl", "rb")
    )
    answer_extractor = AnswerExtractor(
        model=yesno__model,
        pos_vectorizer=yesno_pos_vectorizer,
        bigram_vectorizer=yesno_bigram_vectorizer,
    )

    output_file_name = (
        "output/group2_fact_checked_reponses_" + str(int(time())) + ".txt"
    )

    # Fact checker
    print("INFO: Fact checker: Loading models...")
    lemmatizer = WordNetLemmatizer()
    fact_checker = FactChecker(WORD2VEC_MODEL_PATH, WORD2VEC_ENABLED, lemmatizer)

    for question_id, question in llm_input:
        print(question_id, question)

        # LLM
        # print(question_id, "LLM: Generating answer...")
        # output = llm.generate_answer(question)
        output = "yes"
        response = clean_answer(output)

        # Question classifier
        print(question_id, "Question Classifier: Classifying question...")
        question_type = question_classifier.classify_question(question)
        print(question_id, "Question Type:", question_type)

        # Entity linker
        print(question_id, "Entity Linker: Getting entities from question...")
        question_wiki_entities = get_wikipedia_entities(question)
        print(
            question_id,
            "Linked entities:",
            [ent.object for ent in question_wiki_entities]
            if question_wiki_entities
            else "None",
        )
        print(question_id, "Entity Linker: Getting entities from response...")
        response_wiki_entities = get_wikipedia_entities(response)
        print(
            question_id,
            "Linked entities:",
            [ent.object for ent in response_wiki_entities]
            if response_wiki_entities
            else "None",
        )

        # Answer extractor
        print(question_id, "Answer extractor: Extracting answer...")
        extracted_answer = answer_extractor.extract_answer(
            yesno=True if question_type == "Yes/No" else False,
            response=response,
            question_entities=question_wiki_entities,
            response_entities=response_wiki_entities,
        )
        print(
            question_id,
            "Extracted answer:",
            extracted_answer.object
            if isinstance(extracted_answer, WikipediaEntity)
            else extracted_answer,
        )

        # Fact checker
        correctness = fact_checker.check_fact(
            question=question,
            question_entities=question_wiki_entities,
            extracted_answer=extracted_answer,
        )
        print(question_id, "Correctness:", correctness)

        response_dict = {
            "question_id": question_id,
            "response": output,
            "extracted_answer": extracted_answer
            if question_type == "Yes/No"
            else extracted_answer.wikipedia_page,
            "correctness": correctness,
            "wiki_entities": [ent.wikipedia_page for ent in response_wiki_entities],
        }

        write_to_output_file(output_file_name, question_id, response_dict)


if __name__ == "__main__":
    init()
    main()
