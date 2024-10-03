import discord
from discord.ext import commands
import asyncio

class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, arg1=None, member: discord.Member = None):
        user_id = ctx.author.id
        now = asyncio.get_event_loop().time()

        cooldown_duration = 10
        if user_id in self.cooldowns:
            expiration_time = self.cooldowns[user_id]
            if now < expiration_time:
                time_left = expiration_time - now
                return await ctx.send(f"Veuillez attendre {time_left:.1f} secondes avant de réutiliser cette commande.")

        self.cooldowns[user_id] = now + cooldown_duration

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
        deleted = await ctx.channel.purge(limit=num_messages + 1)
        await ctx.send(f"{num_messages} messages supprimés.", delete_after=5)

    async def clear_all_messages(self, ctx):
        await ctx.send("Tous les messages vont être supprimés. Je vais recréer le salon pour éviter le rate limit.")
        channel = ctx.channel
        new_channel = await channel.clone(name=channel.name)
        await channel.delete()
        await new_channel.send(f"Le salon a été recréé. Vous pouvez commencer à discuter ici !")

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
