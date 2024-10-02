import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Initialisation des intents
intents = discord.Intents.all()

# Initialisation du bot
bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

    game = discord.Streaming(name="La Mayrature n'est jamais fini !", url="https://www.twitch.tv/mayradiblasi")
    await bot.change_presence(activity=game)

    # Charger toutes les commandes dans le dossier 'commands'
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
                print(f'Extension {filename} chargée avec succès.')
            except Exception as e:
                print(f'Erreur lors du chargement de {filename}: {e}')

if __name__ == '__main__':
    keep_alive()
    bot.run(token)
