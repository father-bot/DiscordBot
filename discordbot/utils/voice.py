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

import time
import discord

class VoiceActivity:
    """Represents member's voice activity.

    Attributes
    ----------
    identifier: :class:`str`
        ID of the member.

    """
    def __init__(self, identifier: str):
        self.identifier = identifier
        self.time = 0
        self.channels = {}
        self.current_channel = None
        self.connection_time = 0

    def update_time(self, channel: discord.VoiceChannel):
        """Updates voice activity time.

        Parameter
        ---------
        channel: :class:`discord.VoiceChannel`
            Information of voice channel.
        """
        if self.current_channel is not channel and self.current_channel is not None:
            self.time = self.time + (int(time.time()) - self.connection_time)
            if channel in self.channels:
                self.channels[channel] = (self.channels[channel] + \
                                         int(round(time.time()) - self.connection_time))
            else:
                self.channels[channel] = (int(time.time()) - self.connection_time)
        self.connection_time = int(time.time())
        self.current_channel = channel

    def get_time(self):
        """Get voice activity time
        """
        return self.time
