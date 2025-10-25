import os
import discord
from discord.ext import commands
import random
import string
import asyncio
from datetime import datetime, timedelta

class CodiguinhosBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.reactions = True
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        self.items_disponiveis = {
            "Calça Angelical (Azul)": "🎁",
            "Barbinha": "🧔",
            "Diamantes": "💎", 
            "Punho": "👊",
            "Cristal S...": "🔮",
            "RISTAL STIDRE": "🌟",
            "CUSTAL STORE": "🏪",
            "TESTAL STUNK": "📦",
            "RISAL STORE": "🛍️"
        }
        
        self.codigos_gerados = {}

    async def on_ready(self):
        print(f'✅ Bot {self.user.name} está online!')
        print(f'📊 Conectado em {len(self.guilds)} servidores')
        await self.change_presence(activity=discord.Game(name="!gerar para codiguinhos"))

    async def on_message(self, message):
        if message.author.bot:
            return
            
        if message.content.startswith('!gerar'):
            await self.show_item_selection(message.channel, message.author)
            
        await self.process_commands(message)

    async def show_item_selection(self, channel, user):
        selection_embed = discord.Embed(
            title="Gen Codiguinhos | Cristal Store",
            description="**APP** 00:50\nEscolha o item para gerar o codiguinho:",
            color=0xff9900
        )
        
        items_text = ""
        for item, emoji in list(self.items_disponiveis.items())[:5]:  # Mostrar apenas 5 itens
            items_text += f"{emoji} **{item}**\n"
        
        selection_embed.add_field(
            name="Escolha um item para gerar o codiguinho:",
            value=items_text,
            inline=False
        )
        
        selection_embed.set_footer(text="Só você pode ver esta mensagem • Ignorar mensagem 😊")
        
        selection_msg = await channel.send(f"{user.mention}", embed=selection_embed)
        
        # Adicionar reações para cada item
        for emoji in list(self.items_disponiveis.values())[:5]:
            await selection_msg.add_reaction(emoji)

    def generate_fake_code(self):
        formats = [
            "FF-{}{}{}-{}{}-GIFT",
            "GF-{}{}{}{}-{}{}{}-CODE", 
            "VIP-{}{}-{}{}{}-REWARD",
            "EVENT-{}{}{}-{}{}-BONUS"
        ]
        
        format_choice = random.choice(formats)
        code_parts = []
        
        for char in format_choice:
            if char == '{':
                if random.random() > 0.5:
                    code_parts.append(random.choice(string.ascii_uppercase))
                else:
                    code_parts.append(str(random.randint(0, 9)))
            elif char != '}':
                code_parts.append(char)
                
        return ''.join(code_parts)

# Configuração do bot
bot = CodiguinhosBot()

@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def itens(ctx):
    items_list = "\n".join([f"{emoji} {item}" for item, emoji in bot.items_disponiveis.items()])
    embed = discord.Embed(title="📦 Itens Disponíveis", description=items_list, color=0x00ff00)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ Token não encontrado! Configure a variável DISCORD_TOKEN")
