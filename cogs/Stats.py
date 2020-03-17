import discord
import io
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import logging
from discord import File
from discord.ext import commands
from datetime import datetime
from utils.codes import states, alt_names, alpha2, alpha3

logger = logging.getLogger('covid-19')

class Stats(commands.Cog):

    def __init__(self, client):
        self.client = client

    confirmed_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    deaths_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
    recovered_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

    confirmed_df = pd.read_csv(confirmed_url, error_bad_lines=False).dropna(axis=1, how='all')
    deaths_df = pd.read_csv(deaths_url, error_bad_lines=False).dropna(axis=1, how='all')
    recovered_df = pd.read_csv(recovered_url, error_bad_lines=False).dropna(axis=1, how='all')

    #Statistics Command | Provides Confirmed, Deaths, and Recovered | Mortality Rate: Deaths/Confirmed | Includes Graph
    @commands.command(name='stat', aliases=['stats', 'statistic', 's', 'cases'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def stat(self, ctx, location = 'All', provst = ''):

        if len(location) == 2:
            location = location.upper()
        else:
            location = location.title()

        if len(provst) == 2:
            provst = provst.upper()
        else:
            provst = provst.title()

        if location in alpha2:
            location = alpha2[location]

        elif location in alpha3:
            location = alpha3[location]

        elif location in alt_names:
            location = alt_names[location]

        if provst in states:
            provst = states[provst]

        #Check if data exists for location
        if location == 'All' or location == 'Other' or self.confirmed_df['Country/Region'].str.contains(location).any():

            updated = list(self.confirmed_df)[-1]
            mpl.rcParams.update({'figure.max_open_warning': 0})
            plt.style.use('dark_background')
            fig = plt.figure(dpi=200)

            #Parse Data
            if location == 'All':
                confirmed = self.confirmed_df.iloc[:,-1].sum()
                prev_confirmed = self.confirmed_df.iloc[:,-2].sum()
                deaths = self.deaths_df.iloc[:,-1].sum()
                prev_deaths = self.deaths_df.iloc[:,-2].sum()
                recovered = self.recovered_df.iloc[:,-1].sum()
                prev_recovered = self.recovered_df.iloc[:,-2].sum()
                ax = self.confirmed_df.iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                ax = self.recovered_df.iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')

            elif location == 'Other':
                confirmed = self.confirmed_df[~self.confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                prev_confirmed = self.confirmed_df[~self.confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
                deaths = self.deaths_df[~self.deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                prev_deaths = self.deaths_df[~self.deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
                recovered = self.recovered_df[~self.recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                prev_recovered = self.recovered_df[~self.recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
                ax = self.confirmed_df[~self.confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                ax = self.recovered_df[~self.recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')

            else:
                if provst:
                    if self.confirmed_df['Province/State'].str.match(provst).any():
                        confirmed = self.confirmed_df[self.confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,-1].sum()
                        prev_confirmed = self.confirmed_df[self.confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,-2].sum()
                        deaths = self.deaths_df[self.deaths_df['Province/State'].str.contains(provst, na=False)].iloc[:,-1].sum()
                        prev_deaths = self.deaths_df[self.deaths_df['Province/State'].str.contains(provst, na=False)].iloc[:,-2].sum()
                        recovered = self.recovered_df[self.recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,-1].sum()
                        prev_recovered = self.recovered_df[self.recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,-2].sum()
                        if provst in states:
                            states_abr = dict((v,k) for k,v in states.items())[provst]
                            ax = self.confirmed_df[self.confirmed_df['Province/State'].str.contains(f'{provst}|{states_abr}', na=False)].iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                            ax = self.recovered_df[self.recovered_df['Province/State'].str.contains(f'{provst}|{states_abr}', na=False)].iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')
                        else:
                            ax = self.confirmed_df[self.confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                            ax = self.recovered_df[self.recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')
                    else:
                        await ctx.send('There is no available data for this location | Use **.c help** for more info on commands')
                        return
                else:
                    confirmed = self.confirmed_df[self.confirmed_df['Country/Region'].str.match(location, na=False)].iloc[:,-1].sum()
                    prev_confirmed = self.confirmed_df[self.confirmed_df['Country/Region'].str.match(location, na=False)].iloc[:,-2].sum()
                    deaths = self.deaths_df[self.deaths_df['Country/Region'].str.match(location, na=False)].iloc[:,-1].sum()
                    prev_deaths = self.deaths_df[self.deaths_df['Country/Region'].str.match(location, na=False)].iloc[:,-2].sum()
                    recovered = self.recovered_df[self.recovered_df['Country/Region'].str.match(location, na=False)].iloc[:,-1].sum()
                    prev_recovered = self.recovered_df[self.recovered_df['Country/Region'].str.match(location, na=False)].iloc[:,-2].sum()
                    ax = self.confirmed_df[self.confirmed_df['Country/Region'].str.match(location, na=False)].iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                    ax = self.recovered_df[self.recovered_df['Country/Region'].str.match(location, na=False)].iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')

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

            active_cases = int(confirmed - deaths - recovered)
            prev_active_cases = int(prev_confirmed - prev_deaths - prev_recovered)
            change_active_cases = active_cases - prev_active_cases
            if change_active_cases > 0:
                change_active_cases = f'+{change_active_cases}'

            if confirmed != 0:
                mortality_rate = round((deaths/confirmed * 100), 2)
                recovery_rate = round((recovered/confirmed * 100), 2)
            if prev_confirmed != 0:
                prev_mortality_rate = round((prev_deaths/prev_confirmed * 100), 2)
                change_mortality_rate = round((mortality_rate - prev_mortality_rate), 2)
                prev_recovery_rate = round((prev_recovered/prev_confirmed * 100), 2)
                change_recovery_rate = round((recovery_rate - prev_recovery_rate), 2)
                if change_mortality_rate > 0:
                    change_mortality_rate = f'(+{change_mortality_rate}%)'
                elif change_mortality_rate < 0:
                    change_mortality_rate = f'({change_mortality_rate}%)'
                else:
                    change_mortality_rate = ''

                if change_recovery_rate > 0:
                    change_recovery_rate = f'(+{change_recovery_rate}%)'
                elif change_recovery_rate < 0:
                    change_recovery_rate = f'({change_recovery_rate}%)'
                else:
                    change_recovery_rate = ''
            else:
                mortality_rate = 0
                recovery_rate = 0
                change_mortality_rate = ''
                change_recovery_rate = ''

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
            filename = './graphs/graph.png'
            plt.savefig(filename, transparent=True)
            plt.close(fig)
            with open(filename, 'rb') as f:
                file = io.BytesIO(f.read())
            image = discord.File(file, filename='graph.png')

            if location == 'US' or provst:
                description = 'Data from [Data Repository](https://github.com/CSSEGISandData/COVID-19) by Johns Hopkins CSSE \n Stats update **daily** | May be slightly inconsistent with other sources \n Use **.c help** for more info on commands'
                if len(provst) > 0:
                    provst = ' ' + provst + ','

            else:
                description='Data from [Data Repository](https://github.com/CSSEGISandData/COVID-19) by Johns Hopkins CSSE \n Stats update **daily** | May be slightly inconsistent with other sources \n Use **.c help** for more info on commands'
            embed = discord.Embed(
                title=f'Coronavirus (COVID-19) Cases |{provst} {location} ',
                description=description,
                colour=discord.Colour.red()
            )
            embed.set_image(url=f'attachment://graph.png')
            embed.add_field(name='Confirmed', value= f'**{int(confirmed)}** {change_confirmed}')
            embed.add_field(name='Deaths', value=f'**{int(deaths)}** {change_deaths}')
            embed.add_field(name='Recovered', value=f'**{int(recovered)}** {change_recovered}')
            embed.add_field(name='Active Cases', value=f'**{active_cases}** ({change_active_cases})')
            embed.add_field(name='Mortality Rate', value=f'**{mortality_rate}%** {change_mortality_rate}')
            embed.add_field(name='Recovery Rate', value=f'**{recovery_rate}%** {change_recovery_rate}')
            embed.set_footer(text= f'Updated {updated} | Support me at https://ko-fi.com/picklejason')
            logger.info('Stat command used for {provst} {location}')
            await ctx.send(file=image, embed=embed)

        else:
            await ctx.send('There is no available data for this location | Use **.c help** for more info on commands')

def setup(client):
    client.add_cog(Stats(client))
