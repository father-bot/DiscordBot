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
import sqlite3
from discord.ext import commands

class SQLiteDatabase:
    """The class of sqlite database utilities that require the :class:`commands.Bot`.
    to be passed to be useful.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = "./discordbot/data/database/"
        self.database_tables = {}
        self.conn = None
        self.cursor = None

    def create_database(self, name: str):
        """Create new database.

        Parameter
        ---------
        name: :class:`str`
            Name of new database.
        """
        if not os.path.exists(f"{self.database}/{name}.db"):
            filename = open(f"{self.database}/{name}.db", "w")
            filename.close()

    def create_databases(self):
        """Create new databases.
        """
        for guild in self.bot.guilds:
            self.create_database(guild.name)

    def exists_database(self, name: str):
        """Show if database exists.

        Parameter
        ---------
        name: :class:`str`
            Name of the database.
        """
        return os.path.exists(f"{self.database}/{name}.db")

    def create_new_table_database(self, name: str, table_name: str, options: dict):
        """Create new database table.

        Parameter
        ---------
        name: :class:`str`
            Name of the database.
        table_name: :class:`str`
            Name of the table.
        options: :class:`dict`
            Options for the table.
        """
        if not table_name in self.database_tables.keys():
            try:
                self.database_tables[table_name] = [{key:options[key]} for key in options]
                table = ",\n".join([f"{key} {options[key]}" for key in options]) if options else ""
                self.conn = sqlite3.connect(f"{self.database}/{name}.db")
                self.cursor = self.conn.cursor()
                self.cursor.execute("""CREATE TABLE {} (
                                       id INTEGER PRIMARY KEY,
                                       {}
                                    )""".format(table_name, table))
                self.conn.commit()
                self.conn.close()
            except sqlite3.OperationalError:
                return

    def _to_string(self, table_name: str, data: list):
        """Converts data to string.

        Parameters
        ----------
        table_name: :class:`str`
            Name of the table.
        data: :class:`list`
            All the data.
        """
        result = ""
        for index, value in enumerate(data, 0):
            table = self.database_tables[table_name][index]
            key = list(table.keys())[0]
            if table[key] == "text":
                result += f"'{value}', "
            elif table[key] == "int":
                result += f"{value}, "
        return result[:-2]

    def _to_string_with_variables(self, table_name: str, data: list):
        """Converts data to string with variables name.

        Parameters
        ----------
        table_name: :class:`str`
            Name of the table.
        data: :class:`list`
            All the data.
        """
        result = ""
        for index, value in enumerate(data, 0):
            table = self.database_tables[table_name][index]
            key = list(table.keys())[0]
            if table[key] == "text":
                result += f"{key} = '{value}', "
            elif table[key] == "int":
                result += f"{key} = {value}, "
        return result[:-2]

    def set_default_database_value(self, name: str, table_name: str, data: list):
        """Set default database values.

        Parameters
        ----------
        name: :class:`str`
            Name of the database.
        table_name: :class:`str`
            Name of the table.
        data: :class:`list`
            All the data.
        """
        if table_name in self.database_tables.keys():
            self.conn = sqlite3.connect(f"{self.database}/{name}.db")
            self.cursor = self.conn.cursor()
            try:
                self.cursor.execute("""INSERT INTO {} VALUES ({}, {})""".format(
                    table_name, data[0], self._to_string(table_name, data[1:])))
            except sqlite3.IntegrityError:
                pass
            self.conn.commit()
            self.conn.close()

    def delete_database_id(self, name: str, table_name: str, identifier: int):
        """Converts data to string with variables name.

        Parameters
        ----------
        name: :class:`str`
            Name of the database.
        table_name: :class:`str`
            Name of the table.
        identifier: :class:`int`
            ID of section.
        """
        if table_name in self.database_tables.keys():
            self.conn = sqlite3.connect(f"{self.database}/{name}.db")
            self.cursor = self.conn.cursor()
            self.cursor.execute("""DELETE FROM {} WHERE id = {}""".format(table_name, identifier))
            self.conn.commit()
            self.conn.close()

    def set_new_database_value(self, name: str, table_name: str, identifier: int, data: list):
        """Set new database values.

        Parameters
        ----------
        name: :class:`str`
            Name of the database.
        table_name: :class:`str`
            Name of the table.
        identifier: :class:`int`:
            ID of section.
        data: :class:`list`
            All the data.
        """
        if table_name in self.database_tables.keys():
            self.conn = sqlite3.connect(f"{self.database}/{name}.db")
            self.cursor = self.conn.cursor()
            result = self._to_string_with_variables(table_name, data)
            self.cursor.execute("""UPDATE {}
                                   SET
                                     {}
                                   WHERE id = {}""".format(table_name, result, identifier))
            self.conn.commit()
            self.conn.close()

    def get_database_value(self, name: str, table_name: str, identifier: int):
        """Get database value using ID.

        Parameters
        ----------
        name: :class:`str`
            Name of the database.
        table_name: :class:`str`
            Name of the table.
        identifier: :class:`int`
            ID of section.
        """
        self.conn = sqlite3.connect(f"{self.database}/{name}.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM {} WHERE id = {}".format(table_name, identifier))
        data = self.cursor.fetchall()
        try:
            data = data[0]
        except IndexError:
            data = None
        self.conn.commit()
        self.conn.close()
        return data

    def get_database_values(self, name: str, table_name: str):
        """Get database values.

        Parameters
        ----------
        name: :class:`str`
            Name of the database.
        table_name: :class:`str`
            Name of the table.
        """
        self.conn = sqlite3.connect(f"{self.database}/{name}.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"SELECT * FROM {table_name}")
        data = self.cursor.fetchall()
        self.conn.commit()
        self.conn.close()
        return data
