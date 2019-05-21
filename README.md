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

1. data cleaning:

    - crlf removal
    
    - "," removal
    
    - split positive and negative documents into two files
    
2. tokenizing

    - each document is tokenized with nltk word_tokenize method
    
    - each token is put to lowercase
    
3. creating a wordmap

    - each token is processed (at this moment it is put to lowercase)
    
    - an identifier is assigned to each new unique token
    
    - the corpus term frequency and inverse document frequency are calculated for each token
    
