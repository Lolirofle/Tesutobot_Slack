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
	def __init__(self,word,lives=12):
		self.initial_lives = 12 # TODO: Implement an arbitrary number of lives
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
		return "%s\n%s (%s)" % (ascii_art[self.lives],self.gamestate if self.unrevealed==0 else ' '.join(self.gamestate),''.join(self.guesses))

	def build_gamestate(self):# TODO: An alternative may be to use a list of chars. Strings are immutable, but lists are not
		self.gamestate = ''
		self.unrevealed = 0
		for c in self.word:# I sure hope this is a hashed O(1) operation
			if c in self.guesses or not c.isalpha():
				self.gamestate+= c
			else:
				self.gamestate+= '_'
				self.unrevealed+= 1

	def guess_char(self,c):
		'''
		Guess using a character,
		adding it to the guess list and
		revealing the character in the gamestate if the word contained it.

		Returns a boolean for whether the guess was correct or None if the letter already have been guessed.
		Raises a GameOverError when loses.
		'''

		if c in self.guesses:
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
		pass

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

# Testing it in the terminal
#hangman = Hangman("test")
#print(str(hangman))
#for line in sys.stdin:
#	try:
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
