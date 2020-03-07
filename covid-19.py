import discord
from discord.ext import commands
import pandas as pd
import os
import matplotlib.pyplot as plt
import io
from discord import File
import praw
from datetime import datetime
#import config

client = commands.Bot(command_prefix = '.c ')
client.remove_command('help')

# red = praw.Reddit(client_id=config.redditID,
#                 client_secret=config.redditSecret,
#                 password=config.redditPW,
#                 user_agent=config.user_agent,
#                 username=config.redditName)

#Heroku
red = praw.Reddit(client_id=os.environ['REDDITID'],
                client_secret=os.environ['REDDITSECRET'],
                password=os.environ['REDDITPW'],
                user_agent=os.environ['USER_AGENT'],
                username=os.environ['REDDITNAME'])

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(client.guilds)} servers | .c help'))
    print('Bot is online.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command | Use `.c help` to see available commands and how to use them')

#Help Command
@client.command()
async def help(ctx):

    embed = discord.Embed(
        title='Bot Help',
        description='Documentation for all commands | Data from [Johns Hopkins CSSE Github](https://github.com/CSSEGISandData/COVID-19)',
        colour=discord.Colour.red()
    )
    embed.add_field(name='```.c stat [location]```', value='Return **Total Confirmed**, **Total Deaths**, and **Total Recovered** of given location along with a graph \n __[location]__ \n "all" = stats of all locations \n "other" = stats of locations other than China \n "country name" = stats of a specific country \n *(United States is abbreviated to **US** and United Kingdom is abbreviated to **UK**)* \n If you would like stats on a specific province or state (abbreviated), put it after the country name. \n Example: **.c stat US CA** - shows the stats of the state of California', inline=False)
    embed.add_field(name='```.c reddit [category]```', value='Return posts of given category from [r/Coronavirus](https://www.reddit.com/r/Coronavirus/) \n Shows 5 posts at a time (up to 50 most recent) Use ⏪ and ⏩ to scroll through \n __[category]__ \n "Hot" | "New" | "Top"', inline=False)
    embed.add_field(name='Bot Source Code', value='[Github](https://github.com/picklejason/coronavirus-bot)') #If you self host this bot or use any part of this source code, I would be grateful if you leave this in or credit me somewhere else
    embed.add_field(name='Bot Invite', value='[Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=0&scope=bot)')

    await ctx.send(embed=embed)

left = '⏪'
right = '⏩'

def predicate(message, l, r):
    def check(reaction, user):
        if reaction.message.id != message.id or user == client.user:
            return False
        if l and reaction.emoji == left:
            return True
        if r and reaction.emoji == right:
            return True
        return False

    return check

#Reddit Command | Returns 5 posts (Hot, New, Top) from the subreddit r/Coronavirus
@client.command()
async def reddit(ctx, category = 'Hot'):

    category = category.title()

    if category == 'Hot':
        submissions = list(red.subreddit('Coronavirus').hot(limit=5))
    elif category == 'New':
        submissions = list(red.subreddit('Coronavirus').new(limit=5))
    elif category == 'Top':
        submissions = list(red.subreddit('Coronavirus').top(limit=5))
    else:
        await ctx.send('Please enter one of the following categories: Hot, New, Top')
        return

    index = 1

    description = f'{category} posts'
    timestamp = datetime.utcnow()
    url = 'https://www.reddit.com/r/Coronavirus/'
    embed = discord.Embed(title='/r/Coronavirus', description=description, colour=discord.Colour.red(), timestamp=timestamp, url=url)

    for s in submissions:
        embed.add_field(name=f':small_red_triangle:{s.score} | Posted by u/{s.author} on {datetime.fromtimestamp(s.created).strftime("%m/%d/%y %H:%M:%S")}', value=f'[{s.title}](https://www.reddit.com{s.permalink})', inline=False)

    embed.set_thumbnail(url='https://styles.redditmedia.com/t5_2x4yx/styles/communityIcon_ex5aikhvi3i41.png')
    embed.set_footer(text=f'Page {index} of 10')
    msg = await ctx.send(embed=embed)

    while True:
        l = index != 1
        r = index != 10

        if l:
            await msg.add_reaction(left)
        else:
            await msg.remove_reaction(left, msg.author)
        if r:
            await msg.add_reaction(right)
        else:
            await msg.remove_reaction(right, msg.author)

        react, user = await client.wait_for('reaction_add', check=predicate(msg, l, r))
        if react.emoji == left:
            index -= 1
            await msg.remove_reaction(left, user)

        elif react.emoji == right:
            index += 1
            await msg.remove_reaction(right, user)

        embed.clear_fields()

        number = index * 5

        if category == 'Hot':
            submissions = list(red.subreddit('Coronavirus').hot(limit=50))[number-5:number]
        elif category == 'New':
            submissions = list(red.subreddit('Coronavirus').new(limit=50))[number-5:number]
        elif category == 'Top':
            submissions = list(red.subreddit('Coronavirus').top(limit=50))[number-5:number]

        for s in submissions:
            embed.add_field(name=f':small_red_triangle:{s.score} | Posted by u/{s.author} on {datetime.fromtimestamp(s.created).strftime("%m/%d/%y %H:%M:%S")}', value=f'[{s.title}](https://www.reddit.com{s.permalink})', inline=False)

        embed.set_footer(text=f'Page {index} of 10')
        await msg.edit(embed=embed)

