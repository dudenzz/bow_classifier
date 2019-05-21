from wordmap import Wordmap
from nltk import word_tokenize
from helpers import clean_csvdata
from helpers import get_line_count
import argparse
import random

import sys

def create_wordmap(file, wordmap):
	lns = get_line_count(file)
	for i,line in enumerate(open(file,errors = 'ignore')):
		if i%1000 == 0:
			print('Processed %.2f%% of documents' % (100*i/float(lns)), end='\r')
		toks = word_tokenize(line.split(',')[1])
		wm.process_document(toks)
	print('Processed %i documents' % i, end = '\r\n')
def create_docvecs(file, wordmap, cat):
	dvs = []
	lns = get_line_count(file)
	for i,line in enumerate(open(file,errors = 'ignore')):
		if i%1000 == 0:
			print('Processed %.2f%% of documents' % (100*i/float(lns)), end='\r')
		dvs.append(wm.create_doc_vector(line.split(',')[1],cat))
	return dvs

#######PROCESSING THE ARGUMENTS

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-lwm', '--load_wm', dest='wordmapl_file', action='store',
                    help='Wordmap file. If specified, the wordmap will be loaded from file, it will NOT be created')
parser.add_argument('-wmc', '--create_new_wm', dest='wordmap_file', action='store',
                    help='Wordmap will be created. This arguments specifies the file for the wordmap to be saved in')
parser.add_argument('-d', '--data_file', dest='data_file', action='store',
                    help='A partially cleaned csv file with documents. Required.')

args =  parser.parse_args()

if not args.data_file:
	print('The data file is required, use: \n python3 convert.py -lwm wordmapfile -d datafile \n or \n python3 convert.py -wmc wordmapfile -d datafile')
	exit(0)
file = args.data_file


if(args.wordmapl_file):
	if(args.wordmap_file):
		print('What are you tring to do, load a wordmap or create a new one?')
		exit(0) 
	print('LOADING THE WORDMAP FILE')
	wm = Wordmap()
	wm.load(args.wordmapl_file)
else:
	if(args.wordmap_file):
		#######CLEANING THE DATA
		wm = Wordmap()
		print('CLEANING THE DATA')
		clean_csvdata(file)
		#######PREPARING WORDMAP
		print('PREPARING THE WORDMAP')
		print('PROCESSING THE POSITIVE(OFFENSIVE) DOCUMENTS')
		#create_wordmap('example',wm)
		create_wordmap(file + '.positive.csv',wm)
		print('PROCESSING THE NEGATIVE(NEUTRAL) DOCUMENTS')
		create_wordmap(file + '.negative.csv',wm)
		wm.clean('min_idf', 2)
		wm.clean('max_idf', 10)
		wm.clean('min_docs', 3)
		wm.clean('max_docs', 5000)
		wm.recalculate()
		wm.save(args.wordmap_file)



print('Creating document vectors for positive (offensive) observations')
pvecs = create_docvecs(file + '.positive.csv', wm,0)
print('Creating document vectors for negative (neutral) observations')
nvecs = create_docvecs(file + '.negative.csv', wm,1)

oFileTR = open('../data/train.data','w+')
oFileTST = open('../data/test.data','w+')

print('Saving the files')
for vec in pvecs:
	if len(vec) < 10: continue
	if random.random() > 0.7:
		oFileTST.write(vec + '\n')
	else:
		oFileTR.write(vec + '\n')
for vec in nvecs:
	if len(vec) < 10: continue
	if random.random() > 0.7:
		oFileTST.write(vec + '\n')
	else:
		oFileTR.write(vec + '\n')


oFileTR.close()
oFileTST.close()
