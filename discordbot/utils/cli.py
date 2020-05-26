import os

class Cli:
	def __init__(self, bot):
		self.bot = bot
		self.database = './discordbot/data/'

	def mkdir(self, directory):
		try:
			if not os.path.exists(self.database + directory):
				os.mkdir(self.database + str(directory))
		except:
			return False
		return True

	def mkdirs(self, directories):
		for directory in directories:
			self.mkdir('database/' + str(directory))
		return True
