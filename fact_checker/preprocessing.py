from entity.entity_linker import WikipediaEntity
import nltk


def on_start_up():
    nltk.download("wordnet", quiet=True)


class Features:
    def _pos_tag(self, text: str) -> dict[str, str]:
        tokens = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        pos_dict = dict(pos_tags)
        return pos_dict

    def _lemmatize(self, word: str) -> str:
        return self.lemmatizer.lemmatize(word)

    def _get_synonyms(self, word: str) -> tuple([list, list]):
        synonyms = []
        try:
            # Finding similar words (synonyms)
            similar_words = self.word2vec_model.most_similar(word, topn=2)
            for similar_word, _ in similar_words:
                synonyms.append(similar_word)

        except KeyError:
            print(f"Synonym: '{word}' not found in the vocabulary.")

        return synonyms

    def _process_sentence(self, question: str) -> tuple([list, list, list, bool]):
        # TODO: confirm order of these
        # pos tagging to get the subject, verb, adjective, object
        # stemmatization / lemmatization to get the root of the words
        # word2vec to get the synonyms

        pos_tagging = self._pos_tag(question)
        print(pos_tagging)

        word_pool = set()

        for k, v in pos_tagging.items():
            # Only consider nouns, adjectives, verbs, and negations
            if v in [
                "NN",
                "NNS",
                "NNP",
                "NNPS",
                "VB",
                "VBD",
                "VBG",
                "VBN",
                "VBP",
                "VBZ",
                "JJ",
                "JJR",
                "JJS",
                "RB",
                "RBR",
                "RBS",
            ]:
                synonyms = self._get_synonyms(k)
                # add all synonyms to word pool
                word_pool.update(synonyms)
            if k in ["not", "n't", "no"]:
                word_pool.add(k)

        return word_pool

    def _get_sentences_from_wikipedia(self, entity: WikipediaEntity) -> list[str]:
        # only get sentences containing extracted entity (if it is entity)
        sentences = entity.abstract.split(".")

        word_pools = []
        for sentence in sentences:
            # TODO: check other versions/synonms of extracted answer
            if isinstance(self.extracted_answer, WikipediaEntity) and (
                self.extracted_answer.object not in sentence
            ):
                continue

            word_pools.append(self._process_sentence(sentence))

        return word_pools

    def __init__(
        self,
        word2vec_model,
        lemmatizer,
        question: str,
        question_entities: list[WikipediaEntity],
        extracted_answer: str | WikipediaEntity,
    ) -> None:
        self.word2vec_model = word2vec_model
        self.lemmatizer = lemmatizer
        self.extracted_answer = extracted_answer

        self.question_word_pool = self._process_sentence(question)
        print(self.question_word_pool)

        return
        self.question_entity_content: dict[str, list[str]] = {
            ent.object: self._get_sentences_from_wikipedia(ent)
            for ent in question_entities
        }
