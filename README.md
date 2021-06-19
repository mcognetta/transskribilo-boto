# transskribilo-boto
Roboto por aŭtomata transskribado el x-sistemo al unikodan tekston en Diskordo.

# Intro

__Feel free to open issues if you find bugs or have improvements to make. Keep in mind that this was a one-day project and the author is not perfect.__

This is a small Discord bot for transcribing Esperanto text written with the x-system into Unicode. It is not meant to be complete or cover all cases.

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

You should then create a role on your server called `aŭttransskribiĝebla`. Users can opt-in to this role and the bot will automatically transcribe their messages.

You can then run the bot via just `python3 main.py` after you have installed the dependencies (via `poetry install`).

### TODOs
 - Add channel filter to allow for non-Esperanto channels where the bot does not run.
    - Should be specified in the `bot_config.ini` file.
 - Allow for custom opt-in role names.
    - Should be specified in the `bot_config.ini` file.
 - Make the message cache system better.
    - Probably just need to do a dictionary keyed by user/channel value being their last message and have a timer set to clear the cache after a set amount of time.
