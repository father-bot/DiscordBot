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
import json
import builtins
from discord.ext import commands

class JsonDatabase:
    """The class of json database utilities that require the :class:`commands.Bot`.
    to be passed to be useful.
    """
    def __init__(self, bot: commands.Bot = None):
        self.bot = bot
        self.database = "./discordbot/data/database/"
        self.database_tables = {}

    def create_database(self, name: str):
        """Create database directory"""
        path = f"{self.database}/{name}"
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except OSError:
                pass

    def create_table(self, name: str, table: dict):
        """Create database table"""
        table = {key: builtins.__dict__[value.replace("text", "str")]
                 for key, value in table.items()}
        if self.database_tables.get(name) is None:
            self.database_tables[name] = table
        del table

    def exists_database(self, name: str):
        """Show if database exists"""
        path = f"{self.database}/{name}"
        if os.path.exists(path):
            return os.path.isdir(path)
        return False

    def get_database_values(self, name: str):
        """Get all database values"""
        data = []
        path = f"{self.database}/{name}"
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                with open(f"{path}/{filename}") as file:
                    data.append(json.load(file))
        print(data)
        return data

    def get_database_value(self, name: str, identifier: str):
        """Get value by id"""
        data = {}
        path = f"{self.database}/{name}/{identifier}.json"
        if os.path.exists(path):
            with open(path) as file:
                data = json.load(file)
        return data

    def create_new_value(self, name: str, identifier: str, values: list):
        """Creates new database file with values"""
        data = {}
        table = self.database_tables[name]
        table_len = len(table)
        values_len = len(values)
        if table_len == values_len:
            for i in range(values_len):
                keys = list(table.keys())
                data[keys[i]] = table[keys[i]](values[i])
            with open(f"{self.database}/{name}/{identifier}.json", "w") as file:
                json.dump(data, file)

    def delete_database_table(self, table_name: str):
        """Delete table"""
        if self.database_tables.get(table_name) is not None:
            del self.database_tables[table_name]

    def delete_value(self, name: str, identifier: str):
        """Delete value"""
        path = f"{self.database}/{name}/{identifier}.json"
        if self.exists_database(name):
            if os.path.exists(path):
                os.remove(path)

    def delete_database(self, name: str):
        """Delete all the database"""
        path = f"{self.database}/{name}"
        if self.exists_database(name):
            for filename in os.listdir(path):
                os.remove(f"{path}/{filename}")
            os.removedirs(f"{self.database}/{name}")
