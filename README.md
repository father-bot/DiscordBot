# Discord Bot

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

### How to get Discord Token

Go to [Discord Developers Site](https://discord.com/developers/applications/) and create new application. Go to tab 'Bot' and copy the token.

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
	token = 'TOKEN'
	main(token)
```

## Authors

  - **Simon Chaykin** - *Main developer*

## License

This project is licensed under the [MIT LICENSE](LICENSE).

## Acknowledgments

  - [Discord.py API](https://discordpy.readthedocs.io/en/latest/api.html)
