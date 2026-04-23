import discord
import os
from discord.ext import commands

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", "!")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# flag untuk auto reconnect
auto_reconnect = {}

@bot.event
async def on_ready():
    print(f"Login sebagai {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await channel.connect()
            auto_reconnect[ctx.guild.id] = {
                "enabled": False,
                "channel": channel
            }
            await ctx.send(f"Masuk ke voice channel {channel.name}")
        else:
            await ctx.voice_client.move_to(channel)
    else:
        await ctx.send("Masuk voice channel dulu.")

@bot.command()
async def autoreconnect(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        auto_reconnect[ctx.guild.id] = {
            "enabled": True,
            "channel": channel
        }
        await ctx.send("Auto reconnect aktif.")
    else:
        await ctx.send("Masuk voice channel dulu.")

@bot.event
async def on_voice_state_update(member, before, after):
    # cek apakah bot yang disconnect
    if member.id == bot.user.id:
        guild_id = member.guild.id

        if guild_id in auto_reconnect:
            data = auto_reconnect[guild_id]

            # jika auto reconnect aktif dan bot keluar channel
            if data["enabled"] and after.channel is None:
                try:
                    await data["channel"].connect()
                    print("Auto reconnect berhasil.")
                except Exception as e:
                    print(f"Gagal reconnect: {e}")

# handle command tidak dikenal
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Bawel lu banyak minta")

bot.run(TOKEN)
