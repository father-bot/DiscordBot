import discord, re
from discord.ext import commands
from discordbot.utils import Module

class Marriage(Module):
	'''Marry and divorce two members.'''

	proposal_yes = re.compile(r'(i do)|(yes)|(yeah)|(sure)|(да)')
	proposal_no = re.compile(r'(no)|(нет)|(не)')

	@commands.command(usage='<member>')
	async def marry(self, ctx: commands.Context, member: discord.Member):
		'''Marries to members'''
		target = member
		instigator = ctx.author
		ins = self.bot.members.get_member(instigator.guild.name, instigator.id)
		tar = self.bot.members.get_member(target.guild.name, target.id)
		if instigator.id in self.bot.proposal_cache:
			t = self.bot.proposal_cache.get(instigator.id)
			if t[0] == 'instigator':
				await ctx.send('You can only make one proposal at a time.')
			elif t[0] == 'target':
				await ctx.send('Sorry but you\'ve gotta answer your current proposal before you can make one of your own.')
			return
		elif target.id in self.bot.proposal_cache:
			t = self.bot.proposal_cache.get(target.id)
			if t[0] == 'instigator':
				await ctx.send('I\'m afraid they\'ve already proposed to someone. Give it a minute - see how it goes.')
			elif t[0] == 'target':
				await ctx.send('Someone just proposed to them. See what they say there first.')
			return
		if target.id == self.bot.user.id:
			await ctx.send('Unfortunately, my standards raise above you.')
			return
		elif target.bot or instigator.bot:
			await ctx.send('To the best of my knowledge, most robots can\'t consent.')
			return
		elif instigator.id == target.id:
			await ctx.send('That is you. You cannot marry the you.')
			return
		if ins.partner != '' or tar.partner != '':
			await ctx.send('Sorry, but you can marry at once.')
			return
		
		self.bot.proposal_cache[instigator.id] = ('instignator', 'marriage')
		self.bot.proposal_cache[target.id] = ('target', 'marriage')

		def check(message: discord.Message):
			if message.author.id != target.id:
				return False
			if message.channel.id != ctx.channel.id:
				return False
			c = message.content.casefold()
			no = self.proposal_no.search(c)
			yes = self.proposal_yes.search(c)
			if any([yes, no]):
				return 'no' if no else 'yes'
		try:
			await ctx.send(f'{target.display_name}, will you marry {instigator.display_name}?')
			m = await self.bot.wait_for('message', check=check, timeout=60)
		except TimeoutError:
			del self.bot.proposal_cache[instigator.id]
			del self.bot.proposal_cache[target.id]
			return
		response = check(m)
		if response == 'no':
			await ctx.send('Oh boy. They said no. That can\'t be good.')
		elif response == 'yes':
			await ctx.send(f'{instigator.mention}, {target.mention}, I now pronounce you married.')
			self.bot.members.set_member_partner(instigator.guild.name, instigator.id, target.id)
			self.bot.members.set_member_partner(target.guild.name, target.id, instigator.id)
			self.bot.db.set_new_database_value(instigator.guild.name, instigator.id, self.bot.members.get_info(instigator.guild.name, instigator.id)[1:])
			self.bot.db.set_new_database_value(target.guild.name, target.id, self.bot.members.get_info(target.guild.name, target.id)[1:])
		del self.bot.proposal_cache[instigator.id]
		del self.bot.proposal_cache[target.id]

	@commands.command(usage='<member>')
	async def divorce(self, ctx: commands.Context, member: discord.Member):
		'''Divorces to members'''
		target = member
		instigator = ctx.author
		ins = self.bot.members.get_member(instigator.guild.name, instigator.id)
		if ins.partner == '':
			await ctx.send('You\'re not married. Don\'t try ti divorce strangers.')
			return

		if str(ins.partner_id) != str(target.id):
			await ctx.send('You aren\'t married to that person.')
			return
		
		await ctx.send('You and your partner are now divorced. I wish you luck in your lives.')
		self.bot.members.set_member_partner(instigator.guild.name, instigator.id, 0)
		self.bot.members.set_member_partner(instigator.guild.name, target.id, 0)
		
		self.bot.db.set_new_database_value(instigator.guild.name, instigator.id, self.bot.members.get_info(instigator.guild.name, instigator.id)[1:])
		self.bot.db.set_new_database_value(target.guild.name, target.id, self.bot.members.get_info(target.guild.name, target.id)[1:])

def setup(bot: commands.Bot) -> None:
	bot.add_cog(Marriage(bot))
