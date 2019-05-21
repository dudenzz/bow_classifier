# Bag of words convereter

This repository consists of a simple document -> document vector converter
Entire converter was written in Python3
The converted set of document files is compatible with the LibSVM standard

Purpose of the repository:
   Contents of this repository are a supplementary resources for the offensive language filter project done for the student team project laboratories in Politechnika Poznańska.

Author:
   Jakub Dutkiewicz
    
Additional notes:
   Code is wrote from scratch in a literal sense. No ready methods are imported (such as document vectorisers from sklearn) are used. Only imported function, which completes a practical task is a word_tokenize from nltk. The code is supposed to represent the basic idea.

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
    
    - etc. for all parameters
    
    - if there are more token than the specified number (ntokens), the tokens are sorted in the "ctf times idf" order (descending) and only top ntokens tokens are selected, the rest is removed (not implemented)
     
    - it is advised to tinker with the parameters in the convert.py code or come up with new ones and define them in the clean function in the wordmap.py file
     
     
5. Saving the wordmap to the file (created wordmap can be used later)
    
CREATING DOCUMENT VECTORS AND TRAIN/TEST DATA
    
6. Creating document vectors for each vector

     - it is advised to tinker with the method of creating the document vectors

7. Shuffling the documents and splitting into train and test set

Usage (as some of the paths are hardcoded, you need to direct to the src directory first):


Use the following line if no wordmap file was created before or you want to create a new one(first use or new wordmap is to be created)

         python3 convert.py -wmc path_to_a_new_wordmap -d path_to_datafile

Use this line if wordmap file was previously created and should be used (reproduction of results)

         python3 convert.py -lwm path_to_existing_wordmap -d path_to_datafile




What to do once document vectors are created
 
   1. Download a liblinear tool
   2. Use train process to train the model
   3. Use predict process to test the model

Baseline accuracy: 85%



    - 
