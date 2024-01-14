import discord
import os
from dotenv import load_dotenv
from guild_manager import GuildManager


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

INTENTS = discord.Intents.default()

bot = discord.Bot(intents=INTENTS)
bot.guild_manager = GuildManager('config.json')


@bot.event
async def on_ready():
    print('Bot-C is online.')


@bot.event
async def on_guild_join(guild):
    bot.guild_manager.register_guild(guild.id)
    await guild.system_channel.send("Here and ready to put some blood on the clocktower 😈 (or whatever, I haven't played the game).")


@bot.event
async def on_guild_remove(guild):
    bot.guild_manager.unregister_guild(guild.id)


bot.load_extension('cogs.server_settings')
bot.load_extension('cogs.phase_shifts')
bot.load_extension('cogs.countdowns')
bot.load_extension('cogs.misc')


bot.run(TOKEN)
