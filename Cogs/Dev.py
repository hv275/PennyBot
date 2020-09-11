from discord.ext import commands

class devcom(commands.Cog):
    def __init__(self,bot,sesh):
        self.bot = bot
        self.sesh = sesh


    # cash injection that checks that the user has an admin role, also hidden from help menu
    @commands.command(name='cashinjection', help="dev only", hidden=True)
    #note that roles may be different
    @commands.has_role('dev')
    async def cashinjection(self, ctx, name, num):
        await ctx.send(self.sesh.cashinjection(name, num))

    # please keep these two together
    # output in case of a check failure

    @commands.command(name='kick', help="dev only", hidden=True)
    @commands.has_role('dev')
    async def kick(self, ctx, name):
        await ctx.send(self.sesh.remove_player(name))
        await ctx.send("Removed by admin")


#setup line to add the cog to the bot
def setup(bot):
    bot.add_cog(devcom(bot,sesh))