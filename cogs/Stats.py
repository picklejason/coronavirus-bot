import discord
import io
import os
import pandas as pd
import matplotlib.pyplot as plt
import logging
from discord import File
from discord.ext import commands
from datetime import datetime

logger = logging.getLogger('covid-19')

class Stats(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Statistics Command | Provides Confirmed, Deaths, and Recovered | Mortality Rate: Deaths/Confirmed | Includes Graph
    @commands.command()
    async def stat(self, ctx, location : str, provst = ''):

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
        if location == 'All' or location == 'Other' or any(confirmed_df['Country/Region'].str.contains(location)):

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
                ax = confirmed_df.iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                ax = recovered_df.iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')

            elif location == 'Other':
                confirmed = confirmed_df[~confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                prev_confirmed = confirmed_df[~confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
                deaths = deaths_df[~deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                prev_deaths = deaths_df[~deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
                recovered = recovered_df[~recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                prev_recovered = recovered_df[~recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
                ax = confirmed_df[~confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                ax = recovered_df[~recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')

            else:
                if provst:
                    confirmed = confirmed_df[confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,-1].sum()
                    prev_confirmed = confirmed_df[confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,-2].sum()
                    deaths = deaths_df[deaths_df['Province/State'].str.contains(provst, na=False)].iloc[:,-1].sum()
                    prev_deaths = deaths_df[deaths_df['Province/State'].str.contains(provst, na=False)].iloc[:,-2].sum()
                    recovered = recovered_df[recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,-1].sum()
                    prev_recovered = recovered_df[recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,-2].sum()
                    ax = confirmed_df[confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                    ax = recovered_df[recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')
                else:
                    confirmed = confirmed_df[confirmed_df['Country/Region'].str.contains(location, na=False)].iloc[:,-1].sum()
                    prev_confirmed = confirmed_df[confirmed_df['Country/Region'].str.contains(location, na=False)].iloc[:,-2].sum()
                    deaths = deaths_df[deaths_df['Country/Region'].str.contains(location, na=False)].iloc[:,-1].sum()
                    prev_deaths = deaths_df[deaths_df['Country/Region'].str.contains(location, na=False)].iloc[:,-2].sum()
                    recovered = recovered_df[recovered_df['Country/Region'].str.contains(location, na=False)].iloc[:,-1].sum()
                    prev_recovered = recovered_df[recovered_df['Country/Region'].str.contains(location, na=False)].iloc[:,-2].sum()
                    ax = confirmed_df[confirmed_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                    ax = recovered_df[recovered_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')

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
            fig.autofmt_xdate()
            ax.xaxis.grid(linestyle='--', alpha=0.5)
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
            filename = './graphs/graph.png'
            plt.savefig(filename, transparent=True)
            plt.close(fig)

            with open(filename, 'rb') as f:
                file = io.BytesIO(f.read())

            image = discord.File(file, filename='graph.png')

            if ',' in provst:
                provst = ' ' + provst[-2:] + ','
            elif provst != '':
                provst = ' ' + provst + ','
            embed = discord.Embed(
                title=f'Coronavirus (COVID-19) Cases |{provst} {location} ',
                description='Data from [Data Repository](https://github.com/CSSEGISandData/COVID-19) by Johns Hopkins CSSE',
                colour=discord.Colour.red()
            )
            embed.set_image(url=f'attachment://graph.png')
            embed.add_field(name='Confirmed', value= f'**{int(confirmed)}** {change_confirmed}')
            embed.add_field(name='Deaths', value=f'**{int(deaths)}** {change_deaths}')
            embed.add_field(name='Recovered', value=f'**{int(recovered)}** {change_recovered}')
            embed.add_field(name='Mortality Rate', value=f'**{mortality_rate}%**')
            embed.set_footer(text= f'Updated {updated}')
            logger.info(f'Stat command used for{provst} {location}')
            await ctx.send(file=image, embed=embed)

        else:
            await ctx.send('There is no available data for this location')

def setup(client):
    client.add_cog(Stats(client))
