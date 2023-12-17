from gensim.models import KeyedVectors

# from ..entity.entity_linker import WikipediaEntity
# relative import
from entity.entity_linker import WikipediaEntity
from fact_checker.preprocessing import Features


class FactChecker:
    def __init__(self, word2vec_model_path: str) -> None:
        self.word2vec_model = KeyedVectors.load_word2vec_format(
            word2vec_model_path, binary=True
        )

    def check_fact(
        self,
        word2vec_model,
        # yesno: bool, maybe important?
        question: str,
        question_entities: list[WikipediaEntity],
        extracted_answer: str | WikipediaEntity,
    ) -> str:
        features = Features(
            word2vec_model,
            question,
            question_entities,
            extracted_answer,
        )
        combinations = [
            (subject, verb, object, adjective, entity)
            for subject in features.subject
            for verb in features.verb
            for object in features.object
            for adjective in features.adjective
        ]

        for entity, sentence in features.question_entity_content.values():
            # all combinations of subject, verb, object, adjective, (entity)
            # TODO: add none to certain list of not necessary

            # check if a sentence contains combination of subject, verb, object, adjective
            for subject, verb, object, adjective, entity in combinations:
                if (  # TODO: check if this should be correct
                    subject in sentence
                    and verb in sentence
                    and object in sentence
                    and adjective in sentence
                ):
                    return "correct"

        return "incorrect"
