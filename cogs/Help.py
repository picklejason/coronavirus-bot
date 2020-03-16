import discord
import logging
from discord.ext import commands

logger = logging.getLogger('covid-19')

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='help', aliases=['h', 'commands'])
    async def help(self, ctx):

        embed = discord.Embed(
            title='Bot Help',
            description='Documentation for all commands | Data from [Data Repository](https://github.com/CSSEGISandData/COVID-19) by Johns Hopkins CSSE \n Please vote for me on [TOP.GG](https://top.gg/bot/683462722368700526/vote) 👍',
            colour=discord.Colour.red()
        )
        embed.add_field(name='```.c stat [location]```', value='Return total **Confirmed**, **Deaths**, and **Recovered** along with a **graph** \n **[location]** \n **"all"** = stats of all locations \n **"other"** = stats of locations other than China \n **"country name"** = stats of a specific country \n •For any country you may type the **full name** or **[ISO 3166-1 codes](https://en.wikipedia.org/wiki/ISO_3166-1)** \n __Example:__ **.c stat Italy** or **.c stat IT** \n •If the country or state\'s full name is two words, enclose them in **quotation marks** \n __Example:__ **.c stat "South Korea"** | **.c stat US "New York"** \n •If you would like stats on a specific **province** or **state (full name or abbreviated)**, put it after the country name \n __Example:__ **.c stat US California** or **.c stat US CA**', inline=False)
        embed.add_field(name='```.c reddit [category]```', value='Return posts of given category from [r/Coronavirus](https://www.reddit.com/r/Coronavirus/) \n Shows 5 posts at a time (up to 50 most recent) Use ⬅️ and ➡️ to scroll through (Bot needs permission to **manage messages** to flip pages)\n **[category]** \n "Hot" | "New" | "Top"', inline=False)
        embed.add_field(name='```.c info```', value='Return additional info about the bot such as server and user count', inline=False)
        embed.add_field(name='Bot Source Code', value='[Github](https://github.com/picklejason/coronavirus-bot)') #If you self host this bot or use any part of this source code, I would be grateful if you leave this in or credit me somewhere else
        embed.add_field(name='Bot Invite', value='[Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)')
        embed.add_field(name='Donate', value='[Support Me on Ko-fi](https://ko-fi.com/picklejason)')
        embed.set_footer(text='Have any issues or suggestions? Feel free to message me @PickleJason#5293')
        logger.info("Help command used")
        await ctx.send(embed=embed)

    @commands.command(name='info', aliases=['about', 'vote', 'invite', 'donate'])
    async def info(self, ctx):
        embed = discord.Embed(
            title='Bot Info',
            description='Additional information about the bot | Use **.c help** for more info on commands \n Please vote for me on [TOP.GG](https://top.gg/bot/683462722368700526/vote) 👍',
            colour=discord.Colour.red()
        )
        embed.add_field(name='Command Prefix', value='`.c` or `@mention`')
        users = 0
        for s in self.client.guilds:
            users += len(s.members)
        embed.add_field(name='Servers', value=len(self.client.guilds))
        embed.add_field(name='Users', value=users)
        embed.add_field(name='Bot Invite', value='[Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)')
        embed.add_field(name ='Bot Source Code', value='[Github](https://github.com/picklejason/coronavirus-bot)')
        embed.add_field(name='Donate', value='[Support Me on Ko-fi](https://ko-fi.com/picklejason)')
        embed.set_footer(text='Have any issues or suggestions? Feel free to message me @PickleJason#5293')
        logger.info("Info command used")
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Ping',
            description=f'🏓 Pong! \n `{round(self.client.latency * 1000)}ms`',
            colour=discord.Colour.red()
        )
        embed.set_footer(text='Have any issues or suggestions? Feel free to message me @PickleJason#5293')
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        '''Triggers when wrong command or is inputted'''
        if isinstance(error, commands.CommandNotFound):
            message = ctx.message.content
            logger.info(f'Invalid command use \"{message}\"')
            # if ctx.guild.id == 264445053596991498:
            #     return
            # else:
            #     await ctx.send('Invalid command | Use `.c help` to see available commands and instructions')

    @commands.command(name='reload', aliases=['r'])
    @commands.is_owner()
    async def reload(self, ctx):
        self.client.unload()
        self.client.load()
        logger.info('Cogs Reloaded')
        await ctx.send('Cogs Reloaded')

def setup(client):
    client.add_cog(Help(client))
