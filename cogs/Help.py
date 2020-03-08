import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(
            title='Bot Help',
            description='Documentation for all commands | Data from [Data Repository](https://github.com/CSSEGISandData/COVID-19) by Johns Hopkins CSSE',
            colour=discord.Colour.red()
        )
        embed.add_field(name='```.c stat [location]```', value='Return **Total Confirmed**, **Total Deaths**, and **Total Recovered** of given location along with a graph \n __[location]__ \n "all" = stats of all locations \n "other" = stats of locations other than China \n "country name" = stats of a specific country \n *(United States is abbreviated to **US** and United Kingdom is abbreviated to **UK**)* \n If you would like stats on a specific province or state (abbreviated), put it after the country name. \n Example: **.c stat US CA** - shows the stats of the state of California', inline=False)
        embed.add_field(name='```.c reddit [category]```', value='Return posts of given category from [r/Coronavirus](https://www.reddit.com/r/Coronavirus/) \n Shows 5 posts at a time (up to 50 most recent) Use ⏪ and ⏩ to scroll through (Bot needs permission to manage messages to scroll)\n __[category]__ \n "Hot" | "New" | "Top"', inline=False)
        embed.add_field(name='```.c info```', value='Return additional info about the bot such as server and user count', inline=False)
        embed.add_field(name='Bot Source Code', value='[Github](https://github.com/picklejason/coronavirus-bot)') #If you self host this bot or use any part of this source code, I would be grateful if you leave this in or credit me somewhere else
        embed.add_field(name='Bot Invite', value='[Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)')

        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            title='Bot Info',
            description='Additional information about the bot | Use **.c help** for more info on commands',
            colour=discord.Colour.red()
        )
        embed.add_field(name='Command Prefix', value='.c or @mention ')

        users = 0
        for s in self.client.guilds:
            users += len(s.members)

        embed.add_field(name='Servers', value=len(self.client.guilds))
        embed.add_field(name='Users', value=users)
        embed.add_field(name='Bot Invite', value='[Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)')
        embed.add_field(name = 'Bot Source Code', value='[Github](https://github.com/picklejason/coronavirus-bot)')

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        '''Triggers when wrong command or is inputted'''
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Invalid command | Use `.c help` to see available commands and instructions')

def setup(client):
    client.add_cog(Help(client))
