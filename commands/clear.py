import discord
from discord.ext import commands

class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, arg1=None, member: discord.Member = None):
        if arg1 is None:
            await ctx.send("Veuillez spécifier un nombre de messages à supprimer, 'all' pour tout supprimer, ou mentionner un utilisateur.")
            return

        if arg1.lower() == 'all':
            if member:
                await self.clear_all_messages_from_user(ctx, member)
            else:
                await self.clear_all_messages(ctx)
        
        elif arg1.isdigit():
            num_messages = int(arg1)
            if member:
                await self.clear_messages_from_user(ctx, member, num_messages)
            else:
                await self.clear_number_of_messages(ctx, num_messages)
        else:
            await ctx.send("Argument non valide. Utilisez un nombre ou 'all'.")

    async def clear_number_of_messages(self, ctx, num_messages: int):
        await ctx.channel.purge(limit=num_messages + 1)
        await ctx.send(f"{num_messages} messages supprimés.", delete_after=5)

    async def clear_all_messages(self, ctx):
        await ctx.channel.purge()
        await ctx.send("Tous les messages ont été supprimés.", delete_after=5)

    async def clear_messages_from_user(self, ctx, member: discord.Member, num_messages: int):
        def check(msg):
            return msg.author == member

        deleted = await ctx.channel.purge(limit=num_messages + 1, check=check)
        await ctx.send(f"{len(deleted) - 1} messages de {member.display_name} supprimés.", delete_after=5)

    async def clear_all_messages_from_user(self, ctx, member: discord.Member):
        def check(msg):
            return msg.author == member

        deleted = await ctx.channel.purge(check=check)
        await ctx.send(f"Tous les messages de {member.display_name} ont été supprimés.", delete_after=5)

async def setup(bot):
    await bot.add_cog(ClearCommand(bot))