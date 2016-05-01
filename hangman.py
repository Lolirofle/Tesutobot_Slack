import sys

ascii_art = (
	"========     \n"
	" |   \||     \n"
	" _    ||     \n"
	"/ \   ||     \n"
	"\ /   ||     \n"
	"/|\   ||     \n"
	" |    ||     \n"
	"/ \   ||     \n"
	"    //  \\\\   \n"
	"~~~//~~~~\\\\",

	"========     \n"
	" |   \||     \n"
	" _    ||     \n"
	"/ \   ||     \n"
	"\ /   ||     \n"
	"/|\   ||     \n"
	" |    ||     \n"
	"/ \   ||     \n"
	"    //  \\\\   \n"
	"   //    \\\\",

	"========     \n"
	" |   \||     \n"
	" _    ||     \n"
	"/ \   ||     \n"
	"\ /   ||     \n"
	" |\   ||     \n"
	" |    ||     \n"
	"/ \   ||     \n"
	"    //  \\\\   \n"
	"   //    \\\\",

	"========     \n"
	" |   \||     \n"
	" _    ||     \n"
	"/ \   ||     \n"
	"\ /   ||     \n"
	" |    ||     \n"
	" |    ||     \n"
	"/ \   ||     \n"
	"    //  \\\\   \n"
	"   //    \\\\",

	"========     \n"
	" |   \||     \n"
	" _    ||     \n"
	"/ \   ||     \n"
	"\ /   ||     \n"
	" |    ||     \n"
	" |    ||     \n"
	"  \   ||     \n"
	"    //  \\\\   \n"
	"   //    \\\\",

	"========     \n"
	" |   \||     \n"
	" _    ||     \n"
	"/ \   ||     \n"
	"\ /   ||     \n"
	" |    ||     \n"
	" |    ||     \n"
	"      ||     \n"
	"    //  \\\\   \n"
	"   //    \\\\",

	"========     \n"
	" |   \||     \n"
	" _    ||     \n"
	"/ \   ||     \n"
	"\ /   ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"    //  \\\\   \n"
	"   //    \\\\",

	"========     \n"
	" |   \||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"    //  \\\\   \n"
	"   //    \\\\",

	"========     \n"
	"     \||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"    //  \\\\   \n"
	"   //    \\\\",

	"========     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"    //  \\\\   \n"
	"   //    \\\\",

	"             \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"      ||     \n"
	"    //  \\\\   \n"
	"   //    \\\\",

	"             \n"
	"             \n"
	"             \n"
	"             \n"
	"             \n"
	"             \n"
	"             \n"
	"             \n"
	"    //  \\\\   \n"
	"   //    \\\\",

	"             \n"
	"             \n"
	"             \n"
	"             \n"
	"             \n"
	"             \n"
	"             \n"
	"             \n"
	"             \n"
	"             ",
)


class Hangman(object):
	def __init__(self,word,lives=len(ascii_art),valid_char_predicate=str.isalpha):
		self.initial_lives = lives
		self.word = word
		self.word_chars = set(word)

		# Initialized later:
		#self.gamestate: str
		#self.guesses: set[char]
		#self.lives: int
		#self.unrevealed: int

		self.restart()

	def __str__(self):
		''' Default string representation of the game '''
		return "%s\n%s (%s)" % (
			ascii_art[int(self.lives/self.initial_lives * (len(ascii_art)-1))],
			self.gamestate if self.unrevealed==0 else ' '.join(self.gamestate),
			','.join(self.guesses)
		)

	def build_gamestate(self):# TODO: An alternative may be to use a list of chars. Strings are immutable, but lists are not
		self.gamestate = ''
		self.unrevealed = 0
		for c in self.word:# I sure hope this is a hashed O(1) operation
			if c in self.guesses or not self.valid_char_predicate(c):
				self.gamestate+= c
			else:
				self.gamestate+= '_'
				self.unrevealed+= 1

	def guess_char(self,c):# TODO: Invalid characters
		'''
		Guess using a character,
		adding it to the guess list and revealing the character in the gamestate if the word contained it.
		This counts as one guess if the character was not already guessed.

		Returns a boolean for whether the guess was correct or None if the letter already have been guessed.
		Raises a GameOverError when loses (lives<=0).
		Raises a InvalidCharError when the given character was invalid.
		'''

		if not self.valid_char_predicate(c):
			raise InvalidCharError(c)
		elif c in self.guesses:
			return None
		else:
			self.guesses.add(c)
			if c in self.word_chars:
				self.build_gamestate()
				return True
			else:
				self.lives-= 1
				if self.lives<=0:
					raise GameOverError
				return False

	def guess_str(self,s):
		'''
		Guess using a whole string,
		adding all characters if the word contained the exact string given and reveals them in the gamestate.
		This always counts as one guess.

		Returns a boolean for whether the guess was correct.
		Raises a GameOverError when loses (lives<=0).
		'''
		if self.word.find(s)>=0:
			for c in s:
				self.guesses.add(c)
			self.build_gamestate()
			return True
		else:
			self.lives-= 1
			if self.lives<=0:
				raise GameOverError
			return False

	def guess_chars(self,s):
		'''
		Guess using a list of characters (e.g. a string),
		adding the ones the word contained to the guess list and revealing them in the gamestate.
		Each character that has not already been guessed counts as one guess.

		Returns a map which maps the given characters to True, False or None (See `guess_char`)
		Raises a GameOverError when loses (lives<=0).
		Raises a InvalidCharError when one or more of the the given characters was invalid.
		'''

		mapping = {}
		for c in s:
			if not self.valid_char_predicate(c):
				raise InvalidCharError(c)
			elif c in self.guesses:
				mapping[c] = None
			else:
				self.guesses.add(c)
				if c in self.word_chars:
					mapping[c] = True
				else:
					self.lives-= 1
					mapping[c] = False
		self.build_gamestate()
		if self.lives<=0:
			raise GameOverError
		return mapping

	def restart(self):
		''' Resets the lives and guesses, using the same word '''
		self.lives = self.initial_lives
		self.guesses = set()
		self.build_gamestate()

	def reveal(self):
		''' Reveals the gamestate, thus completes the game (without adding the missing characters to the guess list) '''
		self.gamestate = self.word

	def is_complete(self):
		''' Returns whether the game is completed (all characters are revealed => ..with a victory) '''
		return self.unrevealed==0


class GameOverError(Exception):
	pass


class InvalidCharError(Exception):
	def __init__(self,char):
		self.char = char

# Testing it in the terminal
#hangman = Hangman("test")
#print(str(hangman))
#for line in sys.stdin:
#	try:
#		#guess = hangman.guess_str(line[:-1])
#		#guess = hangman.guess_chars(line[:-1])
#		guess = hangman.guess_char(line[0])
#		print(str(hangman))
#
#		if hangman.is_complete():
#			print("Victory (Lives: %d)" % (hangman.lives,))
#			break
#		else:
#			print("'%s' was %s (Lives: %d)" % (line[0],"correct" if guess else "incorrect",hangman.lives))
#	except GameOverError:
#		print(str(hangman))
#		print("Game over. It was \"%s\"" % (hangman.word,))
#		break
