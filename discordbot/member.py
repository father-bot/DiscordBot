import time
import discord
from discord.ext import commands

class Member:
	def __init__(self, name):
		self.name = name
		self.time = 0
		self.channel_time = {}
		self.current_channel = None
		self.connect_time = 0
		self.ban_warnings = 0

	def state_change(self, channel) -> None:
		if self.current_channel is not channel and self.current_channel is not None:
			self.time = self.time + (int(time.time()) - self.connect_time)
			if channel in self.channel_time:
				self.channel_time[channel] = self.channel_time[channel] + (int(round(time.time())) - self.connect_time) 
			else:
				self.channel_time[channel] = (int(time.time()) - self.connect_time)
		self.connect_time = int(time.time())
		self.current_channel = channel

	def get_active_time(self) -> int:
		return self.time

	def get_ban_warnings(self) -> int:
		return self.ban_warnings

def members_init(bot: commands.Bot) -> dict:
	members = { }
	for guild in bot.guilds:
		for member in guild.members:
			if member != bot.user:
				members[member.name] = Member(member.name)
	return members
