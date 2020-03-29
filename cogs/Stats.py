import discord
import io
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import asyncio
import gc
import requests
from datetime import datetime
from discord.ext import commands
from utils.codes import states, alt_names, alpha2, alpha3, JHU_names

logger = logging.getLogger('covid-19')

class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Parse Data
    confirmed_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    deaths_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    recovered_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
    confirmed_df = pd.read_csv(confirmed_url, error_bad_lines=False).dropna(axis=1, how='all')
    deaths_df = pd.read_csv(deaths_url, error_bad_lines=False).dropna(axis=1, how='all')
    recovered_df = pd.read_csv(recovered_url, error_bad_lines=False).dropna(axis=1, how='all')

    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }

    wom_url = 'https://www.worldometers.info/coronavirus/'
    us_wom_url = 'https://www.worldometers.info/coronavirus/country/us/'
    r = requests.get(wom_url, headers=header)
    r1 = requests.get(us_wom_url, headers=header)

    df_list = pd.read_html(r.text)
    us_df_list = pd.read_html(r1.text)
    df = df_list[0].replace(np.nan, 0).replace(',', '', regex=True)
    us_df = us_df_list[0].replace(np.nan, 0).replace(',', '', regex=True)

    def getTotal(self, type):
        df_all = self.df[self.df['Country,Other'].str.match('Total:', na=False)][type].values[0]
        return df_all

    #type: 'Country,Other', 'TotalCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'ActiveCases', 'Serious,Critical'
    def getLocation(self, location, type):
        df_loc = self.df[self.df['Country,Other'].str.match(location, na=False)][type].values[0]
        return df_loc

    def getState(self, state, type):
        df_state = self.us_df[self.us_df['USAState'].str.match(state, na=False)][type].values[0]
        return df_state

    #Statistics Command
    @commands.command(name='stat', aliases=['stats', 'statistic', 's', 'cases'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def stat(self, ctx, location = 'ALL', state = ''):

        #Parameter formatting | Check if country code
        if len(location) == 2 or len(location) == 3:
            location = location.upper()
        else:
            location = location.title()
        if len(state) == 2:
            state = state.upper()
        else:
            state = state.title()

        if location in alpha2:
            location = alpha2[location]
        elif location in alpha3:
            location = alpha3[location]
        elif location in alt_names:
            location = alt_names[location]

        if state in states:
            state = states[state]

        #Check if data exists for location
        if location == 'ALL' or (location in list(alpha2.values())) :

            #Parse and sum data
            if location == 'ALL':
                confirmed = self.getTotal('TotalCases')
                new_confirmed = self.getTotal('NewCases')
                deaths = self.getTotal('TotalDeaths')
                new_deaths = self.getTotal('NewDeaths')
                recovered = self.getTotal('TotalRecovered')
                active = self.getTotal('ActiveCases')

            else:
                if state:
                    if state in list(states.values()):
                        confirmed = self.getState(state, 'TotalCases')
                        new_confirmed = self.getState(state, 'NewCases')
                        deaths = self.getState(state, 'TotalDeaths')
                        new_deaths = self.getState(state, 'NewDeaths')
                        active = self.getState(state, 'ActiveCases')
                    elif location == 'Canada':
                        confirmed = self.confirmed_df[self.confirmed_df['Province/State'].str.contains(state, na=False)].iloc[:,-1].sum()
                        prev_confirmed = self.confirmed_df[self.confirmed_df['Province/State'].str.contains(state, na=False)].iloc[:,-2].sum()
                        deaths = self.deaths_df[self.deaths_df['Province/State'].str.contains(state, na=False)].iloc[:,-1].sum()
                        prev_deaths = self.deaths_df[self.deaths_df['Province/State'].str.contains(state, na=False)].iloc[:,-2].sum()
                        recovered = self.recovered_df[self.recovered_df['Province/State'].str.contains(state, na=False)].iloc[:,-1].sum()
                        active = confirmed - deaths - recovered
                        new_confirmed = confirmed - prev_confirmed
                        new_deaths = deaths - prev_deaths
                    else:
                        await ctx.send('There is no available data for this location | Use **.c help** for more info on commands')
                else:
                    confirmed = self.getLocation(location, 'TotalCases')
                    new_confirmed = self.getLocation(location, 'NewCases')
                    deaths = self.getLocation(location, 'TotalDeaths')
                    new_deaths = self.getLocation(location, 'NewDeaths')
                    recovered = self.getLocation(location, 'TotalRecovered')
                    active = self.getLocation(location, 'ActiveCases')

            if len(state) > 0:
                name =  f'Coronavirus (COVID-19) Cases | {state}, {location}'
            else:
                name = f'Coronavirus (COVID-19) Cases | {location}'

            if int(new_confirmed) > 0:
                new_confirmed = f'(+{int(new_confirmed)})'
            elif new_confirmed == 0:
                new_confirmed = ''

            if int(new_deaths) > 0:
                new_deaths = f'(+{int(new_deaths)})'
            elif new_deaths == 0:
                new_deaths = ''

            if confirmed != 0:
                mortality_rate = round((deaths/confirmed * 100), 2)
                if state:
                    pass
                else:
                    recovery_rate = round((recovered/confirmed * 100), 2)

            if state:
                description='**Vote** <:dbl:689485017667469327> [TOP.GG](https://top.gg/bot/683462722368700526/vote) | **Donate** <:Kofi:689483361785217299> [Ko-fi](https://ko-fi.com/picklejason) | **Join** <:discord:689486285349715995> [Support Server](https://discord.gg/tVN2UTa)'
            else:
                description='**Vote** <:dbl:689485017667469327> [TOP.GG](https://top.gg/bot/683462722368700526/vote) | **Donate** <:Kofi:689483361785217299> [Ko-fi](https://ko-fi.com/picklejason) | **Join** <:discord:689486285349715995> [Support Server](https://discord.gg/tVN2UTa) \n React with 📈 for a **linear** graph or 📉 for a **log** graph'
            embed = discord.Embed(
                description=description,
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
                )
            embed.add_field(name='<:confirmed:689494326493184090> Confirmed', value= f'**{int(confirmed)}** {new_confirmed}')
            embed.add_field(name='<:deaths:689489690101153800> Deaths', value=f'**{int(deaths)}** {new_deaths}')
            if state:
                embed.set_author(name=name, url='https://www.worldometers.info/coronavirus/country/us/', icon_url='https://images.discordapp.net/avatars/683462722368700526/70c1743a2d87a44116f857a88bb107e0.png?size=512')
                embed.add_field(name='<:activecases:689494177733410861> Active Cases', value=f'**{int(active)}**')
                embed.add_field(name='<:mortalityrate:689488380865544345> Mortality Rate', value=f'**{mortality_rate}%**')

            else:
                embed.set_author(name=name, url='https://www.worldometers.info/coronavirus/', icon_url='https://images.discordapp.net/avatars/683462722368700526/70c1743a2d87a44116f857a88bb107e0.png?size=512')
                embed.add_field(name='<:recovered:689490988808274003> Recovered', value=f'**{int(recovered)}**')
                embed.add_field(name='<:activecases:689494177733410861> Active Cases', value=f'**{int(active)}**')
                embed.add_field(name='<:mortalityrate:689488380865544345> Mortality Rate', value=f'**{mortality_rate}%**')
                embed.add_field(name='<:recoveryrate:689492820125417521> Recovery Rate', value=f'**{recovery_rate}%**')
            embed.set_footer(text='Data from Worldometer and Johns Hopkins CSSE')
            msg = await ctx.send(embed=embed)

            #Graph reactions
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

            if location in JHU_names:
                location = JHU_names[location]

            #Plot graph function
            async def plot(graph_type):

                fig = plt.figure(dpi=150)
                plt.style.use('dark_background')

                if location == 'ALL':
                    if graph_type == 'linear':
                        ax = self.confirmed_df.iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                        ax = self.recovered_df.iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')
                        ax = self.deaths_df.iloc[:,4:].sum().plot(label='Deaths', color='red', marker='o')
                    elif graph_type == 'log':
                        ax = self.confirmed_df.iloc[:,4:].sum().plot(label='Confirmed', logy=True, color='orange', marker='o')
                        ax = self.recovered_df.iloc[:,4:].sum().plot(label='Recovered', logy=True, color='lightgreen', marker='o')
                        ax = self.deaths_df.iloc[:,4:].sum().plot(label='Deaths', logy=True, color='red', marker='o')

                else:
                    if graph_type == 'linear':
                        ax = self.confirmed_df[self.confirmed_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Confirmed', color='orange', marker='o')
                        ax = self.recovered_df[self.recovered_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Recovered', color='lightgreen', marker='o')
                        ax = self.deaths_df[self.deaths_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Deaths', color='red', marker='o')
                    elif graph_type == 'log':
                        ax = self.confirmed_df[self.confirmed_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Confirmed', logy=True, color='orange', marker='o')
                        ax = self.recovered_df[self.recovered_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Recovered', logy=True, color='lightgreen', marker='o')
                        ax = self.deaths_df[self.deaths_df['Country/Region'].str.contains(location, na=False)].iloc[:,4:].sum().plot(label='Deaths', color='red', marker='o')

                if graph_type == 'linear':
                    filename = './graphs/lineargraph.png'
                    ax.set_ylim(0)
                    plt.title('Linear Graph')

                elif graph_type == 'log':
                    filename = './graphs/loggraph.png'
                    ax.set_ylim(10**2)
                    plt.title('Logarithmic Graph')
                    plt.minorticks_off()

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

            if state:
                pass
            else:
                for graph in graphs:
                    await msg.add_reaction(graph)

            while True:
                try:
                    react, self.user = await self.bot.wait_for('reaction_add', check=predicate(msg), timeout=30)
                except asyncio.TimeoutError:
                    description='**Vote** <:dbl:689485017667469327> [TOP.GG](https://top.gg/bot/683462722368700526/vote) | **Donate** <:Kofi:689483361785217299> [Ko-fi](https://ko-fi.com/picklejason) | **Join** <:discord:689486285349715995> [Support Server](https://discord.gg/tVN2UTa)'
                    embed = discord.Embed(
                        description=description,
                        colour=discord.Colour.red(),
                        timestamp=datetime.utcnow()
                        )
                    embed.set_author(name=name, url='https://www.worldometers.info/coronavirus/', icon_url='https://images.discordapp.net/avatars/683462722368700526/70c1743a2d87a44116f857a88bb107e0.png?size=512')
                    embed.add_field(name='<:confirmed:689494326493184090> Confirmed', value= f'**{int(confirmed)}** {new_confirmed}')
                    embed.add_field(name='<:deaths:689489690101153800> Deaths', value=f'**{int(deaths)}** {new_deaths}')
                    embed.add_field(name='<:recovered:689490988808274003> Recovered', value=f'**{int(recovered)}**')
                    embed.add_field(name='<:activecases:689494177733410861> Active Cases', value=f'**{int(active)}**')
                    embed.add_field(name='<:mortalityrate:689488380865544345> Mortality Rate', value=f'**{mortality_rate}%**')
                    embed.add_field(name='<:recoveryrate:689492820125417521> Recovery Rate', value=f'**{recovery_rate}%**')
                    embed.set_footer(text='Data from Worldometer and Johns Hopkins CSSE')
                    await msg.edit(embed=embed)
                    await msg.remove_reaction(linear, self.bot.user)
                    await msg.remove_reaction(log, self.bot.user)

                graph_type = ''
                if react.emoji == linear:
                    graph_type = 'linear'
                    await msg.remove_reaction(linear, self.user)
                    await msg.remove_reaction(linear, self.bot.user)
                    image = await plot(graph_type)
                    embed.set_image(url=f'attachment://{graph_type}graph.png')
                    await msg.delete()
                    await ctx.send(file=image, embed=embed)

                elif react.emoji == log:
                    graph_type = 'log'
                    await msg.remove_reaction(log, self.user)
                    await msg.remove_reaction(log, self.bot.user)
                    image = await plot(graph_type)
                    embed.set_image(url=f'attachment://{graph_type}graph.png')
                    await msg.delete()
                    await ctx.send(file=image, embed=embed)

                if os.path.exists(f'./graphs/{graph_type}graph.png'):
                    os.remove(f'./graphs/{graph_type}graph.png')
                else:
                    pass

        else:
            await ctx.send('There is no available data for this location | Use **.c help** for more info on commands')

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def graph(self, ctx, graph_type, type, *location):

        countries = []
        #Parameter formatting | Check if country code
        for country in location:
            if len(country) == 2 or len(country) == 3:
                country = country.upper()
            else:
                country = country.title()

            if country in alpha2:
                country = alpha2[country]
            elif country in alpha3:
                country = alpha3[country]
            elif country in alt_names:
                country = alt_names[country]

            if country in JHU_names:
                country = JHU_names[country]

            countries.append(country)

        fig = plt.figure(dpi=150)
        plt.style.use('dark_background')

        for country in countries:
            if country in list(alpha2.values()) or country in list(JHU_names.values()):
                if graph_type == 'linear':
                    if type == 'confirmed':
                        ax = self.confirmed_df[self.confirmed_df['Country/Region'].str.contains(country, na=False)].iloc[:,4:].sum().plot(label=country)
                    elif type == 'recovered':
                        ax = self.recovered_df[self.recovered_df['Country/Region'].str.contains(country, na=False)].iloc[:,4:].sum().plot(label=country)
                    elif type == 'deaths':
                        ax = self.deaths_df[self.deaths_df['Country/Region'].str.contains(country, na=False)].iloc[:,4:].sum().plot(label=country)

                elif graph_type == 'log':
                    if type == 'confirmed':
                        ax = self.confirmed_df[self.confirmed_df['Country/Region'].str.contains(country, na=False)].iloc[:,4:].sum().plot(label=country, logy=True)
                    elif type == 'recovered':
                        ax = self.recovered_df[self.recovered_df['Country/Region'].str.contains(country, na=False)].iloc[:,4:].sum().plot(label=country, logy=True)
                    elif type == 'deaths':
                        ax = self.deaths_df[self.deaths_df['Country/Region'].str.contains(country, na=False)].iloc[:,4:].sum().plot(label=country, logy=True)
            else:
                await ctx.send(f'{country} is not a valid location', delete_after=3)

        if graph_type == 'linear':
            filename = './graphs/lineargraph.png'
            ax.set_ylim(0)
            plt.title(f'{type.title()} Linear Graph')

        elif graph_type == 'log':
            filename = './graphs/loggraph.png'
            ax.set_ylim(10**2)
            plt.title(f'{type.title()} Logarithmic Graph')
            plt.minorticks_off()

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
        # description='**Vote** <:dbl:689485017667469327> [TOP.GG](https://top.gg/bot/683462722368700526/vote) | **Donate** <:Kofi:689483361785217299> [Ko-fi](https://ko-fi.com/picklejason) | **Join** <:discord:689486285349715995> [Support Server](https://discord.gg/tVN2UTa)'
        embed = discord.Embed(
            # description=description,
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
            )

        embed.set_image(url=f'attachment://{graph_type}graph.png')
        embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        await ctx.send(file=image, embed=embed)

        if os.path.exists(f'./graphs/{graph_type}graph.png'):
            os.remove(f'./graphs/{graph_type}graph.png')
        else:
            pass

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def vcset(self, ctx, channel: discord.VoiceChannel, *, location = 'All', state = ''):

        if len(location) == 2:
            location = location.upper()
        else:
            location = location.title()
        if len(state) == 2:
            state = state.upper()
        else:
            state = state.title()
        if location in alpha2:
            location = alpha2[location]
        elif location in alpha3:
            location = alpha3[location]
        elif location in alt_names:
            location = alt_names[location]
        if state in states:
            state = states[state]

        while True:
            #Check if data exists for location
            if location == 'All' or location == 'Other' or self.confirmed_df['Country/Region'].str.contains(location).any():
                #Parse Data
                if location == 'All':
                    confirmed = self.confirmed_df.iloc[:,-1].sum()
                    deaths = self.deaths_df.iloc[:,-1].sum()
                    # recovered = self.recovered_df.iloc[:,-1].sum()
                elif location == 'Other':
                    confirmed = self.confirmed_df[~self.confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                    deaths = self.deaths_df[~self.deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                    # recovered = self.recovered_df[~self.recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                else:
                    confirmed = self.confirmed_df[self.confirmed_df['Country/Region'].str.match(location, na=False)].iloc[:,-1].sum()
                    deaths = self.deaths_df[self.deaths_df['Country/Region'].str.match(location, na=False)].iloc[:,-1].sum()
                    # recovered = self.recovered_df[self.recovered_df['Country/Region'].str.match(location, na=False)].iloc[:,-1].sum()
            else:
                await ctx.send('There is no available data for this location | Use **.c help** for more info on commands')

            await channel.edit(name=f'😷 {location}: {str(confirmed)}')

            await asyncio.sleep(86400)

def setup(bot):
    bot.add_cog(Stats(bot))
