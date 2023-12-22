import pickle
from time import time

import pandas as pd
from answer_extractor.answer_extractor import AnswerExtractor
from answer_extractor.preprocessing import on_start_up as answer_extractor_on_start_up
from entity.entity_linker import WikipediaEntity, get_wikipedia_entities
from fact_checker.fact_checker import FactChecker
from fact_checker.preprocessing import on_start_up as fact_checker_on_start_up
from question_classifier.question_classifier import QuestionClassifier
from nltk.stem import WordNetLemmatizer

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


QUESTION_FILE_PATH = "sample_input.txt"
SEPARATOR = "\t"
# SEPARATOR = "    "


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


def evaluate(evaluation_df, application_output):
    # calculate accuracy, precision, recall, f1
    label_decoding_data = {"Correct": 1, "Incorrect": 0}
    label_decoding = {"correct": 1, "incorrect": 0}

    evaluation_df["Correctness"] = evaluation_df["Correctness"].map(label_decoding_data)
    evaluation_df["Application Output"] = application_output
    evaluation_df["Application Output"] = evaluation_df["Application Output"].map(
        label_decoding
    )

    accuracy = accuracy_score(
        evaluation_df["Correctness"], evaluation_df["Application Output"]
    )
    precision = precision_score(
        evaluation_df["Correctness"], evaluation_df["Application Output"]
    )
    recall = recall_score(
        evaluation_df["Correctness"], evaluation_df["Application Output"]
    )
    f1 = f1_score(evaluation_df["Correctness"], evaluation_df["Application Output"])

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1:", f1)


def main():
    print("INFO: Starting...")

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

    evaluation_df = pd.read_csv("evaluation_data.csv")
    application_output = []

    for _, row in evaluation_df.iterrows():
        question_id = row["Index"]
        question = row["Input"]

        print(question_id, question)

        # LLM
        print(question_id, "LLM: Generating answer...")
        output = row["Answer"]
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

        application_output.append(correctness)

    print("Metrics for whole evaluation data:")
    evaluate(evaluation_df, application_output)

    print("Metrics for Yes/No questions:")
    evaluate(
        evaluation_df[evaluation_df["Type"] == "Yes/No"],
        application_output[:20],
    )

    print("Metrics for entity questions:")
    evaluate(
        evaluation_df[evaluation_df["Type"] == "Entity"],
        application_output[20:],
    )


if __name__ == "__main__":
    main()
