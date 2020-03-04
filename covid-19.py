import discord
from discord.ext import commands
import pandas as pd
import os
import matplotlib.pyplot as plt
import io
from discord import File

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
    embed.add_field(name = 'Dataset from', value = '[Johns Hopkins CSSE Github](https://github.com/CSSEGISandData/COVID-19)')
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

    if any(confirmed_df['Country/Region'].str.contains(location)) or location == 'All' or location == 'Other':

        updated = list(confirmed_df)[-1]
        plt.style.use('dark_background')
        fig = plt.figure(dpi=200)

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
            confirmed = confirmed_df[confirmed_df['Country/Region'].str.contains(location)].iloc[:,-1].sum()
            prev_confirmed = confirmed_df[confirmed_df['Country/Region'].str.contains(location)].iloc[:,-2].sum()
            deaths = deaths_df[deaths_df['Country/Region'].str.contains(location)].iloc[:,-1].sum()
            prev_deaths = deaths_df[deaths_df['Country/Region'].str.contains(location)].iloc[:,-2].sum()
            recovered = recovered_df[recovered_df['Country/Region'].str.contains(location)].iloc[:,-1].sum()
            prev_recovered = recovered_df[recovered_df['Country/Region'].str.contains(location)].iloc[:,-2].sum()
            ax = confirmed_df[confirmed_df['Country/Region'].str.contains(location)].iloc[:,4:].sum().plot(label='Confirmed')
            ax = recovered_df[recovered_df['Country/Region'].str.contains(location)].iloc[:,4:].sum().plot(label='Recovered')

        change_confirmed = confirmed - prev_confirmed
        if (change_confirmed > 0):
            change_confirmed = f'(+{change_confirmed})'
        else:
            change_confirmed = ''

        change_deaths = deaths - prev_deaths
        if (change_deaths > 0):
            change_deaths = f'(+{change_deaths})'
        else:
            change_deaths = ''

        change_recovered = recovered - prev_recovered
        if (change_recovered > 0):
            change_recovered = f'(+{change_recovered})'
        else:
            change_recovered = ''

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

        filename = 'tmp\\' + location + '_graph.png'
        plt.savefig(filename, transparent=True)
        plt.close(fig)

        with open(filename, 'rb') as f:
            file = io.BytesIO(f.read())

        image = discord.File(file, filename='graph.png')

        embed = discord.Embed(
            title=f'Coronavirus COVID-19 {location} Cases',
            description='Data from [Johns Hopkins CSSE Github](https://github.com/CSSEGISandData/COVID-19)',
            colour=discord.Colour.red()
        )
        embed.set_image(url=f'attachment://graph.png')
        embed.add_field(name='Confirmed', value= f'**{confirmed}** {change_confirmed}')
        embed.add_field(name='Deaths', value=f'**{deaths}** {change_deaths}')
        embed.add_field(name='Recovered', value=f'**{recovered}** {change_recovered}')
        embed.add_field(name='Mortality Rate', value=f'**{round((deaths/confirmed * 100),2)}%**')
        embed.set_footer(text= f'Updated {updated}')

        await ctx.send(file=image, embed=embed)

    else:
        await ctx.send('There is no available data for this location')

if __name__ == '__main__':
    # import config
    # client.run(config.token)
    client.run(os.environ['TOKEN']) #Heroku
