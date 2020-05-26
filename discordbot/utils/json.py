from discord.ext import commands
import discord, json, io, os

class Json:
	"""A simple class to work with json files"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.database = './discordbot/data/database'

	def create_config(self, nick: str, server: str) -> None:
		json_struct = {'warnings': 0, 'time': 0}
		with io.open('{}/{}/{}.json'.format(self.database, server, nick), 'w+', encoding='utf8') as f:
			__str__ = str(json.dumps(json_struct, indent=4, sort_keys=False, separators=(',', ': ')))
			f.write(__str__)

	def exists_config(self, nick: str, server:str) -> bool:
		return os.path.exists('{}/{}/{}.json'.format(self.database, server, nick))

	def get_config(self, nick: str, server: str) -> dict:
		filename = '{}/{}/{}.json'.format(self.database, server, nick)
		if os.path.exists(filename):
			return json.load(open(filename))
		return {}
	
	def config_to_member(self, member: object) -> object:
		nick = member.name
		server = member.server
		config = self.get_config(nick, server)
		if not config == {}:
			member.time = config['time']
			member.warnings = config['warnings']
		return member

	def update_config(self, nick: str, server: str) -> None:
		member = self.bot.members[server][nick]
		json_struct = {'warnings': member.warnings, 'time': member.time}
		with io.open('{}/{}/{}.json'.format(self.database, server, nick), 'w', encoding='utf8') as f:
			__str__ = str(json.dumps(json_struct, indent=4, sort_keys=False, separators=(',', ': ')))
			f.write(__str__)

	def delete_config(self, nick: str, server: str) -> None:
		if os.path.exists('{}/{}/{}.json'.format(self.database, server, nick)):
			os.remove('{}/{}/{}.json'.format(self.database, server, nick))
