def string_split_when(predicate,string):
	''' Two strings separated from the middle part matched by the predicate '''
	i1 = None
	for (i,c) in enumerate(string):
		if i1==None:
			if predicate(c):
				i1 = i
		else:
			if not predicate(c):
				return (string[:i1],string[i:])
	return (string if i1==None else string[:i1],"")

def string_char_translate(text,table):
	return ' '.join(map(lambda c: table[c] if c in table else c,text))
