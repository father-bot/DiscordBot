import os
import sys
import sqlite3
import discord
from discord.ext import commands
from discordbot import Modules

class DiscordBot(commands.Bot):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.command_prefix = kwargs['command_prefix']
		self.modules = Modules(self)

	def run(self, *args) -> None:
		self.loop.run_until_complete(self.start(*args))
		self.modules.unload_modules()
		self.loop.close()

	async def on_ready(self) -> None:
		with open('./discordbot/welcome.txt') as f:
			print(f.read())
		print('Loading modules... ', end='')
		if self.modules.load_modules():
			print('OK')
		else:
			print('\r[!] Cannot load modules.')
		print('Logged in as')
		print('login: {}'.format(self.user.name))
		print('id: {}'.format(self.user.id))
		print('prefix: {}'.format(self.command_prefix))
		print('Connected.')

	async def on_member_join(self, member: discord.Member) -> None:
		if member.guild.system_channel is not None:
			await member.guild.system_channel.send('Welcome {0.mention} to {1.name}!'.format(member, member.guild))

	async def on_member_remove(self, member: discord.Member) -> None:
		print('{} has left a server.'.format(member))
		self.db.delete_database_id(member.guild.name, member.id)
		self.members.delete_member(member.guild.name, member.id)

	async def on_message(self, message: discord.message) -> None:
		if message.author.id == self.user.id:
			return
		ctx = await self.get_context(message)
		if message.content.startswith(self.command_prefix):
			await self.invoke(ctx)
