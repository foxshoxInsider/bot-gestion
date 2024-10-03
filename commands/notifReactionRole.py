import discord
from discord.ext import commands

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setup_reaction_roles')
    @commands.has_permissions(manage_roles=True)
    async def setup_reaction_roles(self, ctx):
        embed = discord.Embed(title="Roles notif", color=0x7289da)
        embed.add_field(name="🔮 Notif Twitch", value="Réagissez avec 💜 pour obtenir le rôle", inline=False)
        embed.add_field(name="🔮 Notif YouTube", value="Réagissez avec 🤍 pour obtenir le rôle", inline=False)

        message = await ctx.send(embed=embed)

        await message.add_reaction("💜")  # Réaction pour Notif Twitch
        await message.add_reaction("🤍")  # Réaction pour Notif YouTube

        await ctx.send("Les rôles de notification ont été configurés !")

        # Stockez l'ID du message pour le gérer dans la fonction on_reaction_add
        self.reaction_message_id = message.id

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        
        if reaction.message.id != self.reaction_message_id:
            return

        if str(reaction.emoji) == "💜":
            role = discord.utils.get(user.guild.roles, id=1209278048956981370)
            await user.add_roles(role)
            await user.send(f"Vous avez reçu le rôle {role.name} !")

        elif str(reaction.emoji) == "🤍":
            role = discord.utils.get(user.guild.roles, id=1209278050131517542)
            await user.add_roles(role)
            await user.send(f"Vous avez reçu le rôle {role.name} !")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return

        if reaction.message.id != self.reaction_message_id:
            return

        if str(reaction.emoji) == "💜":
            role = discord.utils.get(user.guild.roles, id=1209278048956981370)
            await user.remove_roles(role)
            await user.send(f"Vous avez retiré le rôle {role.name} !")

        elif str(reaction.emoji) == "🤍":
            role = discord.utils.get(user.guild.roles, id=1209278050131517542)
            await user.remove_roles(role)
            await user.send(f"Vous avez retiré le rôle {role.name} !")

async def setup(bot):
    await bot.add_cog(ReactionRole(bot))
