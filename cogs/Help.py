import discord
import logging
from discord.ext import commands

logger = logging.getLogger('covid-19')

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['h', 'commands'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def help(self, ctx):

        embed = discord.Embed(
            title='Bot Help',
            description='__Documentation for all commands__ \n Data from [Data Repository](https://github.com/CSSEGISandData/COVID-19) by Johns Hopkins CSSE \n Please vote for me on [TOP.GG](https://top.gg/bot/683462722368700526/vote) <:dbl:689485017667469327>',
            colour=discord.Colour.red()
        )
        embed.add_field(name='```.c stat <country/all/other> <province/state>```', value='Stats of coronavirus cases | React with 📈 for a linear graph or 📉 for a log graph \n **<all>** - Every country | **<other>** - Excludes China \n •For any country you may type the **full name** or **[ISO 3166-1 codes](https://en.wikipedia.org/wiki/ISO_3166-1)** \n __Example:__ **.c stat Italy** | **.c stat IT** | **.c stat ITA** \n •If the country or state\'s full name is two words, enclose them in **quotation marks** \n __Example:__ **.c stat "South Korea"** | **.c stat US "New York"** \n •If you would like stats on a specific **province** or **state (full name or abbreviated)**, put it after the country name \n __Example:__ **.c stat US California** or **.c stat US CA**', inline=False)
        embed.add_field(name='```.c reddit <category>```', value='Return posts of given category from [r/Coronavirus](https://www.reddit.com/r/Coronavirus/) \n Shows 5 posts at a time (up to 50 most recent) Use ⬅️ and ➡️ to scroll through \n **<category>** - `Hot` | `New` | `Top`', inline=False)
        embed.add_field(name='```.c info```', value='Return additional info about the bot such as server and user count', inline=False)
        embed.add_field(name='Bot Source Code', value='<:github:689501322969350158> [Github](https://github.com/picklejason/coronavirus-bot)') #If you self host this bot or use any part of this source code, I would be grateful if you leave this in or credit me somewhere else
        embed.add_field(name='Bot Invite', value='<:discord:689486285349715995> [Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)')
        embed.add_field(name='Donate', value='<:Kofi:689483361785217299> [Ko-fi](https://ko-fi.com/picklejason)')
        embed.set_footer(text='Have any issues or suggestions? Feel free to message me @PickleJason#5293')
        await ctx.send(embed=embed)

    @commands.command(name='info', aliases=['about', 'vote', 'invite', 'donate'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def info(self, ctx):
        embed = discord.Embed(
            title='Bot Info',
            description='Additional information about the bot | Use **.c help** for more info on commands \n •Please vote for me on [TOP.GG](https://top.gg/bot/683462722368700526/vote) <:dbl:689485017667469327>',
            colour=discord.Colour.red()
        )
        embed.add_field(name='Command Prefix', value='`.c` or `@mention`')
        users = 0
        for s in self.bot.guilds:
            users += len(s.members)
        embed.add_field(name='Servers | Shards', value=f'<:servers:689502498251341953> {len(self.bot.guilds)} | {len(self.bot.shards)}')
        embed.add_field(name='Users', value=f'<:user:689502620590669912> {users}')
        embed.add_field(name='Bot Source Code', value='<:github:689501322969350158> [Github](https://github.com/picklejason/coronavirus-bot)')
        embed.add_field(name='Bot Invite', value='<:discord:689486285349715995> [Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)')
        embed.add_field(name='Donate', value='<:Kofi:689483361785217299> [Ko-fi](https://ko-fi.com/picklejason)')
        embed.set_footer(text='Have any issues or suggestions? Feel free to message me @PickleJason#5293')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Ping',
            description=f'🏓 Pong! \n `{round(self.bot.latency * 1000)}ms`',
            colour=discord.Colour.red()
        )
        embed.set_footer(text='Have any issues or suggestions? Feel free to message me @PickleJason#5293')
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
