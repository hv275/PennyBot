from discord.ext import commands
import discord

class pennying(commands.Cog):
    def __init__(self, bot, sesh):
        self.bot = bot
        self.sesh = sesh


    @commands.command(name='join', help="Joining the game.")
    async def join(self, ctx):
        await ctx.send(self.sesh.add_player(ctx.author.display_name))

    @commands.command(name='leave', help="Leave the game.")
    async def leave(self, ctx):
        await ctx.send(self.sesh.remove_player(ctx.author.display_name))

    @commands.command(name='players', help="Show all the players currently in game")
    async def players(self, ctx):
        players = self.sesh.playershow()
        players.sort(key=lambda x: x.purelevel, reverse=True)
        await ctx.send("LEADERBOARD")
        i = 1
        for player in players:
            # pretty display of players but may be cumbersome in chat
            await ctx.send(f"{i}. {player.name:10s}, Attack: {player.attackstat:1.2f}, "
                           f"Defence: {player.defencestat:1.2f}, "
                           f"Level: {player.level:1.0f}")
            i += 1
        # await ctx.send(sesh.playershow()) for testing uncomment

    @commands.command(name='penny', help="Attempt to penny a player. Format: 'penny attack <name of victim>'")
    async def attack(self, ctx, victim):
        # this is a highly retarded way to go about sending messages to channels but it will have to do
        guild = discord.utils.get(self.bot.guilds, name=self.sesh.GUILD)
        vchannels = guild.voice_channels
        print(vchannels)
        response = self.sesh.penny(ctx.author.display_name, victim, vchannels)
        # change id to the appropriate channel
        channel = self.bot.get_channel(719990123051352155)
        # replies to the author and sends message to the assigned channel if needed
        await ctx.send(response)
        if ctx.channel == channel:
            pass
        else:
            await channel.send(response)

    @commands.command(name='snipe', help="Attempt to snipe a player. Format: 'penny snipe <name of victim>'")
    async def snipe(self, ctx, victim):
        # this is a highly retarded way to go about sending messages to channels but it will have to do
        guild = discord.utils.get(self.bot.guilds, name=self.sesh.GUILD)
        vchannels = guild.voice_channels
        print(vchannels)
        response = self.sesh.snipe(ctx.author.display_name, victim, vchannels)
        # change id to the appropriate channel
        channel = self.bot.get_channel(719990123051352155)
        # replies to the author and sends message to the assigned channel if needed
        await ctx.send(response)
        if ctx.channel == channel:
            pass
        else:
            await channel.send(response)

    @commands.command(name='balance', help="See your balance")
    async def getbalance(self, ctx):
        await ctx.send(self.sesh.get_balance(ctx.author.display_name))

    @commands.command(name='block', help="Hold your glass for 30 secs")
    async def hold_glass(self, ctx):
        await ctx.send(self.sesh.block(ctx.author.display_name))

    @commands.command(name='check', help="Check other player's stats")
    async def check(self, ctx, victim):
        await ctx.send(self.sesh.check(ctx.author.display_name, victim))

    @commands.command(name='give', help="Kindly donate some currency to another player")
    async def give(self, ctx, target, amount):
        await ctx.send(self.sesh.give(ctx.author.display_name, target, amount))


def setup(bot):
    bot.add_cog(pennying(bot,sesh))
