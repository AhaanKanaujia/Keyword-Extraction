from collections import OrderedDict
import numpy as np
from spacy.lang.en.stop_words import STOP_WORDS

import en_core_web_lg
nlp = en_core_web_lg.load()

class TextRank():
    # constructor
    def __init__(self):
        self.d = 0.85 # damping coefficient
        self.min_diff = 1e-5 # convergence threshold
        self.iterations = 100 # number of iterations for graph traversal algorithm
        self.node_weight = None # weight associated with a keyword

    # create a set of stopwords, that will not be considered as keywords
    def set_stopwords(self, stopwords):
        for word in STOP_WORDS.union(set(stopwords)):
            temp = nlp.vocab[word]
            temp.is_stop = True
    
    # create a list of the sentences in the text
    # words in the sentence are filtered to discard stop words
    # words in the sentence are passed through syntactic filter of candidate_pos
    def sentence_segment(self, text, candidate_pos, lower):
        sentences = []
        for sentence in text.sents:
            selected_words = []
            for token in sentence:
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences
    
    # create a dictionary to store occurance of words in sentences
    # vocab contains all candidate keywords and their position in the text
    # counter becomes the number of candidate keywords in the text
    def get_vocab(self, sentences):
        vocab = OrderedDict()
        counter = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = counter
                    counter += 1
        return vocab

    # create word pairs from windows of length window_size in sentences
    # a sliding window of length window_size is used to extract word pairs
    def get_token_pairs(self, window_size, sentences):
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i + 1, i + window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs
    
    # symmetrize matrix
    def get_symmetric_matrix(self, matrix):
        return matrix + matrix.T - np.diag(matrix.diagonal())

    # construct a similarity matrix using word pairs and the vocab dictionary created
    def get_similarity_matrix(self, vocab, token_pairs):
        vocab_size = len(vocab)
        # initialize similarity matrix
        similarity_matrix = np.zeros((vocab_size, vocab_size), dtype = 'float')
        # get word1 and word2 from every word_pair in token_pairs
        for word1, word2 in token_pairs:
            # i and j is the position of word 1 and 2 in the dictionary vocab
            i, j = vocab[word1], vocab[word2]
            # fill in the position [i][j] as 1
            similarity_matrix[i][j] = 1
        # symmetrize the similarity matrix
        similarity_matrix = self.get_symmetric_matrix(similarity_matrix)
        # calculate normalization factor of the similarity matrix
        normalized = np.sum(similarity_matrix, axis = 0)
        # normalize the similarity matrix
        similarity_matrix_normalized = np.divide(similarity_matrix, normalized, where=normalized != 0)
        return similarity_matrix_normalized

    # function to return the keywords in a piece of text based on the page rank score associated with each token 
    def get_keywords(self, number = 25):
        # get the weight associated with each word
        node_weight = OrderedDict(sorted(self.node_weight.items(), key = lambda temp: temp[1], reverse = True))
        # print out the key value pairs for each word as the score associated with each word
        for counter, (key, value) in enumerate(node_weight.items()):
            print(key + ': ' + str(value))
            # once we reach the number of keywords to extract, we break out of the loop
            if counter > number:
                break
        
    # main token analysis algorithm, that uses google's page rank algorithm
    def analyze(self, text, candidate_pos = ['NOUN', 'PROPN'], window_size = 5, lower = False, stopwords = list()):
        # create the set of stopwords
        self.set_stopwords(stopwords)
        # tokenize the text into document
        document = nlp(text)
        # get the sentences present in the document
        sentences = self.sentence_segment(document, candidate_pos, lower)
        # get the vocab(dictionary) of the text
        vocab = self.get_vocab(sentences)
        # get token pairs present in the sentences based on the window size
        token_pairs = self.get_token_pairs(window_size, sentences)
        # normalize the similarity matrix
        normalized_matrix = self.get_similarity_matrix(vocab, token_pairs)
        # create page rank vector to apply page rank algorithm to
        page_rank_vector = np.array([0] * len(vocab))
        
        # Page Rank Algorithm (used by Google)
        prev_page_rank_vector = 0
        for i in range(self.iterations):
            page_rank_vector = (1 - self.d) + self.d * np.dot(normalized_matrix, page_rank_vector)
            if abs(prev_page_rank_vector - sum(page_rank_vector)) < self.min_diff:
                break
            else:
                prev_page_rank_vector = sum(page_rank_vector)

        # Set node weights associated with tokens and store it in node_weight dictionary
        node_weight = dict()
        for word, idx in vocab.items():
            node_weight[word] = page_rank_vector[idx]
        self.node_weight = node_weight

with open('DOI.txt') as f:
    lines = f.read()

text = lines
tr = TextRank()
sentences = tr.sentence_segment(nlp(text), candidate_pos=['NOUN', 'PROPN'], lower = False)
print(sentences)
vocab = tr.get_vocab(sentences)
print(vocab)
window_size = 5
token_pairs = tr.get_token_pairs(window_size, sentences)
print(token_pairs)
similarity_matrix = tr.get_similarity_matrix(vocab, token_pairs)
print(similarity_matrix)
tr.analyze(text, candidate_pos = ['NOUN', 'PROPN'], window_size = 5, lower = False)
tr.get_keywords(10)
