import discord
import os
from discord.ext import commands

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", "!")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"Login sebagai {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
            await ctx.send(f"Masuk ke voice channel {channel.name}")
        else:
            await ctx.voice_client.move_to(channel)
    else:
        await ctx.send("Masuk voice channel dulu.")

bot.run(TOKEN)
