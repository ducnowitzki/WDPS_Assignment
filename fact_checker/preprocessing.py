from entity.entity_linker import WikipediaEntity


class Features:
    def _get_synonyms(self, word: str) -> tuple([list, list]):
        synonyms = []
        try:
            # Finding similar words (synonyms)
            similar_words = self.word2vec_model.most_similar(word, topn=5)
            for similar_word, _ in similar_words:
                synonyms.append(similar_word)

        except KeyError:
            print(f"Word '{word}' not found in the vocabulary.")

        return synonyms

    def _process_question(self, question: str) -> tuple([list, list, list, list, bool]):
        # TODO: confirm order of these
        # pos tagging to get the subject, verb, adjective, object
        # stemmatization / lemmatization to get the root of the words
        # word2vec to get the synonyms
        ...

    def _get_sentences_from_wikipedia(self, entity: WikipediaEntity) -> list[str]:
        # only get sentences containing extracted entity (if it is entity)
        # TODO: post tagging, lemmatization

        ...

    def __init__(
        self,
        word2vec_model,
        question: str,
        question_entities: list[WikipediaEntity],
        extracted_answer: str | WikipediaEntity,
    ) -> None:
        self.word2vec_model = word2vec_model

        subjects, verbs, adjectives, objects, negated = self._process_question(question)
        self.subject = subjects
        self.verb = verbs
        self.adjective = adjectives
        self.object = objects
        self.negated = negated

        self.question_entities = question_entities
        self.question_entity_content: dict[str, list[str]] = {
            ent.object: self._get_sentences_from_wikipedia(ent)
            for ent in question_entities
        }

        self.extracted_answer = extracted_answer
