def string_drop_while(predicate,string):
	''' A string without the beginning matched by the predicate '''
	for (i,c) in enumerate(string):
		if not predicate(c):
			return string[i:]
	return ""

def string_take_while(predicate,string):
	''' A string with the beginning matched by the predicate '''
	for (i,c) in enumerate(string):
		if not predicate(c):
			return string[:i]
	return string

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
