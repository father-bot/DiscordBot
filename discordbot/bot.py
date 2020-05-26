import discord, sys
from discord.ext import commands
from discordbot.utils import Modules
from discordbot.utils import Cli
from discordbot import Member, members
from discordbot.utils import Json

class DiscordBot(commands.Bot):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.command_prefix = kwargs['command_prefix']
		self.modules = Modules(self)
		self.cli = Cli(self)
		self.json = Json(self)
		self.is_inited = False

	def run(self, *args) -> None:
		self.loop.run_until_complete(self.start(*args))
		self.modules.unload()
		self.loop.close()

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
		self.servers = [guild.name for guild in self.guilds]
		self.cli.mkdir('database')
		self.cli.mkdirs(self.servers)
		print('Detecting members... ', end='')
		self.members = members(self)
		if self.members == {}:
			print('\r[!] No members found')
		else:
			print('OK')
		self.is_inited = False
		print('Logged in as')
		print('login: {}'.format(self.user.name))
		print('id: {}'.format(self.user.id))
		print('prefix: {}'.format(self.command_prefix))
		print('Connected.')

	async def on_member_join(self, member: discord.Member) -> None:
		if member.guild.system_channel is not None:
			await member.guild.system_channel.send('Welcome {0.mention} to {1.name}!'.format(member, member.guild))
		self.json.create_config(member.name, member.guild.name)
		self.members[member.guild.name][member.name] = Member(member.name, member.guild.name, self)

	async def on_member_remove(self, member: discord.Member) -> None:
		print('{} has left a server.'.format(member))
		self.json.delete_config(member.name, member.guild.name)
		del self.members[member.guild.name][member.name]

	async def on_message(self, message: discord.message) -> None:
		if message.author.id == self.user.id:
			return
		self.ctx = await self.get_context(message)
		if message.content.startswith(self.command_prefix):
			await self.invoke(self.ctx)

	async def on_command_error(self, ctx, error) -> None:
		await ctx.send(error)

	async def on_voice_state_update(self, member: discord.Member = None, before: discord.VoiceState = None, after: discord.VoiceState = None) -> None:
		if member is not None:
			if member.voice is not None and self.is_inited:
				self.members[member.guild.name][member.name].update(member.voice.channel)
			else:
				self.members[member.guild.name][member.name].update()
