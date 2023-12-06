import numpy as np

class BoW:
    def __init__(self):
        # Here is where we keep all words. A set for faster lookup
        self.all_words = set()
        # Two dictionaries to map word to index and back. This helps 'encoding' and 'decoding' a BoW
        self.word_to_idx= {}
        self.idx_to_word= {}
        # The total number of words is just kept to aid starting the numpy array size, but can be inferred from all_words set.
        self.total_words = 0

    def fit(self, document):
        """
        Fits the BoW using the data. This is used to help the BoW learn the vocabulary and word indexes.
        """
        # Just checking if its empty or not
        if type(document) != list or len(document) < 1 or type(document[0]) != str:
            raise TypeError("You must pass a list of strings for fitting.")
        list_of_sentences = document
        # Now, we go through each sentence.
        for sentence in list_of_sentences:
            # Naive tokenizing. Just splitting sentence is usually not enought, but we keep it simple here.
            words = [word.lower() for word in sentence.split()]
            for word in words:
                # Add all words. Since its a set, there won't be duplicates.
                self.all_words.add(word)
        for idx, word in enumerate(self.all_words):
            # Set the mapping indexes.
            self.word_to_idx[word] = idx
            self.idx_to_word[idx] = word
        # Set the vocab size.
        self.total_words = len(self.all_words)

    def transform(self, data):
        """
        Transforms the input data into the BoW model format.
        """
        # Check that the model is fit.
        if self.total_words == 0:
            raise AttributeError("You must first fit the data.")
        if type(data) == str:
            # We call the private helper function _transform_single for each input. If there's only a single sentence, we transform it here and return a single <vector>.
            transformed = self._transform_single(data.split())
        elif type(data) == list and type(data[0]) == str:
            # Now, if we have more than one sentence (a document), we'll make a matrix of stacked sentence arrays. For that we go through each sentence.
            # Create empty matrix.
            transformed = np.empty((len(data), self.total_words))
            # Iterate over all sentences - this can be parallelized.
            for row, sentence in enumerate(data):
                # Substitute each row by the sentence BoW.
                transformed[row] = self._transform_single(sentence.split())
        else:
            raise TypeError("You must pass either a string or list of strings for transformation.")
        return transformed

    def fit_transform(self, data):
        """
        Does both fitting and transforming at once.
        """
        self.fit(data)
        return self.transform(data)

    def _transform_single(self, list_of_words):
        """
        Auxiliary method for simplifying the process of transforming. Here is where the "magic" happens.
        """
        # Start a zero filled array with the size of the vocabulary.
        transformed = np.zeros(self.total_words)
        for word in list_of_words:
            # Iterate over sentence words checking if they are in the vocabulary.
            if word in self.all_words:
                word_idx = self.word_to_idx[word]
                # Change the value of that specific index, by increasing the value.
                transformed[word_idx] += 1
        return transformed