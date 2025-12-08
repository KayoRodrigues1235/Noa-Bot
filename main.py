import os
import sys
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv


from events import setup_events

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('NoelNoa')

# Carrega variáveis de ambiente
load_dotenv()

class NoelNoaBot(commands.Bot):
    """Classe personalizada do bot Noel Noa"""
    
    def __init__(self):
        # Configuração de intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        
        super().__init__(
            command_prefix=['!', 'n!', 'noa!'],
            intents=intents,
            help_command=None,
            case_insensitive=True
        )
        
        self.logger = logger
        self.config = {
            'token': os.getenv('DISCORD_TOKEN'),
            'default_value': 10000,
            'owner_id': os.getenv('OWNER_ID', '')
        }
        
    async def setup_hook(self):
        """Configuração inicial do bot"""
        self.logger.info("🎮 Iniciando setup do Noel Noa...")
        
        # Carrega módulos/eventos
        await self.load_events()
        
        # Carregaria cogs aqui no futuro
        # await self.load_cogs()
        
        self.logger.info("✅ Setup completo!")
    
    async def load_events(self):
        """Carrega os eventos do bot"""
        try:
            # Se você tiver um arquivo events.py com eventos
            # from events import setup_events
            # setup_events(self)
            
            # Por enquanto, vamos definir eventos direto aqui
            self.logger.info("📥 Eventos carregados")
        except Exception as e:
            self.logger.error(f"❌ Erro ao carregar eventos: {e}")
    
    async def on_ready(self):
        """Evento quando o bot está pronto"""
        self.logger.info(f'⚽ {self.user.name} está online!')
        self.logger.info(f'📊 Conectado em {len(self.guilds)} servidor(es)')
        self.logger.info(f'🆔 ID do bot: {self.user.id}')
        self.logger.info('─' * 40)
        
        # Define status do bot
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="o Bastard München | !ajuda"
        )
        await self.change_presence(activity=activity)
    
    async def on_command_error(self, ctx, error):
        """Tratamento global de erros"""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignora comandos não encontrados silenciosamente
        
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 **Sem permissão** para executar este comando.")
        
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"⚠️ **Argumentos faltando:** `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`")
        
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ **Argumento inválido.** Verifique os valores informados.")
        
        else:
            self.logger.error(f"💥 Erro no comando {ctx.command}: {error}")
            await ctx.send("💥 **Erro interno.** Reporte aos administradores.")

# Cria instância do bot
bot = NoelNoaBot()

setup_events(
    bot,
    welcome_channel_id=1447582043000144003,  # ID do canal de boas-vindas
    log_channel_id=1447582067222118491       # ID do canal de logs
)


# ===== COMANDOS BÁSICOS =====
# Estes comandos ficam aqui temporariamente, depois vão para cogs

@bot.command(name='ping')
async def ping(ctx):
    """Testa a latência do bot"""
    latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latência: `{latency}ms`",
        color=0x00ff00
    )
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
    
    embed.add_field(name="💵 Valor de Mercado", value="$10,000", inline=True)
    embed.add_field(name="⚽ Time Atual", value="Time C", inline=True)
    embed.add_field(name="📈 Status", value="🟢 Ativo", inline=True)
    
    embed.set_thumbnail(url=membro.display_avatar.url)
    embed.set_footer(text="Use !registrar para entrar no sistema")
    
    await ctx.send(embed=embed)

@bot.command(name='noa')
async def noa(ctx):
    """Mensagem inspiradora do Noel Noa"""
    import random
    
    frases = [
        "Naquele campo, não há lugar para o futebol de cordões. Há apenas você e seu objetivo.",
        "Um gênio não é aquele que nasce com um dom, mas aquele que queima de desejo para se tornar um.",
        "Se você não é o melhor, então você é apenas mais um.",
        "No Bastard München, só os egos mais fortes sobrevivem.",
        "Mostre-me que você tem o que é preciso para brilhar."
    ]
    
    frase = random.choice(frases)
    
    embed = discord.Embed(
        title="🎙️ Noel Noa",
        description=f'*"{frase}"*',
        color=0xff6b00
    )
    
    await ctx.send(embed=embed)

@bot.command(name='ajuda')
async def ajuda(ctx):
    """Mostra os comandos disponíveis"""
    embed = discord.Embed(
        title="🏆 Comandos do Noel Noa",
        description="Sistema de rankeamento Blue Lock",
        color=0x1a75ff
    )
    
    embed.add_field(
        name="📊 Informações",
        value="• `!ping` - Testa o bot\n• `!info` - Seu status\n• `!noa` - Frase inspiradora",
        inline=False
    )
    
    embed.add_field(
        name="🎯 Sistema",
        value="• `!registrar [apelido]` - Entrar no sistema\n• `!ranking` - Ver top jogadores",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Administração",
        value="• `!premiar @jogador valor motivo`\n• `!promover` - Atualizar times",
        inline=False
    )
    
    embed.set_footer(text="Apenas os mais fortes sobrevivem no Bastard München")
    
    await ctx.send(embed=embed)

@bot.command(name='registrar')
async def registrar(ctx, *, apelido_jogo: str):
    """Registra um jogador no sistema"""
    # TODO: Implementar lógica de banco de dados
    
    embed = discord.Embed(
        title="✅ Registro Concluído!",
        description=f"**{ctx.author.display_name}** foi registrado como **{apelido_jogo}**",
        color=0x00ff00
    )
    
    embed.add_field(name="💵 Valor Inicial", value="$10,000", inline=True)
    embed.add_field(name="⚽ Time Inicial", value="Time C", inline=True)
    embed.add_field(name="🎯 Próximo Passo", value="Suba no ranking para entrar no Time Titular!", inline=False)
    
    embed.set_footer(text="Bem-vindo ao Bastard München!")
    
    await ctx.send(embed=embed)

# ===== PONTO DE ENTRADA =====
def main():
    """Função principal para iniciar o bot"""
    token = bot.config['token']
    
    if not token:
        logger.error("❌ DISCORD_TOKEN não encontrado no .env")
        logger.info("💡 Configure a variável de ambiente na Square Cloud")
        return
    
    try:
        logger.info("🚀 Iniciando Noel Noa Bot...")
        bot.run(token)
        
    except discord.LoginFailure:
        logger.error("❌ Token do Discord inválido")
    except KeyboardInterrupt:
        logger.info("👋 Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"💥 Erro fatal: {e}")

if __name__ == "__main__":
    main()