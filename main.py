#!/usr/bin/env python3

from discordbot import DiscordBot

def main(token: str = None) -> None:
	if token is not None:
		bot = DiscordBot(command_prefix='?')
		try:
			bot.run(token)
		except KeyboardInterrupt:
			pass

if __name__ == '__main__':
	token = input('Enter your discord token: ')
	main(token)
