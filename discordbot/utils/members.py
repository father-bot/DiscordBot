# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2020 Simon Chaykin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from discord.ext import commands

class Member:
    """Represents a member.

    Attributes
    ----------
    identifier: :class:`str`
        ID of the member.
    guild_identifier: :class:`str`
        ID of the server.
    """
    def __init__(self, identifier: str, guild_identifier: str):
        self.identifier = identifier
        self.nick = None
        self.guild_identifier = guild_identifier

        self.roles = []

    def change_nickname(self, nick: str):
        """Set new member's nick.

        Parameter
        ---------
        nick: :class:`str`
            New nick of the member.
        """
        self.nick = nick

    def add_role(self, role: str):
        """Adds new role to the member.

        Parameter
        ---------
        role: :class:`str`
            The name of the role.
        """
        self.roles.append(role)

    def remove_role(self, role: str):
        """Removes role from the member's roles.

        Parameter
        ---------
        role: :class:`str`
            The name of the role.
        """
        if role in self.roles:
            del self.roles[self.roles.index(role)]

    def get_roles(self):
        """Get all member's roles.
        """
        return self.roles

    def __repr__(self):
        return f'<{self.__class__.__name__} id="{self.identifier}">'

class Members:
    """The class of custom members' utilities that require the :class:`commands.Bot`.
    to be passed to be useful.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guilds = self.bot.guilds
        self.__members = {}
        self._class = Member

    def create_member(self, identifier: str, guild_identifier: str):
        """Create new member.

        Parameter
        ---------
        identifier: :class:`str`
            ID of new member.
        guild_identifier: :class:`str`
            ID of member's server.
        """
        key = f'{guild_identifier}/{identifier}'
        if not key in self.__members.keys():
            self.__members[key] = self._class(identifier, guild_identifier)
            return True
        return False

    def reload_members(self, bot: commands.Bot):
        """Update list of members.

        Parameter
        ---------
        identifier: :class:`commands.Bot`
            The bot that class requires to be passed to be useful.
        """
        self.bot = bot
        self.guilds = self.bot.guilds
        self.__members = {f'{guild.identifier}/{member.identifier}':
                          self._class(member.identifier, guild.identifier)
                          for guild in self.guilds
                          for member in guild.members}

    def add_role_member(self, identifier: str, guild_identifier: str, role: str):
        """Add member's role.

        Parameter
        ---------
        identifier: :class:`str`
            ID of the member.
        guild_identifier: :class:`str`
            ID of member's server.
        role: :class:`str`
            The name of the role.
        """
        self.__members[f'{guild_identifier}/{identifier}'].add_role(role)

    def remove_role_member(self, identifier: str, guild_identifier: str, role: str):
        """Remove member's role.

        Parameter
        ---------
        identifier: :class:`str`
            ID of the member.
        guild_identifier: :class:`str`
            ID of member's server.
        role: :class:`str`
            Name of the role.
        """
        self.__members[f'{guild_identifier}/{identifier}'].remove_role(role)

    def get_roles_member(self, identifier: str, guild_identifier: str):
        """Get member's roles.

        Parameter
        ---------
        identifier: :class:`str`
            ID of the member.
        guild_identifier: :class:`str`
            ID of member's server.
        """
        self.__members[f'{guild_identifier}/{identifier}'].get_roles()

    def change_nickname_member(self, identifier: str, guild_identifier: str, nick: str):
        """Change member's nickname.

        Parameter
        ---------
        identifier: :class:`str`
            ID of the member.
        guild_identifier: :class:`str`
            ID of member's server.
        nick: :class:`str`
            New nickname of the member.
        """
        self.__members[f'{guild_identifier}/{identifier}'].change_nickname(nick)

    def get_members(self):
        """Get all members.
        """
        return self.__members

    def get_member(self, identifier: str, guild_identifier: str):
        """Get the member.

        Parameter
        ---------
        identifier: :class:`str`
            ID of the member.
        guild_identifier: :class:`str`
            ID of member's server.
        """
        member = self.__members.get(f'{guild_identifier}/{identifier}')
        return member

    def exists_member(self, identifier: str, guild_identifier: str):
        """Show if member exists.

        Parameter
        ---------
        identifier: :class:`str`
            ID of the member.
        guild_identifier: :class:`str`
            ID of member's server.
        """
        return bool(self.get_member(identifier, guild_identifier))

    def delete_member(self, identifier: str, guild_identifier: str):
        """Delete the member.

        Parameter
        ---------
        identifier: :class:`str`
            ID of the member.
        guild_identifier: :class:`str`
            ID of member's server.
        """
        if self.exists_member(identifier, guild_identifier):
            del self.__members[f'{guild_identifier}/{identifier}']
            return True
        return False

    def delete_members(self):
        """Create all members.
        """
        for key in self.__members.keys():
            if not self.delete_member(key.split('/')[1], key.split('/')[0]):
                return False
        return True

    def __repr__(self):
        return f'<{self.__class__.__name__} members={len(self.__members)}>'
