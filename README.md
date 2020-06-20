# Discord Bot

![Twitter](https://img.shields.io/twitter/follow/thecakeisfalse?label=Follow)
![Github](https://img.shields.io/github/followers/game-lover?label=Follow&style=social)

Discord Bot - a simple bot for Discord servers, that uses [Discord.py](https://github.com/Rapptz/discord.py) API to work.

## Summary

  - [Getting Started](#getting-started)
  - [Example of Bot](#example-of-bot)
  - [Authors](#authors)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Getting Started

These instructions will get you a copy of the project up and running on your machine.

### Prerequisites

There are apt packages, needed by Discord Bot

    python3, python3-dev, python3-pip

### Installing

To install Discord Bot

```bash
git clone https://github.com/game-lover/DiscordBot
cd DiscordBot
pip3 install -r requirements.txt
```

### Creating a discord bot and getting its discord token

1. Head over to the [discord developer portal](https://discordapp.com/developers/applications) and sign in if you haven't already.

2. Press "Create an application".

3. From the left menu, click "Bot", then press "Add bot" on the next screen.

4. Press the "Copy" button under the "Client ID" section to get your discord bot client id. Insert your client id in the link: https://discord.com/oauth2/authorize?client_id=ENTER_YOUR_CLIENT_ID_HERE&scope=bot&permissions=805314622. 
5. Finally, press the "Copy" button under the "Token" section to get your discord bot token and write it in config.txt.

### Running

To run Discord Bot

```bash
python3 main.py
```

### Link to download DiscordBot on your server

[Link to install DiscordBot on your server](https://discord.com/oauth2/authorize?client_id=707219673523159160&scope=bot&permissions=805314622)

## Example of Bot

You can create your own bot based on discordbot.

```python
#!/usr/bin/env python3

from discordbot import DiscordBot

def main(token: str = None) -> None:
	if token is not None:
		bot = DiscordBot(command_prefix='!')
		try:
			bot.run(token)
		except KeyboardInterrupt:
			pass

if __name__ == '__main__':
	token = 'ENTER_YOUR_TOKEN_HERE'
	main(token)
```

## Authors

  - **Simon Chaykin** - *Main developer*

## License

This project is licensed under the [MIT LICENSE](LICENSE).

## Acknowledgments

  - [Discord.py API](https://discordpy.readthedocs.io/en/latest/api.html)
