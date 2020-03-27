import discord
import logging
from discord.ext import commands
from datetime import datetime

logger = logging.getLogger('covid-19')

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def total_users(self):
        users = 0
        for s in self.bot.guilds:
            users += len(s.members)
        return users

    @commands.command(name='help', aliases=['h', 'commands'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def help(self, ctx):

        embed = discord.Embed(
            title='Bot Help',
            description='Data from [Worldometer](https://www.worldometers.info/coronavirus/) and [Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19) \n Please vote for me on <:dbl:689485017667469327> [TOP.GG](https://top.gg/bot/683462722368700526/vote) | <:discord:689486285349715995> Join the [Support Server](https://discord.gg/tVN2UTa) \n \n __Documentation for all commands__',
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
            )
        embed.add_field(name='```.c stat <country/all> <state>```', value='Show **Confirmed** (new cases), **Deaths** (new deaths), and **Recovered** \n React with 📈 for a linear graph or 📉 for a log graph \n **<country>** - Country stats | **<all>** - Global stats \n •For any country you may type the **full name** or **[ISO 3166-1 codes](https://en.wikipedia.org/wiki/ISO_3166-1)** \n __Example:__ **.c stat Italy** | **.c stat IT** | **.c stat ITA** \n •If the country or state\'s full name is two words, enclose them in **quotation marks** \n __Example:__ **.c stat "South Korea"** | **.c stat US "New York"** \n •If you would like stats on a specific **state (full name or abbreviated)** in the US, put it after the country name \n __Example:__ **.c stat US California** or **.c stat US CA**', inline=False)
        embed.add_field(name='```.c reddit <category>```', value='Return posts of given category from [r/Coronavirus](https://www.reddit.com/r/Coronavirus/) \n Shows 5 posts at a time (up to first 15) Use ⬅️ and ➡️ to scroll through \n **<category>** - `Hot` | `New` | `Top`', inline=False)
        embed.add_field(name='```.c info```', value='Return additional info about the bot such as server and user count', inline=False)
        embed.add_field(name='```.c support```', value='Return invite link to support server', inline=False)
        embed.add_field(name='Bot Source Code', value='<:github:689501322969350158> [Github](https://github.com/picklejason/coronavirus-bot)') #If you self host this bot or use any part of this source code, I would be grateful if you leave this in or credit me somewhere else
        embed.add_field(name='Bot Invite', value='<:discord:689486285349715995> [Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)')
        embed.add_field(name='Donate', value='<:Kofi:689483361785217299> [Ko-fi](https://ko-fi.com/picklejason)')
        await ctx.send(embed=embed)

    @commands.command(name='info', aliases=['about', 'vote', 'invite', 'donate'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def info(self, ctx):
        embed = discord.Embed(
            title='Bot Info',
            description='Additional information about the bot | Use **.c help** for more info on commands \n Please vote for me on <:dbl:689485017667469327> [TOP.GG](https://top.gg/bot/683462722368700526/vote) | Join the <:discord:689486285349715995> [Support Server](https://discord.gg/tVN2UTa)',
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name='Command Prefix', value='`.c` or `@mention`')
        users = self.total_users()
        embed.add_field(name='Servers | Shards', value=f'<:servers:689502498251341953> {len(self.bot.guilds)} | {len(self.bot.shards)}')
        embed.add_field(name='Users', value=f'<:user:689502620590669912> {users}')
        embed.add_field(name='Bot Source Code', value='<:github:689501322969350158> [Github](https://github.com/picklejason/coronavirus-bot)')
        embed.add_field(name='Bot Invite', value='<:discord:689486285349715995> [Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)')
        embed.add_field(name='Donate', value='<:Kofi:689483361785217299> [Ko-fi](https://ko-fi.com/picklejason)')
        await ctx.send(embed=embed)

    @commands.command(name='support', aliases=['server'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def support(self, ctx):
        embed = discord.Embed(
            description='<:discord:689486285349715995> Join the [Support Server](https://discord.gg/tVN2UTa)!',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Ping',
            description=f'🏓 Pong! \n `{round(self.bot.latency * 1000)}ms`',
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        '''Triggers when wrong command or is inputted'''
        if isinstance(error, commands.CommandNotFound):
            message = ctx.message.content
            # logger.info(f'Invalid command use \"{message}\"')
        elif isinstance(error, commands.CommandOnCooldown):
            message = 'To prevent spam, the command has been rate limited to 3 times every 10 seconds'
            logger.info(f'Rate limit reached by {ctx.message.author}({ctx.message.author.id}) in {ctx.message.guild}({ctx.message.guild.id})')
            await ctx.send(message)

    @commands.command(name='reload', aliases=['r'])
    @commands.is_owner()
    async def reload(self, ctx):
        self.bot.unload()
        self.bot.load()
        logger.info('Cogs Reloaded')
        await ctx.send('Cogs Reloaded')

def setup(bot):
    bot.add_cog(Help(bot))
