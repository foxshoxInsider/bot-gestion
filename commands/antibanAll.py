import discord
from discord.ext import commands
import asyncio
from collections import defaultdict
import time

class Antiban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bans_tracker = defaultdict(list)  # Dictionnaire pour garder la trace des bans

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        # Obtenez les logs de la guilde
        audit_logs = await guild.audit_logs(limit=5, action=discord.AuditLogAction.ban).flatten()
        
        # Recherchez l'utilisateur qui a effectué le ban
        executor = None
        for entry in audit_logs:
            if entry.target.id == user.id:
                executor = entry.user  # L'utilisateur qui a effectué le ban
                break
        
        if executor is None:
            return  # Aucun ban trouvé

        # Ajoutons le ban à notre tracker
        current_time = time.time()
        self.bans_tracker[executor.id].append(current_time)

        # Nettoyage des anciens bans
        self.bans_tracker[executor.id] = [t for t in self.bans_tracker[executor.id] if current_time - t < 60]

        # Vérifiez si l'utilisateur a banni plus de 4 personnes en moins de 60 secondes
        if len(self.bans_tracker[executor.id]) > 4:
            await guild.kick(executor)
            print(f"{executor.name} a été kické pour avoir banni trop de personnes en peu de temps.")

# Fonction setup pour enregistrer le cog
async def setup(bot):
    await bot.add_cog(Antiban(bot))
