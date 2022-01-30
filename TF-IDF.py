from nltk.tokenize import word_tokenize
import numpy as np
import pandas as pd

with open('DOI.txt') as f:
    lines = f.read()

text = lines
# Split text based on sentences (.)
text = text.split('.')

# List of sentences present in the text
sentences = []
# Create a set of candidate keywords
set_of_words = []

# Tokenize sentences in the text and appened them to sentences list
# Add words in the tokenized sentences to the set of words
for sentence in text:
    tokenized_sentence = [i.lower() for i in word_tokenize(sentence) if i.isalpha()]
    sentences.append(tokenized_sentence)
    for word in tokenized_sentence:
        if word not in set_of_words:
            set_of_words.append(word)

print(sentences)

set_of_words = set(set_of_words)
total_documents = len(sentences)

# Create a dictionary that stores the word and its position of in the document
idx_dict = {}
for counter, word in enumerate(set_of_words):
    idx_dict[word] = counter

# Count the frequency of words present in the set of candidate keywords present in the sentences
def count_dict(sentences):
    count_of_words = {}
    for word in set_of_words:
        count_of_words[word] = 0
        for sentence in sentences:
            if word in sentence:
                count_of_words[word] += 1
    return count_of_words

count_of_words = count_dict(sentences)

# Calculate the term frequnecy of words present in the set of words
def term_freq(document, word):
    total_documents = len(document)
    occurance = len([token for token in document if token == word])
    return occurance/total_documents

# Calculate the inverse document frequency of word present in the set of words
def inverse_document_freq(word):
    try:
        word_occurance = count_of_words[word] + 1
    except:
        word_occurance = 1 
    return np.log(total_documents / word_occurance)

# Caluclate the tf-idf of a sentence by multiplying the tf and idf of words present in the sentence
def tf_idf(sentence):
    tf_idf_vec =[0 for x in range(len(set_of_words))]
    for word in sentence:
        tf = term_freq(sentence, word)
        idf = inverse_document_freq(word)

        tf_idf_val = tf*idf
        temp = idx_dict[word]
        tf_idf_vec[temp] = tf_idf_val
    return tf_idf_vec

# Calculate the tfidf of sentences present in the text
vectors = []
for sentence in sentences:
    vect = tf_idf(sentence)
    vectors.append(vect)

words = []
for word in set_of_words:
    words.append(word)

# Print the results obtained in a df
df = pd.DataFrame(vectors, columns = words)
print(df)
