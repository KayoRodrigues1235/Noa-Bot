import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# INTENTS CORRETOS
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} está online!')
    activity = discord.Activity(type=discord.ActivityType.watching, name="Bastard München")
    await bot.change_presence(activity=activity)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! {latency}ms')

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"📊 {ctx.author.display_name}", color=0x00ff00)
    embed.add_field(name="💵 Valor", value="$10,000", inline=True)
    embed.add_field(name="⚽ Time", value="Time C", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def noa(ctx):
    await ctx.send('🎙️ **Noel Noa**: "Apenas os mais fortes sobrevivem no Bastard München!"')

if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_TOKEN'))