from discord.ext import commands


class Events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    # note: you always need to pass in self into the asyncs so the bot will work
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')

#setup line to add the cog to the bot
def setup(bot):
    bot.add_cog(Events(bot))