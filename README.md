# transskribilo-boto
Roboto por aŭtomata transskribado el x-sistemo al unikodan tekston.

# Intro

This is a small Discord bot for transcribing Esperanto text writing with the x-system to Unicode. It is not meant to be complete or cover all cases.

The bot runs in the background of a Discord server and detects text that can be transcribed, does the transcription, and replaces the message.

It comes with one command, `!malfaru`, which undoes the most recent transcription that the bot made to one of your messages (if applicable).

# How To Run

Clone this repo and add a bot on Discord (https://discord.com/developers/applications). The bot should have the following permissions (this list might shrink in the future as I find some are unnecessary):
 - `Manage Emojis`
 - `Manage Webhooks`
 - `View Channels`
 - `Send Messages`
 - `Manage Messages`
 - `Mention Everyone`
 - `Use External Emojis`
 - `Add Reactions`

This corresponds to the permissions integer `1611017280`.

Once you create the bot, get its key, and add it to your server, create a `bot_config.ini` file in the top level of your local copy of this repo. It should look like this:

```
[DEFAULT]
key = <your bot key here>
```

You can then run the bot via just `python3 main.py` after you have installed the dependencies (in the poetry file).
