import discord
from discord.ext import commands
from discord.ui import Button, View

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reactionrole')
    @commands.has_permissions(administrator=True)  # Vérifie si l'utilisateur est administrateur
    async def create_reaction_role(self, ctx, role: discord.Role):
        """Crée un message de bouton pour attribuer un rôle de vérification"""
        
        # Créer un embed
        embed = discord.Embed(
            title="**Rôle de Vérification**",  # Titre en gras
            description=f"Appuyez sur le bouton ci-dessous pour obtenir le rôle {role.name}.",
            color=discord.Color.from_rgb(255, 255, 255)  # Couleur RGB
        )

        # Créer le bouton
        button = Button(label="Obtenir le rôle", style=discord.ButtonStyle.grey)

        async def button_callback(interaction: discord.Interaction):
            # Vérifie si l'utilisateur a déjà le rôle
            member = interaction.user
            if role in member.roles:
                await member.send("Vous avez déjà ce rôle.")
            else:
                await member.add_roles(role)
                await interaction.response.send_message(f"Vous avez obtenu le rôle {role.name}.", ephemeral=True)

        button.callback = button_callback  # Lier la fonction de callback au bouton

        # Créer une vue pour contenir le bouton
        view = View()
        view.add_item(button)

        # Envoie l'embed avec le bouton
        await ctx.send(embed=embed, view=view)

# Fonction setup pour enregistrer le cog
async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
