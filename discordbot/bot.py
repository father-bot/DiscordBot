import discord, sys, os, sqlite3
from discord.ext import commands
from discordbot import Member, Members
from discordbot.utils import Modules#, Cli, Json
from discordbot.utils import Database

class DiscordBot(commands.Bot):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.command_prefix = kwargs['command_prefix']
		self.modules = Modules(self)
		self.database = './discordbot/data/database'
		if not os.path.exists(self.database):
			os.mkdir(self.database)
		self.proposal_cache = {}

	def run(self, *args) -> None:
		self.loop.run_until_complete(self.start(*args))
		self.modules.unload()
		self.loop.close()

	async def database_init(self):
		self.db = Database(self)
		self.servers = [guild.name for guild in self.guilds]
		self.members = Members(self)
		for server in self.servers:
			if not self.db.exists_database(server):
				self.db.create_database(server)
				self.db.create_default_database(server)
			for key, value in self.members.get_members().items():
				if server in key:
					try:
						data = self.db.get_database_value(server, key.split('/')[1])
						self.members.set_member_data(data[2], data[0], data)
					except:
						self.db.set_default_database_value(server, value.get_info())

	async def on_ready(self) -> None:
		try:
			with open('./discordbot/data/welcome.txt') as f:
				print(f.read())
		except OSError:
			print('Cannot find logo')
		print('Loading modules... ', end='')
		if self.modules.load():
			print('OK')
		else:
			print('\r[!] Cannot load modules.')
		print('Detecting members... ', end='')
		try:
			await self.database_init()
			print('OK')
		except:
			print('\r[!] Cannot load members')
		print('Logged in as')
		print('login: {}'.format(self.user.name))
		print('id: {}'.format(self.user.id))
		print('prefix: {}'.format(self.command_prefix))
		print('Connected.')

	async def on_member_join(self, member: discord.Member) -> None:
		if member.guild.system_channel is not None:
			await member.guild.system_channel.send('Welcome {0.mention} to {1.name}!'.format(member, member.guild))
		#self.json.create_config(member.name, member.guild.name)
		self.members.create_member_nick(member.guild.name, member.id, member.name)
		self.db.set_default_database_value(member.guild.name, self.members.get_info(member.guild.name, member.id))

	async def on_member_remove(self, member: discord.Member) -> None:
		print('{} has left a server.'.format(member))
		self.db.delete_database_id(member.guild.name, member.id)
		self.members.delete_member(member.guild.name, member.id)

	async def on_message(self, message: discord.message) -> None:
		if message.author.id == self.user.id:
			return
		message.content = message.content.lower()
		self.ctx = await self.get_context(message)
		if message.content.startswith(self.command_prefix):
			await self.invoke(self.ctx)

	async def on_command_error(self, ctx, error) -> None:
		await ctx.send(error)

	async def on_voice_state_update(self, member: discord.Member = None, before: discord.VoiceState = None, after: discord.VoiceState = None) -> None:
		if member is not None:
			try:
				self.members.update_member_time(member.guild.name, member.id, member.voice.channel)
			except Exception as e:
				self.members.update_member_time(member.guild.name, member.id, None)
			self.db.set_new_database_value(member.guild.name, member.id, self.members.get_info(member.guild.name, member.id)[1:])
