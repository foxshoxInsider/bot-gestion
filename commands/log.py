import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Log des messages envoyés dans le chat
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        log_channel = self.bot.get_channel(1209278082930835486)  # Canal de log chat
        if log_channel and not message.author.bot:
            embed = discord.Embed(
                title="Nouveau message",
                description=message.content,
                color=discord.Color.green()
            )
            embed.add_field(name="Auteur", value=message.author.mention)
            embed.add_field(name="Salon", value=message.channel.mention)
            embed.set_footer(text=f"ID du message: {message.id} | Heure: {message.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            await log_channel.send(embed=embed)

    # Log des messages supprimés
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        log_channel = self.bot.get_channel(1209278082930835486)  # Canal de log chat
        if log_channel and message.author:
            embed = discord.Embed(
                title="Message supprimé",
                description=message.content,
                color=discord.Color.red()
            )
            embed.add_field(name="Auteur", value=message.author.mention)
            embed.add_field(name="Salon", value=message.channel.mention)
            embed.set_footer(text=f"ID du message: {message.id} | Heure: {message.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            await log_channel.send(embed=embed)

    # Log des membres qui rejoignent ou quittent un canal vocal
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        log_channel = self.bot.get_channel(1209278084600045599)  # Canal de log vocal
        if log_channel:
            if before.channel is None and after.channel is not None:
                embed = discord.Embed(
                    title="Membre a rejoint un canal vocal",
                    description=f"{member.mention} a rejoint {after.channel.name}",
                    color=discord.Color.blue()
                )
                await log_channel.send(embed=embed)
            elif before.channel is not None and after.channel is None:
                embed = discord.Embed(
                    title="Membre a quitté un canal vocal",
                    description=f"{member.mention} a quitté {before.channel.name}",
                    color=discord.Color.red()
                )
                await log_channel.send(embed=embed)
            elif before.channel != after.channel:
                embed = discord.Embed(
                    title="Membre a changé de canal vocal",
                    description=f"{member.mention} a changé de {before.channel.name} à {after.channel.name}",
                    color=discord.Color.orange()
                )
                await log_channel.send(embed=embed)

    # Log des rôles qui sont attribués ou retirés
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        log_channel = self.bot.get_channel(1213579045338611732)  # Canal de log serveur
        if log_channel:
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]

            if added_roles:
                roles_names = ', '.join(role.name for role in added_roles)
                embed = discord.Embed(
                    title="Rôles ajoutés",
                    description=f"{after.mention} a reçu le(s) rôle(s) : {roles_names}",
                    color=discord.Color.green()
                )
                await log_channel.send(embed=embed)

            if removed_roles:
                roles_names = ', '.join(role.name for role in removed_roles)
                embed = discord.Embed(
                    title="Rôles retirés",
                    description=f"{after.mention} a perdu le(s) rôle(s) : {roles_names}",
                    color=discord.Color.red()
                )
                await log_channel.send(embed=embed)

    # Log des modifications du serveur
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        log_channel = self.bot.get_channel(1213579045338611732)  # Canal de log serveur
        if log_channel:
            if before.name != after.name:
                embed = discord.Embed(
                    title="Nom du serveur modifié",
                    description=f"Le nom du serveur a été changé de **{before.name}** à **{after.name}**",
                    color=discord.Color.purple()
                )
                await log_channel.send(embed=embed)

            if before.icon != after.icon:
                embed = discord.Embed(
                    title="Icône du serveur modifiée",
                    description="L'icône du serveur a été changée.",
                    color=discord.Color.purple()
                )
                await log_channel.send(embed=embed)

    # Log des canaux créés ou supprimés
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_channel = self.bot.get_channel(1213579045338611732)  # Canal de log serveur
        if log_channel:
            embed = discord.Embed(
                title="Canal créé",
                description=f"Le canal **{channel.name}** a été créé.",
                color=discord.Color.green()
            )
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = self.bot.get_channel(1213579045338611732)  # Canal de log serveur
        if log_channel:
            embed = discord.Embed(
                title="Canal supprimé",
                description=f"Le canal **{channel.name}** a été supprimé.",
                color=discord.Color.red()
            )
            await log_channel.send(embed=embed)

# Fonction setup pour enregistrer le cog
async def setup(bot):
    await bot.add_cog(Logs(bot))