#Statistics Command | Provides Confirmed, Deaths, and Recovered | Mortality Rate: Deaths/Confirmed | Includes Graph
@client.command()
async def stat(ctx, location : str, provst = ''):

    if len(location) == 2:
        location = location.upper()
    else:
        location = location.title()

    if len(provst) == 2:
        provst = ', ' + provst.upper()
    else:
        provst = provst.title()

    confirmed_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    deaths_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
    recovered_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

    confirmed_df = pd.read_csv(confirmed_url, error_bad_lines=False)
    deaths_df = pd.read_csv(deaths_url, error_bad_lines=False)
    recovered_df = pd.read_csv(recovered_url, error_bad_lines=False)

    #Check if data exists for location
    if any(confirmed_df['Country/Region'].str.contains(location)) or location == 'All' or location == 'Other':

        updated = list(confirmed_df)[-1]
        plt.style.use('dark_background')
        fig = plt.figure(dpi=200)

        #Parse Data
        if location == 'All':
            confirmed = confirmed_df.iloc[:,-1].sum()
            prev_confirmed = confirmed_df.iloc[:,-2].sum()
            deaths = deaths_df.iloc[:,-1].sum()
            prev_deaths = deaths_df.iloc[:,-2].sum()
            recovered = recovered_df.iloc[:,-1].sum()
            prev_recovered = recovered_df.iloc[:,-2].sum()
            ax = confirmed_df.iloc[:,4:].sum().plot(label='Confirmed')
            ax = recovered_df.iloc[:,4:].sum().plot(label='Recovered')

        elif location == 'Other':
            confirmed = confirmed_df[~confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
            prev_confirmed = confirmed_df[~confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
            deaths = deaths_df[~deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
            prev_deaths = deaths_df[~deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
            recovered = recovered_df[~recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
            prev_recovered = recovered_df[~recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
            ax = confirmed_df[~confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,4:].sum().plot(label='Confirmed')
            ax = recovered_df[~recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,4:].sum().plot(label='Recovered')

        else:
            if provst:
                confirmed = confirmed_df[confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,-1].sum()
                prev_confirmed = confirmed_df[confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,-2].sum()
                deaths = deaths_df[deaths_df['Province/State'].str.contains(provst, na=False)].iloc[:,-1].sum()
                prev_deaths = deaths_df[deaths_df['Province/State'].str.contains(provst, na=False)].iloc[:,-2].sum()
                recovered = recovered_df[recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,-1].sum()
                prev_recovered = recovered_df[recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,-2].sum()
                ax = confirmed_df[confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,4:].sum().plot(label='Confirmed')
                ax = recovered_df[recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,4:].sum().plot(label='Recovered')
            else:
                confirmed = confirmed_df[confirmed_df['Country/Region'].str.contains(location, na=False)].iloc[:,-1].sum()
                prev_confirmed = confirmed_df[confirmed_df['Country/Region'].str.contains(location, na=False)].iloc[:,-2].sum()
                deaths = deaths_df[deaths_df['Country/Region'].str.contains(location, na=False)].iloc[:,-1].sum()
                prev_deaths = deaths_df[deaths_df['Country/Region'].str.contains(location, na=False)].iloc[:,-2].sum()
                recovered = recovered_df[recovered_df['Country/Region'].str.contains(location, na=False)].iloc[:,-1].sum()
                prev_recovered = recovered_df[recovered_df['Country/Region'].str.contains(location, na=False)].iloc[:,-2].sum()
                ax = confirmed_df[confirmed_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Confirmed')
                ax = recovered_df[recovered_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Recovered')

        #Check if change is postive | adds "+" before change
        change_confirmed = confirmed - prev_confirmed
        if (change_confirmed > 0):
            change_confirmed = f'(+{int(change_confirmed)})'
        else:
            change_confirmed = ''

        change_deaths = deaths - prev_deaths
        if (change_deaths > 0):
            change_deaths = f'(+{int(change_deaths)})'
        else:
            change_deaths = ''

        change_recovered = recovered - prev_recovered
        if (change_recovered > 0):
            change_recovered = f'(+{int(change_recovered)})'
        else:
            change_recovered = ''

        if confirmed == 0 or deaths == 0:
            mortality_rate = 0
        else:
            mortality_rate = round((deaths/confirmed * 100), 2)

        #Graph
        ax.yaxis.grid()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.legend(loc='upper left', fancybox=True, facecolor='0.2')
        ax.set_ylim(ymin=0)

        locs, _ = plt.yticks()
        ylabels = []
        for l in locs:
            lab = str(int(l)).replace('00000000', '00M').replace('0000000', '0M').replace('000000', 'M').replace('00000', '00K').replace('0000', '0K').replace('000', 'K')
            if not ('K' in lab or 'M' in lab):
                lab = "{:,}".format(int(lab))
            ylabels.append(lab)

        plt.yticks(locs, ylabels)

        #Save graph to tmp folder
        filename = 'tmp\\' + location + '_graph.png'
        plt.savefig(filename, transparent=True)
        plt.close(fig)

        with open(filename, 'rb') as f:
            file = io.BytesIO(f.read())

        image = discord.File(file, filename='graph.png')

        embed = discord.Embed(
            title=f'Coronavirus COVID-19 Cases | {location} {provst}',
            description='Data from [Johns Hopkins CSSE Github](https://github.com/CSSEGISandData/COVID-19)',
            colour=discord.Colour.red()
        )
        embed.set_image(url=f'attachment://graph.png')
        embed.add_field(name='Confirmed', value= f'**{int(confirmed)}** {change_confirmed}')
        embed.add_field(name='Deaths', value=f'**{int(deaths)}** {change_deaths}')
        embed.add_field(name='Recovered', value=f'**{int(recovered)}** {change_recovered}')
        embed.add_field(name='Mortality Rate', value=f'**{mortality_rate}%**')
        embed.set_footer(text= f'Updated {updated}')

        await ctx.send(file=image, embed=embed)

    else:
        await ctx.send('There is no available data for this location')

if __name__ == '__main__':
    # client.run(config.token)
    #Heroku
    client.run(os.environ['TOKEN'])
