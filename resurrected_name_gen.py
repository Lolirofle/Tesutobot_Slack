import random

# Potential next character for each character
combinations = {
	'q': set('wylujöåarhneioäv'),
	'f': set('fyluöåarheioä'),
	'p': set('pylujöåarheioä'),
	'g': set('wgylujöåarhneioäzv'),
	'y': set('qwfpglrstdhnzxvbkm'),
	'l': set('luöåaheioä'),
	'u': set('qwfpgyljrstdhnzxvbkm'),
	'j': set('yuöåaeioä'),
	'ö': set('fpglrstdhnzxvbkm'),
	'å': set('fpgljrstdhnzxcvbkm'),
	'a': set('qfpgljrstdnizxcvbkm'),
	'r': set('yuöåarheioä'),
	's': set('wyluöåasthneioäcvm'),
	't': set('wyuöåartheioäv'),
	'd': set('wyuöåardheioäv'),
	'h': set('yujöåaeioä'),
	'n': set('yuöåahneioä'),
	'e': set('wfpgljrstdnizxcvbkm'),
	'i': set('qwfpgljrstdnezxcvbkm'),
	'o': set('qwfpgylujrstdhnzxcvbkm'),
	'ä': set('pgylrstdnvkm'),
	'z': set('wluöåathneioäv'),
	'x': set('uaeio'),
	'c': set('wyuarheioc'),
	'v': set('yuöåarheioä'),
	'b': set('yuöåarheioäb'),
	'k': set('yluöåarhneioäv'),
	'm': set('yujöåahneioäm'),
	'w': set('uaheio'),
}

# Other data
initial    = set('wfpgylujarstdhneiocvbkm')
vowels     = set('aoueiyåäö')
consonants = set('qwrtpsdfghjklzxcvbnm')

def generate_name(length=6,exclude=set()):
	try:
		# First character
		name = random.choice(list(initial.difference(exclude)))

		# Second character (Only if the first is a consonant, and this is then a vowel)
		if name[0] in consonants:
			name+= random.choice(list(vowels.difference(exclude)))

		# State for number of consonants after each other
		consonant_count = 0

		# Generates pseudo-randomly new letters
		for i in range(len(name),length):
			# States
			previous_c = name[-1]
			c = ''

			# Potential character for the next position
			potential_cs = combinations[previous_c].difference(exclude)

			# Disallow a specific number of consonants after each other
			if consonant_count==2:
				potential_cs = potential_cs.difference(consonants)

			# Check if there are any potential characters at all
			if potential_cs:
				# Choose a random character from the list of potential characters
				c = random.choice(list(potential_cs))

				# Handle the consonant count
				if c in consonants:
					consonant_count+= 1
				else:
					consonant_count = 0
			else:
				break

			# Append the character to the name
			name+= c
		return name
	except:
		return ""
