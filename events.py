"""
events.py - Sistema de Eventos do Noel Noa
Gerencia todos os eventos do Discord para o bot
"""

import discord
import asyncio
import random
from datetime import datetime, timedelta
from typing import Optional

# ========== CONFIGURAÇÃO DE EVENTOS ==========

class EventSystem:
    """Sistema principal de eventos"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.welcome_channel_id = None  # Configure no setup
        self.log_channel_id = None      # Configure no setup
        
        # Cache para controle de spam
        self.message_cache = {}
        self.user_warnings = {}
        
        # Lista de palavras proibidas (adicione mais conforme necessário)
        self.banned_words = [
            # Palavrões/linguagem ofensiva
            'palavrao1', 'palavrao2', 'xingamento',
            
            # Conteúdo inapropriado para menores
            'conteudo+18', 'nsfw',
            
            # Discursos de ódio
            'racista', 'homofobico', 'preconceito',
            
            # Spam/auto-promoção
            'discord.gg/', 'convite', 'meu servidor',
        ]
        
        # Mensagens de boas-vindas personalizadas
        self.welcome_messages = [
            "Bem-vindo ao Bastard München, {member.mention}! Mostre-nos seu ego!",
            "Um novo diamante bruto chegou! {member.mention}, está pronto para ser lapidado?",
            "Olá {member.mention}! No Bastard München, apenas os mais fortes sobrevivem. Prove seu valor!",
            "Mais um jogador entra em campo! {member.mention}, use `!registrar` para começar sua jornada.",
            "Ego detectado! {member.mention} acaba de entrar no Bastard München."
        ]
        
        # Frases do Noel Noa para eventos
        self.noa_quotes = [
            "Naquele campo, não há lugar para o futebol de cordões. Há apenas você e seu objetivo.",
            "Um gênio não é aquele que nasce com um dom, mas aquele que queima de desejo para se tornar um.",
            "Se você não é o melhor, então você é apenas mais um.",
            "No Bastard München, só os egos mais fortes sobrevivem.",
            "Mostre-me que você tem o que é preciso para brilhar.",
            "A vitória não é um acidente. É uma escolha.",
            "Não importa o quão talentoso você seja, sem trabalho duro é apenas potencial desperdiçado.",
            "O verdadeiro egoísmo é buscar ser o melhor, não apenas para si, mas acima de todos.",
            "Cada falha é uma lição. Cada derrota, um degrau.",
            "O campo é um espelho. Ele reflete exatamente quem você é."
        ]

# ========== FUNÇÕES DE SETUP ==========

def setup_events(bot, welcome_channel_id=None, log_channel_id=None):
    """
    Configura todos os eventos no bot
    
    Args:
        bot: Instância do bot
        welcome_channel_id: ID do canal de boas-vindas
        log_channel_id: ID do canal de logs
    """
    
    
    event_system = EventSystem(bot)
    event_system.welcome_channel_id = welcome_channel_id
    event_system.log_channel_id = log_channel_id
    
    # Atribui os handlers de eventos
    bot.event_system = event_system
    
    # Registra os eventos
    @bot.event
    async def on_ready():
        """Chamado quando o bot está pronto"""
        await event_system.handle_ready()
    
    @bot.event
    async def on_member_join(member):
        """Chamado quando um novo membro entra no servidor"""
        await event_system.handle_member_join(member)
    
    @bot.event
    async def on_member_remove(member):
        """Chamado quando um membro sai do servidor"""
        await event_system.handle_member_remove(member)
    
    @bot.event
    async def on_message(message):
        """Chamado quando uma mensagem é enviada"""
        await event_system.handle_message(message)
    
    @bot.event
    async def on_message_edit(before, after):
        """Chamado quando uma mensagem é editada"""
        await event_system.handle_message_edit(before, after)
    
    @bot.event
    async def on_message_delete(message):
        """Chamado quando uma mensagem é deletada"""
        await event_system.handle_message_delete(message)
    
    @bot.event
    async def on_command_completion(ctx):
        """Chamado quando um comando é executado com sucesso"""
        await event_system.handle_command_completion(ctx)
    
    @bot.event
    async def on_member_update(before, after):
        """Chamado quando um membro é atualizado"""
        await event_system.handle_member_update(before, after)
    
    bot.logger.info("✅ Sistema de eventos configurado")

# ========== HANDLERS DE EVENTOS ==========

async def handle_ready(self):
    """Handler para o evento on_ready"""
    self.logger.info(f'⚽ {self.bot.user.name} está online!')
    self.logger.info(f'📊 Conectado em {len(self.bot.guilds)} servidor(es)')
    self.logger.info('─' * 40)
    
    # Define status do bot
    activities = [
        discord.Activity(type=discord.ActivityType.watching, name="o Bastard München"),
        discord.Activity(type=discord.ActivityType.playing, name="Blue Lock Project"),
        discord.Activity(type=discord.ActivityType.listening, name="!ajuda")
    ]
    
    activity = random.choice(activities)
    await self.bot.change_presence(activity=activity)
    
    # Inicia tarefa de rotação de status
    self.bot.loop.create_task(self.rotate_status())

async def handle_member_join(self, member):
    """Handler para quando um membro entra"""
    self.logger.info(f'👤 {member.name} ({member.id}) entrou no servidor')
    
    # Envia mensagem de boas-vindas
    if self.welcome_channel_id:
        channel = self.bot.get_channel(self.welcome_channel_id)
        if channel:
            welcome_msg = random.choice(self.welcome_messages)
            embed = discord.Embed(
                title="🎉 Bem-vindo ao Bastard München!",
                description=welcome_msg.format(member=member),
                color=0x00ff00
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.add_field(
                name="Primeiros Passos",
                value="1. Leia as regras\n2. Use `!registrar [apelido]`\n3. Prove seu valor!",
                inline=False
            )
            
            await channel.send(embed=embed)
    
    # Log no canal de logs
    await self.log_event(
        title="👤 Novo Membro",
        description=f"{member.mention} ({member.id}) entrou no servidor",
        color=0x00ff00
    )
    
    # Mensagem direta (opcional)
    try:
        embed = discord.Embed(
            title="Bem-vindo ao Bastard München!",
            description="Eu sou Noel Noa, líder deste time. Aqui, apenas os mais fortes sobrevivem.\n\n"
                       "**Para começar:**\n"
                       "1. Leia as regras do servidor\n"
                       "2. Use `!registrar [seu_apelido]` para entrar no sistema\n"
                       "3. Participe dos jogos para aumentar seu valor\n\n"
                       "Que seu ego brilhe!",
            color=0x1a75ff
        )
        await member.send(embed=embed)
    except:
        pass  # Usuário tem DM fechada

async def handle_member_remove(self, member):
    """Handler para quando um membro sai"""
    self.logger.info(f'👋 {member.name} ({member.id}) saiu do servidor')
    
    await self.log_event(
        title="👋 Membro Saiu",
        description=f"{member.mention} ({member.id}) deixou o servidor",
        color=0xff9900
    )

async def handle_message(self, message):
    """Handler para novas mensagens"""
    # Ignora mensagens do bot
    if message.author == self.bot.user:
        return
    
    # Controle de spam
    if await self.check_spam(message):
        return
    
    # Filtro de conteúdo
    if await self.check_content(message):
        return
    
    # Respostas automáticas para menções
    if self.bot.user in message.mentions:
        await self.handle_mention(message)
    
    # Processa comandos normalmente
    await self.bot.process_commands(message)

async def handle_message_edit(self, before, after):
    """Handler para mensagens editadas"""
    if before.content == after.content:
        return
    
    # Verifica se a edição adicionou conteúdo proibido
    if await self.check_content(after, is_edit=True):
        return
    
    # Log de edições importantes
    if len(before.content) > 10 and len(after.content) > 10:
        await self.log_event(
            title="📝 Mensagem Editada",
            description=f"**Autor:** {before.author.mention}\n"
                       f"**Canal:** {before.channel.mention}\n"
                       f"**Antes:** {before.content[:100]}...\n"
                       f"**Depois:** {after.content[:100]}...",
            color=0xffff00
        )

async def handle_message_delete(self, message):
    """Handler para mensagens deletadas"""
    # Ignora mensagens do bot
    if message.author == self.bot.user:
        return
    
    # Log de deleção
    await self.log_event(
        title="🗑️ Mensagem Deletada",
        description=f"**Autor:** {message.author.mention}\n"
                   f"**Canal:** {message.channel.mention}\n"
                   f"**Conteúdo:** {message.content[:150]}{'...' if len(message.content) > 150 else ''}",
        color=0xff0000
    )

async def handle_command_completion(self, ctx):
    """Handler para comandos completados"""
    self.logger.info(f'✅ Comando executado: {ctx.command} por {ctx.author}')

async def handle_member_update(self, before, after):
    """Handler para atualizações de membro"""
    # Detecta mudança de nome
    if before.display_name != after.display_name:
        await self.log_event(
            title="🏷️ Nome Alterado",
            description=f"{before.mention} mudou de nome\n"
                       f"**De:** {before.display_name}\n"
                       f"**Para:** {after.display_name}",
            color=0x00ccff
        )
    
    # Detecta mudança de avatar
    if before.avatar != after.avatar:
        await self.log_event(
            title="🖼️ Avatar Alterado",
            description=f"{after.mention} mudou de avatar",
            color=0x00ccff
        )

# ========== FUNÇÕES AUXILIARES ==========

async def check_spam(self, message) -> bool:
    """Verifica e previne spam"""
    user_id = message.author.id
    now = datetime.now()
    
    # Inicializa cache para o usuário
    if user_id not in self.message_cache:
        self.message_cache[user_id] = []
    
    # Limpa mensagens antigas (últimos 5 segundos)
    self.message_cache[user_id] = [
        msg_time for msg_time in self.message_cache[user_id]
        if (now - msg_time).seconds < 5
    ]
    
    # Adiciona nova mensagem
    self.message_cache[user_id].append(now)
    
    # Se mais de 5 mensagens em 5 segundos = spam
    if len(self.message_cache[user_id]) > 5:
        await message.delete()
        
        # Aviso
        warning = await message.channel.send(
            f"🚫 {message.author.mention}, muito rápido! Aguarde alguns segundos.",
            delete_after=5
        )
        
        # Log
        await self.log_event(
            title="⚠️ Spam Detectado",
            description=f"**Usuário:** {message.author.mention}\n"
                       f"**Mensagens:** {len(self.message_cache[user_id])} em 5 segundos",
            color=0xff6600
        )
        
        return True
    
    return False

async def check_content(self, message, is_edit=False) -> bool:
    """Verifica conteúdo inapropriado"""
    content_lower = message.content.lower()
    
    # Verifica palavras proibidas
    for word in self.banned_words:
        if word in content_lower:
            await message.delete()
            
            # Conta infrações
            user_id = message.author.id
            if user_id not in self.user_warnings:
                self.user_warnings[user_id] = 0
            
            self.user_warnings[user_id] += 1
            warnings = self.user_warnings[user_id]
            
            # Ação baseada no número de infrações
            action_msg = "🚫 Linguagem inapropriada não é permitida!"
            
            if warnings == 2:
                action_msg += " **Segundo aviso!**"
            elif warnings >= 3:
                action_msg += " **Mute aplicado!**"
                # Aplicaria mute aqui
                # await self.apply_mute(message.author, 300)  # 5 minutos
            
            warning = await message.channel.send(
                f"{message.author.mention}, {action_msg}",
                delete_after=10
            )
            
            # Log
            await self.log_event(
                title="🚫 Conteúdo Inapropriado",
                description=f"**Usuário:** {message.author.mention}\n"
                           f"**Canal:** {message.channel.mention}\n"
                           f"**Conteúdo:** {message.content[:100]}...\n"
                           f"**Infrações:** {warnings}",
                color=0xff0000
            )
            
            return True
    
    # Verifica links suspeitos
    if "http://" in content_lower or "https://" in content_lower:
        # Lista de domínios permitidos (adicione mais conforme necessário)
        allowed_domains = ['discord.com', 'youtube.com', 'twitch.tv', 'github.com']
        
        import re
        urls = re.findall(r'https?://[^\s]+', content_lower)
        
        for url in urls:
            if not any(domain in url for domain in allowed_domains):
                await message.delete()
                
                warning = await message.channel.send(
                    f"🔗 {message.author.mention}, links não verificados não são permitidos.",
                    delete_after=10
                )
                
                return True
    
    return False

async def handle_mention(self, message):
    """Responde quando o bot é mencionado"""
    # Remove a menção do conteúdo
    content = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
    
    if not content:  # Apenas mencionou
        response = random.choice([
            "Sim? Use `!ajuda` para ver meus comandos.",
            "Noel Noa presente. O que precisa?",
            "Me chamou? Use `!info` para ver seu status.",
            "Estou observando. Use `!noa` para uma frase inspiradora."
        ])
        await message.channel.send(response)

async def log_event(self, title: str, description: str, color: int):
    """Registra eventos no canal de logs"""
    if not self.log_channel_id:
        return
    
    channel = self.bot.get_channel(self.log_channel_id)
    if not channel:
        return
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now()
    )
    
    # Adiciona footer com data formatada
    embed.set_footer(text="Sistema de Logs • Bastard München")
    
    await channel.send(embed=embed)

async def rotate_status(self):
    """Rotaciona o status do bot periodicamente"""
    await self.bot.wait_until_ready()
    
    statuses = [
        {"type": "watching", "text": "o Bastard München"},
        {"type": "playing", "text": "Blue Lock Project"},
        {"type": "listening", "text": "!ajuda para comandos"},
        {"type": "watching", "text": f"{len(self.bot.guilds)} servidor(es)"},
        {"type": "competing", "text": "Ranking dos Egocentristas"}
    ]
    
    while not self.bot.is_closed():
        for status in statuses:
            if self.bot.is_closed():
                break
            
            activity_type = getattr(discord.ActivityType, status["type"])
            activity = discord.Activity(type=activity_type, name=status["text"])
            
            await self.bot.change_presence(activity=activity)
            await asyncio.sleep(30)  # Muda a cada 30 segundos

# Atribui os métodos à classe
EventSystem.handle_ready = handle_ready
EventSystem.handle_member_join = handle_member_join
EventSystem.handle_member_remove = handle_member_remove
EventSystem.handle_message = handle_message
EventSystem.handle_message_edit = handle_message_edit
EventSystem.handle_message_delete = handle_message_delete
EventSystem.handle_command_completion = handle_command_completion
EventSystem.handle_member_update = handle_member_update
EventSystem.check_spam = check_spam
EventSystem.check_content = check_content
EventSystem.handle_mention = handle_mention
EventSystem.log_event = log_event
EventSystem.rotate_status = rotate_status