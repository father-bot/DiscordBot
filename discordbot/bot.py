import discord
from discord.ext import commands
from discordbot import modules_load, modules_remove
from discordbot import Member, members_init

class DiscordBot(commands.Bot):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.command_prefix = kwargs['command_prefix']
		self.members = { }

	def run(self, *args) -> None:
		self.loop.run_until_complete(self.start(*args))
		self.loop.close()

	async def on_ready(self) -> None:
		with open('./discordbot/data/welcome.txt') as f:
			print(f.read())
		print('Logged in as')
		print('login: {}'.format(self.user.name))
		print('id: {}'.format(self.user.id))
		if modules_load(self):
			print('Successfully loaded cogs.')
		else:
			print('Cannot load cogs.')
		self.members = members_init(self)
		print('Connected.')

	async def on_member_join(self, member: discord.Member) -> None:
		if member.guild.system_channel is not None:
			await member.guild.system_channel.send('Welcome {0.mention} to {1.name}!'.format(member, member.guild))
		self.members[member.display_name] = Member(member.display_name)

	async def on_member_remove(self, member: discord.Member) -> None:
		print('{} has left a server.'.format(member))
		del self.members[member.display_name]

	async def on_message(self, message: discord.message) -> None:
		if message.author.id == self.user.id:
			return
		self.ctx = await self.get_context(message)
		if message.content.startswith(self.command_prefix):
			await self.invoke(self.ctx)

	async def on_command_error(self, ctx, error) -> None:
		await ctx.send(error)
