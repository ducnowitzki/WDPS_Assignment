from gensim.models import KeyedVectors

# from ..entity.entity_linker import WikipediaEntity
# relative import
from entity.entity_linker import WikipediaEntity
from fact_checker.preprocessing import Features


class FactChecker:
    def __init__(self, word2vec_model_path: str, word2vec_enabled, lemmatizer) -> None:
        if word2vec_model_path:
            self.word2vec_model = KeyedVectors.load_word2vec_format(
                word2vec_model_path, binary=True
            )

        self.word2vec_enabled = word2vec_enabled

        self.lemmatizer = lemmatizer

    def check_fact(
        self,
        # yesno: bool, maybe important?
        question: str,
        question_entities: list[WikipediaEntity],
        extracted_answer: str | WikipediaEntity,
    ) -> str:
        features = Features(
            self.word2vec_model,
            self.word2vec_enabled,
            self.lemmatizer,
            question,
            question_entities,
            extracted_answer,
        )

        for entity, word_pool_list in features.question_entity_content.items():
            for word_pool in word_pool_list:
                if features.question_word_pool.issubset(word_pool):
                    print(
                        "Correct entity: ", entity, "Entity sentence pool: ", word_pool
                    )
                    return "correct"

        return "incorrect"
