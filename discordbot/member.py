import time
import discord
from discord.ext import commands
from discordbot.utils import Json 

class Member(object):
	def __init__(self, name, server, bot):
		self.name = name
		self.bot = bot
		self.server = server
		self.time = 0
		self.channel_time = {}
		self.current_channel = None
		self.connect_time = 0
		self.warnings = 0
		self.json = Json(self.bot)
		self.partner = ''

	def __str__(self):
		self.json.config_to_member(self)
		return ("""Information about @{}:
Ban warnings: {}
Active time: {}
Partner: {}
""".format(self.name, self.warnings, self.time, self.partner if self.partner else 'alone'))

	def update(self, channel: discord.VoiceChannel = None) -> None:
		if self.current_channel is not channel and self.current_channel is not None:
			self.time = self.time + (int(time.time()) - self.connect_time)
			if channel in self.channel_time:
				self.channel_time[channel] = self.channel_time[channel] + (int(round(time.time())) - self.connect_time)
			else:
				self.channel_time[channel] = (int(time.time()) - self.connect_time)
		self.connect_time = int(time.time())
		self.current_channel = channel
		self.json.update_config(self.name, self.server)

def members(bot: commands.Bot) -> dict:
	servers = { }
	json = Json(bot)
	for guild in bot.guilds:
		members = { }
		for member in guild.members:
			if member != bot.user:
				if not json.exists_config(member.name, guild.name):
					json.create_config(member.name, guild.name)
				members[member.name] = json.config_to_member(Member(member.name, guild.name, bot))
		servers[guild.name] = members
	return servers
