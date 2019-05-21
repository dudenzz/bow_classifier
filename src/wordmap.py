from nltk import word_tokenize
import numpy as np

class Wordmap:
	def __init__(self):
		self.wordmap = {}
		self.cterm_frequency = []
		self.doc_frequency = []
		self.reverse_wordmap = {}
		self.id = 0
		self.nodocs = 0
		self.notoks = 0
		self.size = 0
	def process_document(self,doc_tokens):
		processed_ids = []
		self.nodocs += 1
		for token in doc_tokens:
			self.notoks += 1
			token = token.lower()
			if token not in self.reverse_wordmap:
				self.wordmap[self.id] = token
				self.reverse_wordmap[token] = self.id
				self.cterm_frequency.append(0)
				self.doc_frequency.append(0)
				self.size += 1
				token_id = self.id
				self.id += 1
			else:
				token_id = self.reverse_wordmap[token]
			self.cterm_frequency[token_id] += 1
			if token_id not in processed_ids:
				self.doc_frequency[token_id] += 1
				processed_ids.append(token_id)
	def get_idf(self,token):
		return np.log(self.nodocs/self.doc_frequency[self.reverse_wordmap[token]])
	def get_ctf(self, token):
		return self.cterm_frequency[self.reverse_wordmap[token]]/float(self.notoks)
	def clean(self, metric, value):
		i = 0
		print('There are % i words in the wordmap, cleaning the data with [%s,%f]' % (self.size, metric, value))
		if metric not in  ['min_idf','max_idf','min_ctf','max_ctf','min_docs','max_docs']:
			raise NameError('Unknown metric %s' % metric)
		for word in self.reverse_wordmap:
			if i % 1000 == 0:
				print('Processed %f words ' % (i / float(self.size)), end = '\r')
			i += 1
			if metric == 'min_idf':
				idf = self.get_idf(word)
				if idf < value:
					delete = 1
				else:
					delete = 0
			if metric == 'max_idf':
				idf = self.get_idf(word)
				if idf > value:
					delete = 1
				else:
					delete = 0
			if metric == 'min_ctf':
				ctf = self.get_ctf(word)
				if ctf < value:
					delete = 1
				else:
					delete = 0
			if metric == 'max_ctf':
				ctf = self.get_ctf(word)
				if ctf > value:
					delete = 1
				else:
					delete = 0
			if metric == 'min_docs':
				df = self.doc_frequency[self.reverse_wordmap[word]]
				if df < value:
					delete = 1
				else:
					delete = 0
			if metric == 'max_docs':
				df = self.doc_frequency[self.reverse_wordmap[word]]
				if df > value:
					delete = 1
				else:
					delete = 0
			if delete == 1:
				if self.reverse_wordmap[word] in self.wordmap:
					del self.wordmap[self.reverse_wordmap[word]]
		rm_values = self.reverse_wordmap.values()
		old_toks = self.size
		self.size = 0
		for id in self.wordmap:
			self.size += 1
		print('Removed %i tokens, %i tokens remain' % (old_toks - self.size, self.size))
	def recalculate(self):
		print('Recalculating the wordmap')
		self.reverse_wordmap = {}
		docfreq = []
		ctf = []
		nwmap = {}
		idgen = 0
		for id in self.wordmap:
			nwmap[idgen] = self.wordmap[id]
			self.reverse_wordmap[self.wordmap[id]] = idgen
			docfreq.append(self.doc_frequency[id])
			ctf.append(self.cterm_frequency[id])
			idgen += 1
		self.cterm_frequency = ctf
		self.doc_frequency = docfreq
		self.wordmap = nwmap
	def save(self, file):
		oFile = open(file, 'w+')
		oFile.write(str(self.notoks) + ' ' + str(self.nodocs) + ' ' + str(self.size) + '\n')
		for id in self.wordmap:
			oFile.write(self.wordmap[id] + ' ' + str(id) + ' ' + str(self.cterm_frequency[id]) + ' ' + str(self.doc_frequency[id]) + '\n')
		oFile.close()
	def load(self, file):
		self.wordmap = {}
		self.cterm_frequency = {}
		self.doc_frequency = {}
		self.reverse_wordmap = {}
		self.id = 0
		self.nodocs = 0
		self.notoks = 0
		self.size = 0
		f = open(file)
		toks = f.readline().split()
		self.notoks = int(toks[0])
		self.nodocs = int(toks[1])
		self.size = int(toks[2])
		tempdf = {}
		tempctf = {}
		for line in f:
			[word, id, ctf, df] = line.split()
			self.wordmap[int(id)] = word
			self.reverse_wordmap[word] = int(id)
			self.id = int(id)
			tempdf[int(id)] = int(ctf)
			tempctf[int(id)] = int(df)
		self.doc_frequency = [0 for i in range(len(tempdf))]
		self.cterm_frequency = [0 for i in range(len(tempctf))]
		for i in range(len(tempdf)):
			self.doc_frequency[i] = tempdf[i]
			self.cterm_frequency[i] = tempctf[i]
		f.close()
	def create_doc_vector(self, tokens, category):
		doc_vec = [0 for i in range(self.size)]
		for tok in tokens:
			tok = tok.lower()
			if tok in self.reverse_wordmap:
				doc_vec[self.reverse_wordmap[tok]] += 1
		doc_vec_sps = str(category) + ' '
		for i,val in enumerate(doc_vec):
			if val == 0: continue
			doc_vec_sps += str(i+1) + ':' + str(val) + ' '
		return doc_vec_sps
	def __iter__(self):
		list = [self.wordmap[id] + ' : id = ' + str(id) + '  idf=' + str(self.get_idf(self.wordmap[id])) + ' ctf=' + str(self.get_ctf(self.wordmap[id])) for id in self.wordmap]
		return list.__iter__()

