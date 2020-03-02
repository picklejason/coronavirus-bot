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
        colour=discord.Colour.red()
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

    confirmed = confirmed_df[confirmed_df['Country/Region'].str.contains(location)].iloc[:,-1].sum()
    prev_confirmed = confirmed_df[confirmed_df['Country/Region'].str.contains(location)].iloc[:,-2].sum()
    change_confirmed = confirmed - prev_confirmed
    if (change_confirmed > 0):
        change_confirmed = f'(+{change_confirmed})'
    else:
        change_confirmed = ''

    deaths = deaths_df[deaths_df['Country/Region'].str.contains(location)].iloc[:,-1].sum()
    prev_deaths = deaths_df[deaths_df['Country/Region'].str.contains(location)].iloc[:,-2].sum()
    change_deaths = deaths - prev_deaths
    if (change_deaths > 0):
        change_deaths = f'(+{change_deaths})'
    else:
        change_deaths = ''

    recovered = recovered_df[recovered_df['Country/Region'].str.contains(location)].iloc[:,-1].sum()
    prev_recovered = recovered_df[recovered_df['Country/Region'].str.contains(location)].iloc[:,-2].sum()
    change_recovered = recovered - prev_recovered
    if (change_recovered > 0):
        change_recovered = f'(+{change_recovered})'
    else:
        change_recovered = ''

    all_confirmed = confirmed_df.iloc[:,-1].sum()
    prev_all_confirmed = confirmed_df.iloc[:,-2].sum()
    change_all_confirmed = all_confirmed - prev_all_confirmed
    if (change_all_confirmed > 0):
        change_all_confirmed = f'(+{change_all_confirmed})'
    else:
        change_all_confirmed = ''

    all_deaths = deaths_df.iloc[:,-1].sum()
    prev_all_deaths = deaths_df.iloc[:,-2].sum()
    change_all_deaths = all_deaths - prev_all_deaths
    if (change_all_deaths > 0):
        change_all_deaths = f'(+{change_all_deaths})'
    else:
        change_all_deaths = ''

    all_recovered = recovered_df.iloc[:,-1].sum()
    prev_all_recovered = recovered_df.iloc[:,-2].sum()
    change_all_recovered = all_recovered - prev_all_recovered
    if (change_all_recovered > 0):
        change_all_recovered = f'(+{change_all_recovered})'
    else:
        change_all_recovered = ''

    other_confirmed = confirmed_df[~confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
    prev_other_confirmed = confirmed_df[~confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
    change_other_confirmed = other_confirmed - prev_other_confirmed
    if (change_other_confirmed > 0):
        change_other_confirmed = f'(+{change_other_confirmed})'
    else:
        change_other_confirmed = ''

    other_deaths = deaths_df[~deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
    prev_other_deaths = deaths_df[~deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
    change_other_deaths = other_deaths - prev_other_deaths
    if (change_other_deaths > 0):
        change_other_deaths = f'(+{change_other_deaths})'
    else:
        change_other_confirmed = ''

    other_recovered = recovered_df[~recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
    prev_other_recovered = recovered_df[~recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
    change_other_recovered = other_recovered - prev_other_recovered
    if (change_other_recovered > 0):
        change_other_recovered = f'(+{change_other_recovered})'
    else:
        change_other_confirmed = ''

    if any(confirmed_df['Country/Region'].str.contains(location)) or location == 'All' or location == 'Other':

        embed = discord.Embed(
            title=f'Coronavirus COVID-19 {location} Cases',
            description='Data from [John Hopkins University Github](https://github.com/CSSEGISandData/COVID-19)',
            colour=discord.Colour.red()
        )
        if location == 'All':
            embed.add_field(name='Confirmed', value=f'**{all_confirmed}** {change_all_confirmed}')
            embed.add_field(name='Deaths', value=f'**{all_deaths}** {change_all_deaths}')
            embed.add_field(name='Recovered', value=f'**{all_recovered}** {change_all_recovered}')
            embed.add_field(name='Mortality Rate', value=f'**{round((all_deaths/all_confirmed * 100),2)}%**')
        elif location == 'Other':
            embed.add_field(name='Confirmed', value=f'**{other_confirmed}** {change_other_confirmed}')
            embed.add_field(name='Deaths', value=f'**{other_deaths}** {change_other_deaths}')
            embed.add_field(name='Recovered', value=f'**{other_recovered}** {change_other_recovered}')
            embed.add_field(name='Mortality Rate', value=f'**{round((other_deaths/other_confirmed * 100),2)}%**')
        else:
            embed.add_field(name='Confirmed', value= f'**{confirmed}** {change_confirmed}')
            embed.add_field(name='Deaths', value=f'**{deaths}** {change_deaths}')
            embed.add_field(name='Recovered', value=f'**{recovered}** {change_recovered}')
            embed.add_field(name='Mortality Rate', value=f'**{round((deaths/confirmed * 100),2)}%**')

        embed.set_footer(text= f'Updated {updated}')

        await ctx.send(embed=embed)

    else:
        await ctx.send('There is no available data for this location')

if __name__ == '__main__':
    # import config
    # client.run(config.token)
    client.run(os.environ['TOKEN']) #Heroku
