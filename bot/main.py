"""
Noel Noa Bot - Versão Simplificada para Testes
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# load env 
load_dotenv()

class Config:
    TOKEN = os.getenv('DISCORD_TOKEN')
# ---

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=['!', 'n!'],
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')
    print(f'Conectado em {len(bot.guilds)} servidor')
    
    # Status
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="o Bastard München | !ajuda"
    )
    await bot.change_presence(activity=activity)

@bot.event
async def on_command_error(ctx, error):
    """Tratamento simples de erros"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando não encontrado. Use `!ajuda`")
    else:
        print(f"Erro: {error}")

# ===== COMANDOS BÁSICOS =====
@bot.command(name='ping')
async def ping(ctx):
    """Testa se o bot está respondendo"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'**Pong!** Latência: `{latency}ms`')

@bot.command(name='ajuda')
async def ajuda(ctx):
    """Mostra os comandos disponíveis"""
    embed = discord.Embed(
        title="Noel Noa - Comandos Básicos",
        description="Sistema de rankeamento Blue Lock",
        color=0x1a75ff
    )
    
    embed.add_field(
        name="Comandos de Teste",
        value="`!ping` - Testa o bot\n`!ajuda` - Esta mensagem\n`!info` - Sua info",
        inline=False
    )
    
    embed.add_field(
        name="Comandos do Sistema", 
        value="`!registrar [apelido]` - Entrar no sistema\n`!valor` - Seu valor atual",
        inline=False
    )
    
    embed.set_footer(text="Apenas os mais fortes sobrevivem")
    await ctx.send(embed=embed)

@bot.command(name='info')
async def info(ctx, membro: discord.Member = None):
    """Mostra informações de um jogador"""
    if membro is None:
        membro = ctx.author
    
    embed = discord.Embed(
        title=f"📊 Análise do Jogador: {membro.display_name}",
        color=0x00ff00
    )
    
    embed.add_field(name="Valor de Mercado", value="$10,000", inline=True)
    embed.add_field(name="Time Atual", value="Time C", inline=True)
    embed.add_field(name="Posição", value="#--", inline=True)
    embed.add_field(name="Status", value="Não registrado", inline=True)
    
    embed.set_thumbnail(url=membro.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name='registrar')
async def registrar(ctx, *, apelido_jogo: str):
    """Registra um jogador no sistema"""
    embed = discord.Embed(
        title="✅ Registro Concluído!",
        description=f"**{ctx.author.display_name}** foi registrado como **{apelido_jogo}**",
        color=0x00ff00
    )
    
    embed.add_field(name="Valor Inicial", value="$10,000", inline=True)
    embed.add_field(name="Time Inicial", value="Time C", inline=True)
    embed.add_field(name="Próximo Passo", value="Use `!info` para ver seu status", inline=False)
    
    embed.set_footer(text="Bem-vindo ao Bastard München!")
    await ctx.send(embed=embed)

@bot.command(name='valor')
async def valor(ctx):
    """Mostra seu valor atual"""
    embed = discord.Embed(
        title="Seu Valor de Mercado",
        description=f"**{ctx.author.display_name}**",
        color=0xffd700
    )
    
    embed.add_field(name="Valor Atual", value="$10,000", inline=True)
    embed.add_field(name="Variação", value="+$0 (estável)", inline=True)
    embed.add_field(name="Meta", value="$50,000 para Time Titular", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='noa')
async def noa(ctx):
    """Mensagem inspiradora do Noel Noa"""
    frases = [
        "Naquele campo, não há lugar para o futebol de cordões. Há apenas você e seu objetivo.",
        "Um gênio não é aquele que nasce com um dom, mas aquele que queima de desejo para se tornar um.",
        "Se você não é o melhor, então você é apenas mais um.",
        "No Bastard München, só os egos mais fortes sobrevivem.",
        "Mostre-me que você tem o que é preciso para brilhar."
    ]
    
    import random
    frase = random.choice(frases)
    
    embed = discord.Embed(
        title="Noel Noa",
        description=f'*"{frase}"*',
        color=0xff6b00
    )
    
    await ctx.send(embed=embed)

# admin only
@bot.command(name='premiar')
@commands.has_permissions(administrator=True)
async def premiar(ctx, membro: discord.Member, valor: int, *, motivo):
    embed = discord.Embed(
        title="Prêmio Concedido!",
        description=f"**{membro.display_name}** foi premiado",
        color=0x00ff00
    )
    
    embed.add_field(name="Valor", value=f"${valor:,}", inline=True)
    embed.add_field(name="Motivo", value=motivo, inline=True)
    embed.add_field(name="Admin", value=ctx.author.display_name, inline=True)
    
    await ctx.send(embed=embed)


# init
def main():
    token = Config.TOKEN
    
    if not token:
        print("Token não encontrado")
        return
    
    try:
        print("Iniciando Noel Noa.")
        bot.run(token)
    except discord.LoginFailure:
        print("Token inválido")
    except KeyboardInterrupt:
        print("Bot interrompido")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()