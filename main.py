import sys, collections, configparser

import discord
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands

from transskribilo.data import data_utils

bot = commands.Bot(
    command_prefix="!",
    description="Roboto por aŭtomata transskribado el x-sistemo al unikodan tekston.",
)
bot._ignore_list = data_utils.get_filter_wordlist()


@bot.event
async def on_connect():
    print("transskribilo connected")


@bot.event
async def on_ready():
    print("transskribilo ready")


replace_list = {
    "cx": "ĉ",
    "gx": "ĝ",
    "hx": "ĥ",
    "jx": "ĵ",
    "sx": "ŝ",
    "ux": "ŭ",
    "Cx": "Ĉ",
    "Gx": "Ĝ",
    "Hx": "Ĥ",
    "Jx": "Ĵ",
    "Sx": "Ŝ",
    "Ux": "Ŭ",
}

_allowed_ending_punc = list(".?!,")

CACHED_MESSAGE = collections.namedtuple(
    "CACHED_MESSAGE", "author original_content channel webhook_msg"
)
bot._message_cache = collections.deque(maxlen=100)


def _queue_msg(author, content, channel, hook_msg):

    if len(bot._message_cache) == bot._message_cache.maxlen:
        bot._message_cache.popleft()

    bot._message_cache.append(CACHED_MESSAGE(author, content, channel, hook_msg))


def _message_metadata_filter(message):

    # filter out messages with bad metadata

    # if the author isn't a use
    author = message.author
    if not isinstance(author, discord.member.Member):
        return False

    channel = message.channel
    guild = channel.guild
    role = discord.utils.find(lambda r: r.name == "aŭttransskribiĝebla", guild.roles)

    # if the user hasn't opted-in
    if role not in author.roles:
        return False

    # if the message isn't plain text
    if message.embeds:
        return False

    # if the message has attachments, files, etc
    if message.attachments:
        return False

    return True


def ascii_condition(t):
    o = ord(t)
    return 65 <= o <= 90 or 97 <= o <= 122 or t == "-"


def token_validator(token):

    # check if tokens are valid via some heuristics

    # not too long
    if len(token) > 50:
        return False

    # not a mention
    if token[0] == "@":
        return False

    # not a filtered word (things with literal ux, cx, etc.)
    if token in bot._ignore_list:
        return False

    # not words with lots of punctuation inside (emails, websites, etc)
    if token[-1] in _allowed_ending_punc:
        return all(ascii_condition(t) for t in token[:-1])
    else:
        return all(ascii_condition(t) for t in token)


def replacer(s):

    # iterate over tokens and replace them via the unicode rules
    replaced = False
    split_text = s.split(" ")
    for idx, token in enumerate(split_text):
        if token_validator(token):
            if any(t in token for t in replace_list):
                replaced = True

                for before, after in replace_list.items():
                    split_text[idx] = split_text[idx].replace(before, after)
    return (replaced, " ".join(split_text))


def _find_last_edited_msg(author, channel):
    # search backwards through the cache to find a message that
    # matches the author and channel (and then remove it)
    for i in range(len(bot._message_cache) - 1, -1, -1):
        if (
            bot._message_cache[i].author == author
            and bot._message_cache[i].channel == channel
        ):
            out = bot._message_cache[i]
            bot._message_cache.remove(out)
            return out
    return None


@bot.command(
    brief="Malfari vian lastan transskribitan mesaĝon.",
    help="Malfari vian lastan transskribitan mesaĝon.",
)
async def malfaru(ctx):
    msg, author = ctx.message, ctx.author
    channel = msg.channel

    # find the last edited message by this user in the current
    # channel, or return None
    edited_msg = _find_last_edited_msg(author, channel)
    if edited_msg:

        # fetch and delete the edited message
        webhook_msg = await ctx.fetch_message(edited_msg.webhook_msg.id)
        await webhook_msg.delete()

        # send a message via a webhook with the original message content
        hook = await msg.channel.create_webhook()
        await hook.send(
            edited_msg.original_content,
            username=author.name + " | (malfarita)",
            avatar_url=author.avatar_url,
        )
        await hook.delete()

        # emojis for "pardonu"
        for emoji in [
            "\U0001F1F5",
            "\U0001F1E6",
            "\U0001F1F7",
            "\U0001F1E9",
            "\U0001F1F4",
            "\U0001F1F3",
            "\U0001F1FA",
        ]:
            await msg.add_reaction(emoji=emoji)
        # delete the undo command message so that it doesn't
        # clutter the screen
        await msg.delete(delay=2)
    else:
        await ctx.send(
            f"{author.mention} Mi ne povas trovi vian transskribintan mesaĝon."
        )


@bot.event
async def on_message(message):
    author, content, channel = message.author, message.content, message.channel

    # filter out messages we don't want to process
    # for example, users who have not opted in or messages
    # that contain files, etc. that we do not want to be
    # responsible for
    if _message_metadata_filter(message):

        # a transcription function that returns a flag indicating if any
        # transcription took place and the (possibly) edited text
        replaced, edited_text = replacer(content)

        if replaced:

            hook = await message.channel.create_webhook(name="transskribilo_hook")
            await message.delete()

            # send the transcribed message via the webhook
            # with the original author's information
            webhook_msg = await hook.send(
                edited_text,
                username=author.display_name + " | (transskribita)",
                avatar_url=author.avatar_url,
                # allows the webhook message info to be cached
                wait=True,
            )

            # stores the message in an LRU cache in case of
            # an undo command
            _queue_msg(author, content, channel, webhook_msg)
            await hook.delete()

    await bot.process_commands(message)


config_parser = configparser.ConfigParser()
config_parser.read("bot_config.ini")
key = config_parser["DEFAULT"]["key"]

bot.run(key)
