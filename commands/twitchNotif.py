import discord
from discord.ext import commands, tasks
import aiohttp
from bs4 import BeautifulSoup

TWITCH_USER_NAME = 'mayradiblasi'  # Nom d'utilisateur Twitch
CHANNEL_ID = 1209278061837688852  # Remplacez par l'ID de votre canal Discord

class TwitchNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_live = False  # Pour suivre l'état de streaming
        self.session = aiohttp.ClientSession()
        self.check_stream_status.start()  # Démarrer la tâche périodique

    async def check_if_live(self):
        url = f'https://www.twitch.tv/{TWITCH_USER_NAME}'
        async with self.session.get(url) as response:
            if response.status == 200:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')

                # Vérifie si la balise pour le statut du stream est présente
                stream_status = soup.find('div', class_='live')
                return stream_status is not None  # Si la balise existe, l'utilisateur est en direct
            else:
                print(f"Erreur lors de la récupération de la page Twitch : {response.status}")
                return False

    @tasks.loop(minutes=1)
    async def check_stream_status(self):
        live_status = await self.check_if_live()
        if live_status and not self.is_live:
            self.is_live = True
            await self.send_live_notification()
        elif not live_status and self.is_live:
            self.is_live = False

    async def send_live_notification(self):
        channel = self.bot.get_channel(CHANNEL_ID)
        if channel:
            button = discord.ui.Button(label='Rejoindre le stream', url=f'https://www.twitch.tv/{TWITCH_USER_NAME}')
            view = discord.ui.View()
            view.add_item(button)

            embed = discord.Embed(
                title=f"{TWITCH_USER_NAME} est maintenant en live !",
                description="Cliquez sur le bouton ci-dessous pour rejoindre le stream.",
                color=discord.Color.green()
            )
            await channel.send(embed=embed, view=view)

    def cog_unload(self):
        self.check_stream_status.cancel()
        self.session.close()

# Fonction setup pour enregistrer le cog
async def setup(bot):
    await bot.add_cog(TwitchNotifier(bot))
