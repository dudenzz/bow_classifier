# Bag of words convereter

This repository consists of a simple document -> document vector converter
Entire converter was written in Python3
The converted set of document files is compatible with the LibSVM standard

Required packages:
  nltk
  numpy
Required data:
  a semi cleaned csv file

Description of a semi cleaned csv file:
  the documents in the csv file start with either "1," or "0," (positive and negative observations)
  there are no lines in a document which start with either "1," or "0," besides the initial line
  
The converter performs the following operations (in that order):

CREATING A WORDMAP WHICH CONSISTS OF WORD-IDENTIFIER PAIRS

1. data cleaning:

    - crlf removal
    
    - "," removal
    
    - split positive and negative documents into two files
    
2. tokenizing

    - each document is tokenized with nltk word_tokenize method
    
    - each token is put to lowercase
    
3. creating the wordmap

    - each token is processed (at this moment it is put to lowercase)
    
    - an identifier is assigned to each new unique token
    
    - the corpus term frequency (ctf) and inverse document frequency (idf) are calculated for each token
    
4. cleaning the wordmap

    - if a token didn't achieve mininimal required idf (min_idf) it is removed
    - if a token didn't achieve minimal ctf (min_ctf) it is removed
    - if a token didn't appear in minimal number of documents (min_docs)
    - if a token exceeded idf maximum (max_idf) it is removed
    - if there are more token than the specified number (ntokens), the tokens are sorted in the $ctf \cdot idf$ order (descending) and only top $ntokens$ tokens are selected
    
