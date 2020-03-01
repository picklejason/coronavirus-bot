import discord
from discord.ext import commands
import pandas as pd
import os

client = commands.Bot(command_prefix = '.c ')
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='.c help'))
    print('Bot is online.')

@client.command()
async def help(ctx):

    embed = discord.Embed(
        title='Bot Help',
        colour=discord.Colour.purple()
    )
    embed.add_field(name='```.c stat```', value='Returns **Total Confirmed**, **Total Deaths**, and **Total Recovered** \n \n To see stats of all locations use ```.c stat "all"``` \n To see stats of locations other than China use ```.c stat "other"``` \n To see stats of a specific country use ```.c stat "country name"```', inline=False)
    embed.add_field(name = 'Dataset from', value = '[John Hopkins University Github](https://github.com/CSSEGISandData/COVID-19)')
    embed.add_field(name='Bot Source Code', value='[Github](https://github.com/picklejason/coronavirus-bot)')

    await ctx.send(embed=embed)

@client.command()
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount+1)

@client.command()
async def stat(ctx, location : str ):

    if len(location) == 2:
        location = location.upper()
    else:
        location = location.title()

    confirmed_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    deaths_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
    recovered_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

    confirmed_df = pd.read_csv(confirmed_url, error_bad_lines=False)
    deaths_df = pd.read_csv(deaths_url, error_bad_lines=False)
    recovered_df = pd.read_csv(recovered_url, error_bad_lines=False)

    updated = list(confirmed_df)[-1]

    index = {'confirmed': confirmed_df[confirmed_df['Country/Region'].str.contains(location)].iloc[:,-1].sum(),
    'deaths': deaths_df[deaths_df['Country/Region'].str.contains(location)].iloc[:,-1].sum(),
    'recovered': recovered_df[recovered_df['Country/Region'].str.contains(location)].iloc[:,-1].sum(),

    'aConfirmed': confirmed_df.iloc[:,-1].sum(),
    'aDeaths': deaths_df.iloc[:,-1].sum(),
    'aRecovered': recovered_df.iloc[:,-1].sum(),

    'oConfirmed': confirmed_df[~confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum(),
    'oDeaths': deaths_df[~deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum(),
    'oRecovered': recovered_df[~recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
    }

    if any(confirmed_df['Country/Region'].str.contains(location)) or location == 'All' or location == 'Other':

        embed = discord.Embed(
            title=f'Coronavirus COVID-19 {location} Cases ',
            colour=discord.Colour.purple()
        )
        if location == 'All':
            embed.add_field(name='Confirmed', value=index['aConfirmed'])
            embed.add_field(name='Deaths', value=index['aDeaths'])
            embed.add_field(name='Recovered', value=index['aRecovered'])
        elif location == 'Other':
            embed.add_field(name='Confirmed', value=index['oConfirmed'])
            embed.add_field(name='Deaths', value=index['oDeaths'])
            embed.add_field(name='Recovered', value=index['oRecovered'])
        else:
            embed.add_field(name='Confirmed', value=index['confirmed'])
            embed.add_field(name='Deaths', value=index['deaths'])
            embed.add_field(name='Recovered', value=index['recovered'])

        embed.add_field(name = 'Dataset from', value = '[John Hopkins University Github](https://github.com/CSSEGISandData/COVID-19)', inline=False)
        embed.set_footer(text= f'Updated {updated}')

        await ctx.send(embed=embed)

    else:
        await ctx.send('There is no available data for this location')

if __name__ == '__main__':
    # import config
    # client.run(config.token)
    client.run(os.environ['TOKEN']) #Heroku
