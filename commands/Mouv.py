import discord
from discord.ext import commands

class MouvCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mouv")
    @commands.has_permissions(administrator=True)  # Vérifie si l'utilisateur a les permissions d'administrateur
    async def move_members(self, ctx, channel_id: int):
        """Déplace tous les membres du canal vocal actuel vers le canal cible spécifié par l'ID."""
        # Vérifie si l'utilisateur est dans un canal vocal
        if ctx.author.voice:
            # Récupère le canal vocal actuel
            current_channel = ctx.author.voice.channel

            # Récupère le channel vocal cible avec l'ID donné
            target_channel = self.bot.get_channel(channel_id)

            if target_channel and isinstance(target_channel, discord.VoiceChannel):
                # Déplace tous les membres du canal vocal actuel vers le canal cible
                for member in current_channel.members:
                    await member.move_to(target_channel)
                await ctx.send(f"Tous les membres ont été déplacés vers {target_channel.name}.")
            else:
                await ctx.send("Channel introuvable ou n'est pas un canal vocal.")
        else:
            await ctx.send("Vous devez être dans un canal vocal pour utiliser cette commande.")

    @move_members.error
    async def move_members_error(self, ctx, error):
        """Gère les erreurs liées à la commande `!mouv`."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Vous devez être un administrateur pour utiliser cette commande.")

# Fonction setup pour enregistrer le cog
async def setup(bot):
    await bot.add_cog(MouvCommand(bot))
