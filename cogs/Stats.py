import discord
import io
import os
import pandas as pd
import matplotlib.pyplot as plt
import logging
import gc
from discord import File
from discord.ext import commands
from datetime import datetime
from utils.codes import states, alt_names, alpha2, alpha3

logger = logging.getLogger('covid-19')

class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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

        if len(location) == 2 or len(location) == 3:
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
        if location == 'ALL' or location == 'Other' or self.confirmed_df['Country/Region'].str.contains(location).any():

            updated = list(self.confirmed_df)[-1]

            #Parse Data
            if location == 'ALL':
                confirmed = self.confirmed_df.iloc[:,-1].sum()
                prev_confirmed = self.confirmed_df.iloc[:,-2].sum()
                deaths = self.deaths_df.iloc[:,-1].sum()
                prev_deaths = self.deaths_df.iloc[:,-2].sum()
                recovered = self.recovered_df.iloc[:,-1].sum()
                prev_recovered = self.recovered_df.iloc[:,-2].sum()

            elif location == 'Other':
                confirmed = self.confirmed_df[~self.confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                prev_confirmed = self.confirmed_df[~self.confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
                deaths = self.deaths_df[~self.deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                prev_deaths = self.deaths_df[~self.deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()
                recovered = self.recovered_df[~self.recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                prev_recovered = self.recovered_df[~self.recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-2].sum()

            else:
                if provst:
                    if self.confirmed_df['Province/State'].str.contains(provst).any():
                        confirmed = self.confirmed_df[self.confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,-1].sum()
                        prev_confirmed = self.confirmed_df[self.confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,-2].sum()
                        deaths = self.deaths_df[self.deaths_df['Province/State'].str.contains(provst, na=False)].iloc[:,-1].sum()
                        prev_deaths = self.deaths_df[self.deaths_df['Province/State'].str.contains(provst, na=False)].iloc[:,-2].sum()
                        recovered = self.recovered_df[self.recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,-1].sum()
                        prev_recovered = self.recovered_df[self.recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,-2].sum()
                    else:
                        await ctx.send('There is no available data for this location | Use **.c help** for more info on commands')
                        return
                else:
                    confirmed = self.confirmed_df[self.confirmed_df['Country/Region'].str.contains(location, na=False)].iloc[:,-1].sum()
                    prev_confirmed = self.confirmed_df[self.confirmed_df['Country/Region'].str.contains(location, na=False)].iloc[:,-2].sum()
                    deaths = self.deaths_df[self.deaths_df['Country/Region'].str.contains(location, na=False)].iloc[:,-1].sum()
                    prev_deaths = self.deaths_df[self.deaths_df['Country/Region'].str.contains(location, na=False)].iloc[:,-2].sum()
                    recovered = self.recovered_df[self.recovered_df['Country/Region'].str.contains(location, na=False)].iloc[:,-1].sum()
                    prev_recovered = self.recovered_df[self.recovered_df['Country/Region'].str.contains(location, na=False)].iloc[:,-2].sum()

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
                change_active_cases = f'(+{change_active_cases})'
            elif change_active_cases < 0:
                change_active_cases = f'({change_active_cases})'
            else:
                change_active_cases = ''

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

            description='•Stats update **daily** around 23:59 (UTC) | May slightly differ from other sources \n •React with 📈 for a linear graph or 📉 for a log graph (within 60s) \n •Please vote for me on [TOP.GG](https://top.gg/bot/683462722368700526/vote) <:dbl:689485017667469327>'
            embed = discord.Embed(
                title=f'Coronavirus (COVID-19) Cases  | {provst} {location} ',
                description=description,
                colour=discord.Colour.red()
            )

            embed.add_field(name='<:confirmed:689494326493184090> Confirmed', value= f'**{int(confirmed)}** {change_confirmed}')
            embed.add_field(name='<:deaths:689489690101153800> Deaths', value=f'**{int(deaths)}** {change_deaths}')
            embed.add_field(name='<:recovered:689490988808274003> Recovered', value=f'**{int(recovered)}** {change_recovered}')
            embed.add_field(name='<:activecases:689494177733410861> Active Cases', value=f'**{active_cases}** {change_active_cases}')
            embed.add_field(name='<:mortalityrate:689488380865544345> Mortality Rate', value=f'**{mortality_rate}%** {change_mortality_rate}')
            embed.add_field(name='<:recoveryrate:689492820125417521> Recovery Rate', value=f'**{recovery_rate}%** {change_recovery_rate}')
            embed.set_footer(text= f'Updated {updated} | Support me at https://ko-fi.com/picklejason')
            # logger.info(f'Stat command used for {provst} {location} by {ctx.message.author}({ctx.message.author.id}) in {ctx.message.guild}({ctx.message.guild.id})')
            msg = await ctx.send(embed=embed)

            linear = '📈'
            log = '📉'
            graphs = [linear, log]
            def predicate(message):
                def check(reaction, user):
                    if reaction.message.id != message.id or user == self.bot.user:
                        return False
                    if reaction.emoji == linear and user == ctx.message.author:
                        return True
                    if reaction.emoji == log and user == ctx.message.author:
                        return True
                    return False
                return check

            async def plot(graph_type):

                fig = plt.figure(dpi=150)
                plt.style.use('dark_background')

                if location == 'ALL':
                    if graph_type == 'linear':
                        ax = self.confirmed_df.iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                        ax = self.recovered_df.iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')
                    elif graph_type == 'log':
                        ax = self.confirmed_df.iloc[:,4:].sum().plot(label='Confirmed', logy=True, color='orange', marker='o')
                        ax = self.recovered_df.iloc[:,4:].sum().plot(label='Recovered', logy=True, color='lightgreen', marker='o')
                elif location == 'Other':
                    if graph_type == 'linear':
                        ax = self.confirmed_df[~self.confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                        ax = self.recovered_df[~self.recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')
                    elif graph_type == 'log':
                        ax = self.confirmed_df[~self.confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,4:].sum().plot(label='Confirmed', logy=True, color='orange', marker='o')
                        ax = self.recovered_df[~self.recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,4:].sum().plot(label='Recovered', logy=True, color='lightgreen', marker='o')
                else:
                    if provst:
                        if self.confirmed_df['Province/State'].str.contains(provst).any():
                            if provst in states:
                                if graph_type == 'linear':
                                    ax = self.confirmed_df[self.confirmed_df['Province/State'].str.contains(f'{provst}|{states_abr}', na=False)].iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                                    ax = self.recovered_df[self.recovered_df['Province/State'].str.contains(f'{provst}|{states_abr}', na=False)].iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')
                                elif graph_type == 'log':
                                    ax = self.confirmed_df[self.confirmed_df['Province/State'].str.contains(f'{provst}|{states_abr}', na=False)].iloc[:,4:].sum().plot(label='Confirmed', logy=True, color='orange', marker='o')
                                    ax = self.recovered_df[self.recovered_df['Province/State'].str.contains(f'{provst}|{states_abr}', na=False)].iloc[:,4:].sum().plot(label='Recovered', logy=True, color='lightgreen', marker='o')
                            else:
                                if graph_type == 'linear':
                                    ax = self.confirmed_df[self.confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                                    ax = self.recovered_df[self.recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')
                                elif graph_type == 'log':
                                    ax = self.confirmed_df[self.confirmed_df['Province/State'].str.contains(provst, na=False)].iloc[:,4:].sum().plot(label='Confirmed', logy=True, color='orange', marker='o')
                                    ax = self.recovered_df[self.recovered_df['Province/State'].str.contains(provst, na=False)].iloc[:,4:].sum().plot(label='Recovered', logy=True, color='lightgreen', marker='o')
                        else:
                            await ctx.send('There is no available data for this location | Use **.c help** for more info on commands')
                            return
                    else:
                        if graph_type == 'linear':
                            ax = self.confirmed_df[self.confirmed_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                            ax = self.recovered_df[self.recovered_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')
                        elif graph_type == 'log':
                            ax = self.confirmed_df[self.confirmed_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Confirmed', logy=True, color='orange', marker='o')
                            ax = self.recovered_df[self.recovered_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Recovered', logy=True, color='lightgreen', marker='o')

                if graph_type == 'linear':
                    filename = './graphs/lineargraph.png'
                    ax.set_ylim(0)
                    plt.title('Linear Graph')

                elif graph_type == 'log':
                    filename = './graphs/loggraph.png'
                    ax.set_ylim(10**2)
                    plt.title('Logarithmic Graph')
                    plt.minorticks_off()

                #Graph
                ax.legend(loc='upper left', fancybox=True, facecolor='0.2')
                ax.yaxis.grid()
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
                locs, _ = plt.yticks()
                ylabels = []
                for l in locs:
                    lab = str(int(l)).replace('00000000', '00M').replace('0000000', '0M').replace('000000', 'M').replace('00000', '00K').replace('0000', '0K').replace('000', 'K')
                    if not ('K' in lab or 'M' in lab):
                        lab = '{:,}'.format(int(lab))
                    ylabels.append(lab)
                plt.yticks(locs, ylabels)
                plt.savefig(filename, transparent=True)
                plt.cla()
                plt.close(fig)
                plt.close('all')
                gc.collect()
                with open(filename, 'rb') as f:
                    file = io.BytesIO(f.read())
                image = discord.File(file, filename=f'{graph_type}graph.png')

                return image

            for graph in graphs:
                await msg.add_reaction(graph)

            while True:
                react, self.user = await self.bot.wait_for('reaction_add', check=predicate(msg), timeout=60)
                graph_type = ''
                if react.emoji == linear:
                    logger.info(f'Linear graph used for {provst} {location}')
                    graph_type = 'linear'
                    await msg.remove_reaction(linear, self.user)
                    await msg.remove_reaction(linear, self.bot.user)
                    image = await plot(graph_type)
                    embed.set_image(url=f'attachment://{graph_type}graph.png')
                    await msg.delete()
                    await ctx.send(file=image, embed=embed)

                elif react.emoji == log:
                    logger.info(f'Log graph used for {provst} {location}')
                    graph_type = 'log'
                    await msg.remove_reaction(log, self.user)
                    await msg.remove_reaction(log, self.bot.user)
                    image = await plot(graph_type)
                    embed.set_image(url=f'attachment://{graph_type}graph.png')
                    await msg.delete()
                    await ctx.send(file=image, embed=embed)

        else:
            await ctx.send('There is no available data for this location | Use **.c help** for more info on commands')

def setup(bot):
    bot.add_cog(Stats(bot))
