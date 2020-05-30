import discord
from discord.ext import commands
from discordbot import Member
from discordbot.utils import Module
import asyncio

class Ban(Module):
	'''Bans or reports users.'''

	@commands.command(usage='<member> <reason>')
	async def report(self, ctx: commands.Context, member: discord.Member = None, *, reason: str = None) -> None:
		'''Reports user.'''
		if reason is not None and member is not None: # If member or reason isn't None
			__member = self.bot.members
			warnings = __member.get_member_warnings(member.guild.name, member.id)
			if warnings >= 2:
				await ctx.send('Member {} was banned.'.format(member.name))
				await member.ban(reason=reason)
			else:
				mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')
				__member.update_member_warnings(member.guild.name, member.id)
				warnings = __member.get_member_warnings(member.guild.name, member.id)
				self.bot.db.set_new_database_value(member.guild.name, member.id, __member.get_info(member.guild.name, member.id)[1:])
				await ctx.send('{} more report{} for ban.'.format(3-warnings, 's' if 3-warnings != 1 else ''))
				await member.add_roles(mute_role)
				await asyncio.sleep(60)
				if member.name in __member.get_members().keys():
					await member.remove_roles(mute_role)

	@commands.command(usage='<member> <reason>')
	async def ban(self, ctx: commands.Context, member: discord.Member = None, *, reason: str = None) -> None:
		'''Bans user.'''
		await ctx.send('Member {} was banned.'.format(member.name))
		await member.ban(reason=reason)

def setup(bot: commands.Bot) -> None:
	bot.add_cog(Ban(bot))
