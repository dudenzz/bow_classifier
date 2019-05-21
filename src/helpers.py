def clean_csvdata(in_filename):
	iFile = open(in_filename)
	iFile.readline()
	current_text = ''
	current_category = -1
	list_of_positive_texts = []
	list_of_negative_texts = []
	for line in iFile:
		if line.startswith('1,') or line.startswith('0,'):
			if current_category != -1:
				if current_category == 1:
					list_of_positive_texts.append(current_text)
				if current_category == 0:
					list_of_negative_texts.append(current_text)
			current_text = line[2:].replace(',',' ').strip()
			current_category = int(line[0])
		else:
			current_text += ' ' + line.replace(',',' ').strip()

	if current_category == 1:
		list_of_positive_texts.append(current_text)
	if current_category == 0:
		list_of_negative_texts.append(current_text)

	iFile.close()
	oFilePos = open(in_filename + '.positive.csv', 'w+')
	oFileNeg = open(in_filename + '.negative.csv', 'w+')
	for text in list_of_positive_texts:
		oFilePos.write('1,' + text.strip() + '\n')
	for text in list_of_negative_texts:
		oFileNeg.write('0,' + text.strip() + '\n')
	oFilePos.close()
	oFileNeg.close()

def get_line_count(filename):
	i = 0
	f = open(filename)
	for line in f:
		i+=1
	f.close()
	return i

