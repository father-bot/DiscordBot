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
			__member__ = self.bot.members[member.guild.name][member.name]
			__member__.json.config_to_member(__member__)
			if __member__.warnings >= 2:
				await ctx.send('Member {} was banned.'.format(member.name))
				await member.ban(reason=reason) # Bans member
			else:
				mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')
				__member__.warnings += 1
				__member__.json.update_config(member.name, member.guild.name)
				if 3-__member__.warnings == 1:
					await ctx.send('1 more report for ban.')
				else:
					await ctx.send('{} more reports for ban.'.format(3-__member__.warnings))
				await member.add_roles(mute_role)
				await asyncio.sleep(2 * 60 * 60) # 2 hours
				if member.name in self.bot.members[member.guild.name]: # If member wasn't banned.
					await member.remove_roles(mute_role)

	@commands.command(usage='<member> <reason>')
	async def ban(self, ctx: commands.Context, member: discord.Member = None, *, reason: str = None) -> None:
		'''Bans user.'''
		await ctx.send('Member {} was banned.'.format(member.name))
		await member.ban(reason=reason)

def setup(bot: commands.Bot) -> None:
	bot.add_cog(Ban(bot))
