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

import os
from discord.ext import commands

class Module(commands.Cog):
    """The base class of module that require the :class:`.Bot`
    to be passed to be useful.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

class Modules:
    """The class of custom modules utilities that require the :class:`.Bot`.
    to be passed to be useful.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.modules_path = './discordbot/cogs/{}'
        self.python_path = 'discordbot.cogs.{}'

    def load_module(self, name: str) -> bool:
        """The method to load module.

        Parameters
        -----------
        name: :class:`str`
            Name of the module.
        """
        try:
            self.bot.load_extension(self.python_path.format(name))
        except commands.errors.ExtensionAlreadyLoaded:
            pass
        except Exception as e:
            print(e)
            return False
        return True

    def reload_module(self, name: str) -> bool:
        """The method to reload module.

        Parameters
        -----------
        name: :class:`str`
            Name of the module.
        """
        try:
            self.bot.reload_extension(self.python_path.format(name))
        except Exception:
            return False
        return True

    def unload_module(self, name: str) -> bool:
        """The method to unload module.

        Parameters
        -----------
        name: :class:`str`
            Name of the module.
        """
        try:
            self.bot.unload_extension(self.python_path.format(name))
        except Exception:
            return False
        return True

    def load_modules(self) -> bool:
        """The method to load all modules.
        """
        for filename in os.listdir(self.modules_path.format('')):
            if not '__init__' in filename and filename.endswith('.py'):
                if not self.load_module(filename[:-3]):
                    return False
        return True

    def reload_modules(self) -> bool:
        """The method to reload all modules.
        """
        for filename in os.listdir(self.modules_path.format('')):
            if not '__init__' in filename and filename.endswith('.py'):
                if not self.reload_module(filename[:-3]):
                    return False
        return True

    def unload_modules(self) -> bool:
        """The method to unload all modules.
        """
        for filename in os.listdir(self.modules_path.format('')):
            if not '__init__' in filename and filename.endswith('.py'):
                if not self.unload_module(filename[:-3]):
                    return False
        return True
