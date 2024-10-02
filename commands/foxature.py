import discord
from discord.ext import commands
import asyncio

class Foxature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        elif message.content.startswith("foxature"):
            bot_message = await message.channel.send("Un coup d'etat approche ...")

            await asyncio.sleep(1)
            await message.delete()  
            await bot_message.delete()


# Fonction setup pour enregistrer le cog
async def setup(bot):
    await bot.add_cog(Foxature(bot))
