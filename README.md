# Keyword-Extraction

<b>
   Term Frequency Inverse Term Frequency Implementation
</b>

<hr>

In TF-IDF, a score is computed for each word to signify its importance in the piece of text. We first vectorize the document by using a bag-of-words. 
Then, to represent a piece of text, count the number of times each word appears in the document and is put in the corresponding vector entry. 

Algorithm for TF-IDF: 

Terminology: t – term (word), d – document, N – count of the corpus (total document set). 

Term Frequency of a word in the document is dependent on the word t and the document d. The final value of the normalized tf will be in the range [0,1]. 

<p align="center">
  <img width="500" src="tf formula.png">
</p>

Document Frequency measures the importance of documents in the whole set of the corpus. df is the count of occurrences of term t in the document set N. 

<p align="center">
  <img width="500" src="df formula.png">
</p>

Inverse Document Frequency (idf) is the inverse of the document frequency which measures the informativeness of term t. 
idf will be low for most words such as stop words because they are present in most documents, and N/df will give a low value for that word. 

<p align="center">
  <img width="500" src="idf formula.png">
</p>

However, when the value of N is large i.e., we have a large corpus, the value of idf(t) explodes. 
To dampen its effect, we compute the log of the idf. Moreover, since the occurrence of some words may be 0 in the corpus, the df will be 0. 
Since we can’t divide by 0, in order to smoothen out idf, we add 1 to df(t). 

<p align="center">
  <img width="500" src="modified idf formula.png">
</p>

Finally, we get the tf-idf (t, d) by multiplying the values of tf(t, d) and idf(t).

<p align="center">
  <img width="500" src="tfidf formula.png">
</p>

Analysis of the Results of TF-IDF: The model is more accurate than a simple word frequency model, since it incorporates the inverse document frequency of a word. 
The model’s results are more accurate when the number of documents is large since it has a larger collection of words for its set and dictionary. 
However, TF-IDF takes a lot of space since it uses a dictionary to count words in a piece of text and a set to store all unique words. 
TF-IDF can be improved by assigning weights to words based on their position so that it can calculate the words which rely on high term frequency evenly.  

<hr>

<b>
   Graph Based Ranking Algorithms
</b>

<hr>

Graph based ranking algorithms decide the importance of a vertex within a graph, based on global information drawn from the graph. 
It works on the principal of voting. When a vertex links to another through an edge, it casts a vote for the other. 
The more the number of votes for a vertex, the more the importance of the vertex. 
The importance of the vertex casting the vote also determines the weight given to the vote. 

Formally, let G=(V,E) be a directed graph with set of vertices V and set of edges E, where E is a subset of V×V. 
For a given vertex Vi, let In(Vi) be the set of vertices that point to it (predecessors), and let Out(Vi) be the set of vertices that vertex 
Vi points to (successors). The score of a Vi can be calculated as: 

<p align="center">
  <img width="500" src="page rank formula.png">
</p>

where d is a damping factor, usually set as 0.85, which integrates into the model the probability of jumping from a given vertex to another 
random vertex in the graph. In graph-based approaches, the words present in a piece of text are represented as nodes in a graph and the edges 
connecting these nodes are decided based on a co-occurrence sliding window that traverses the entire document. Edges are added between all 
the nodes present in any particular sliding window and the graph formed is unweighted and undirected in nature. Next, we iterate through the 
graph until convergence and get the most common nodes.

<hr>

<b>
   Text Rank Implementation
</b>

<hr>

Text Rank: In Text Rank, a piece of text is tokenized and annotated with part of speech tags – a preprocessing step that is required to 
enable application of syntactic filters. All lexical units (words) that pass the syntactic filters are added to the graph and an edge is 
added between those lexical units, as nodes, that co-occur within a window of n words, that create an undirected and unweighted graph is 
constructed. Next, a score is calculated for each vertex and the PageRank algorithm is applied for many iterations until it converges. 
Lastly, the vertices are sorted in reverse order of their score and the top T vertices are extracted. 

Analysis of the Results of Text Rank: The text rank algorithm gives results similar to those in the research paper and online implementations 
for window size = 5 and by applying a syntactic filter to only consider nouns and propositions. Moreover, a larger window decreases the accuracy 
of the results since all words in the text receive a higher score, while a smaller window fails to capture the importance of side-by-side words 
in the same context.

Text Rank is efficient for fast and lightweight extraction of keywords. It can be applied on documents, articles, and any piece of text to get 
the underlying keywords of the piece of text that are representative of the document. It is also completely unsupervised and draws information 
only from text itself. However, text rank still cannot achieve the same results as that of supervised models, since a limitation is imposed on 
the number of keywords to be selected, which creates a smaller dataset. Text Rank can be improved by modifying the algorithm to consider the 
position of the words in a piece of text or by considering a set of documents instead of a single one to extract global information. 
