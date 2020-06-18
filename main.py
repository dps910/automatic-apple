__authors__ = 'aejb'

## requires d.py 1.0
## requires python3.6
import discord
from discord.ext import commands
from traceback import print_exc
from sys import stderr
from datetime import datetime
import pickledb


initial_extensions = ['cog', 'apple']


def gettoken():
    token_file = open("token.txt", "r")
    token_string = token_file.read()
    token_token = token_string.split("\n")
    bot_token = str(token_token[0])
    return bot_token


bot_token = gettoken()

description = "here to help with your apples."
bot = commands.Bot(command_prefix=["apl "], description=description)
now = datetime.now()

if __name__ == '__main__':
    for extension in initial_extensions:
        # noinspection PyBroadException
        try:
            bot.load_extension(extension)
        except Exception as e:
            print("Failed to load" + extension, file=stderr)
            print_exc()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That command does not exist, or the cog did not properly load.')
        await ctx.message.add_reaction('\N{CROSS MARK}')
    else:
        raise error


@bot.event
async def on_message_delete(ctx):
    await ctx.guild.get_channel(695630766477934632).send(
        f"Message by {ctx.author} deleted from {ctx.channel_name} at {now.strftime('%I:%M:%S %p')}\n > {discord.utils.escape_markdown(ctx.content)}"
    )


@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.content==after.content: return
    if len(str(discord.utils.escape_markdown(before.content))) < 2000 and len(
            str(discord.utils.escape_markdown(after.content))) < 2000:
        now = datetime.now()
        await before.guild.get_channel(695630766477934632).send(
            f"""
            Message by {before.author} edited in {before.channel.name} at {now.strftime('%I:%M:%S %p')}\n**Before:**\n> 
            {discord.utils.escape_markdown(before.content)}\n**After:**\n>{discord.utils.escape_markdown(after.content)}
            """
        )
    else:
        now = datetime.now()
        await before.guild.get_channel(695630766477934632).send(
            f"""
            Message by {before.author} edited in {before.channel_name} 
            at {now.strftime('%I:%M:%S %p')}
            """
        )
        await before.guild.get_channel(695630766477934632).send(f"**Before**\n> {discord.utils.escape_markdown(before.content)}")

        await before.guild.get_channel(695630766477934632).send(f"**After**\n> {discord.utils.escape_markdown(after.content)}")

@bot.event
async def on_member_join(member: discord.Member):
    now = datetime.now()
    await member.guild.get_channel(695630766477934632).send(f"User {member} with ID {member.id} joined at {now.strftime('%I:%M:%S %p')} :D")

@bot.event
async def on_member_remove(member: discord.Member):
    now = datetime.now()
    await member.guild.get_channel(695630766477934632).send(f"User {member} with ID {member.id} left at {now.strftime('%I:%M:%S %p')} :(")

bot.run(bot_token)
