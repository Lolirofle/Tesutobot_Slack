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

		self.restart()

	def __str__(self):
		return "%s\n%s (%s)" % (ascii_art[self.lives],' '.join(self.gamestate),''.join(self.guesses))

	def build_gamestate(self):# TODO: An alternative may be to use a list of chars. Strings are immutable, but lists are not
		self.gamestate = ''
		unrevealed = 0
		for c in self.word:# I sure hope this is a hashed O(1) operation
			if c in self.guesses or not c.isalpha():
				self.gamestate+= c
			else:
				self.gamestate+= '_'
				unrevealed+= 1
		return unrevealed

	def guess_char(self,c):
		'''
		Guess using a character,
		adding it to the guess list and
		revealing the character in the gamestate if the word contained it.

		Returns whether the game is completed (with a victory).
		Raises a GameOverError when loses.
		'''
		if self.lives<=0:
			raise GameOverError

		self.guesses.add(c);
		if c in self.word_chars:
			return self.build_gamestate()==0
		else:
			self.lives-= 1
			return False

	def guess_str(self,s):
		pass

	def restart(self):
		self.lives = self.initial_lives
		self.guesses = set()
		self.build_gamestate()

	def reveal(self):
		''' Reveals the gamestate, thus completes the game (without adding the missing characters to the guess list) '''
		self.gamestate = self.word

class GameOverError(Exception):
	pass

# Testing it in the terminal
#hangman = Hangman("test")
#print(str(hangman))
#for line in sys.stdin:
#	hangman.guess_char(line[0])
#	print(str(hangman))
