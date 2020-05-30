import discord, time
from discord.ext import commands

class Member(object):
	def __init__(self, server, id, nick):
		self.id = id
		self.server = server
		self.nick = nick

		self.time = 0
		self.connect_time = 0
		self.current_channel = None
		self.channel_time = {}

		self.warnings = 0

		self.partner = ''
		self.partner_id = 0

	def update_time(self, channel: discord.VoiceChannel):
		#print(channel)
		if self.current_channel is not channel and self.current_channel is not None:
			self.time = self.time + (int(time.time()) - self.connect_time)
			if channel in self.channel_time:
				self.channel_time[channel] = self.channel_time[channel] + (int(round(time.time())) - self.connect_time)
			else:
				self.channel_time[channel] = (int(time.time()) - self.connect_time)
		self.connect_time = int(time.time())
		self.current_channel = channel
		#print(self.time)
		#print(str(self))

	def set_partner(self, partner, partner_id):
		self.partner = partner
		self.partner_id = partner_id

	def get_info(self):
		return [self.id, self.nick, self.server, self.time, self.warnings, self.partner]

	def __str__(self):
		return ('''Information about @{}:
Active time: {}
Ban warnings: {}
Partner: {}'''.format(self.nick, self.time, self.warnings, self.partner if self.partner else ''))

class Members(object):
	def __init__(self, bot):
		self.bot = bot
		self.__members = {f'{guild.name}/{member.id}': Member(guild.name, member.id, member.name) for guild in bot.guilds for member in guild.members}
		#print(self.__members)

	def create_member_nick(self, server, id, nick):
		self.__members[f'{server}/{id}'] = Member(server, id, nick)

	def get_member(self, server, id):
		return self.__members[f'{server}/{id}']

	def get_members(self):
		return self.__members
	
	def set_member_partner(self, server, id, partner_id):
		if partner_id == 0:
			self.__members[f'{server}/{id}'].set_partner('', 0)
		else:
			self.__members[f'{server}/{id}'].set_partner(self.__members[f'{server}/{partner_id}'].nick, partner_id)

	def update_member_time(self, server, id, channel: discord.VoiceChannel):
		self.__members[f'{server}/{id}'].update_time(channel)

	def get_info(self, server, id):
		return self.__members.get(f'{server}/{id}').get_info()
	
	def create_member(self, server, id):
		nick = [member.name for guild in self.bot.guilds if guild.name == server for member in guild.members if str(member.id) == id][0]
		self.__members[f'{server}/{id}'] = Member(server, id, nick)
	
	def delete_member(self, server, id):
		del self.__members[f'{server}/{id}']

	def update_member_warnings(self, server, id):
		self.__members[f'{server}/{id}'].warnings += 1

	def get_member_warnings(self, server, id):
		return self.__members[f'{server}/{id}'].warnings

	def set_member_data(self, server, id, data):
		try:
			member = self.__members[f'{server}/{id}']
		except KeyError:
			self.create_member(server, id)
		self.__members[f'{server}/{id}'].time = int(data[3])
		self.__members[f'{server}/{id}'].warnings = int(data[4])
		self.__members[f'{server}/{id}'].set_partner(str(data[5]), [member.id for _server in self.bot.guilds if _server.name == server for member in _server.members if member.name == str(data[5])][0] if str(data[5]) else 0)
