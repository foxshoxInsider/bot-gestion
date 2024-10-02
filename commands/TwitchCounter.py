import discord
from discord.ext import commands, tasks
import aiohttp
from bs4 import BeautifulSoup

TWITCHTRACKER_URL = "https://socialblade.com/twitch/user/mayradiblasi/realtime"

class TwitchCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_follower_channel.start()  # Démarre la tâche périodique au démarrage du bot

    # Fonction pour récupérer le nombre de followers
    async def get_twitch_follower_count(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(TWITCHTRACKER_URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
                if response.status == 200:
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # Extrait le nombre de followers
                    followers_tag = soup.find('p', id='rawCount')
                    if followers_tag:
                        return int(followers_tag.text.strip())
                    else:
                        print("Impossible de trouver le nombre de followers.")
                        return 0
                else:
                    print(f"Erreur lors de la requête: {response.status}")
                    return 0

    # Tâche périodique qui met à jour le nom du channel
    @tasks.loop(minutes=5)
    async def update_follower_channel(self):
        follower_count = await self.get_twitch_follower_count()

        if follower_count > 0:
            channel = self.bot.get_channel(1290645185193185361)  # Remplace par ton ID de channel
            if channel:
                new_channel_name = f"Followers Twitch: {follower_count}"
                await channel.edit(name=new_channel_name)
                
                # Indique dans le terminal que la mise à jour a été effectuée
                print(f"Counter mis à jour : {follower_count} followers.")
            else:
                print("Channel introuvable.")
        else:
            print("Impossible de récupérer le nombre de followers.")

    # Méthode pour stopper la tâche périodique si nécessaire
    def cog_unload(self):
        self.update_follower_channel.cancel()

# Fonction setup pour enregistrer le cog (asynchrone)
async def setup(bot):
    await bot.add_cog(TwitchCounter(bot))
