import string

def fix_punc(text):
	return text.translate(str.maketrans('', '', string.punctuation.replace('-','')+'"'+"'"+'“'+'”'+"’"))