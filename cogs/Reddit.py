import discord
import praw
import os
import asyncio
import logging
import config
from datetime import datetime
from discord.ext import commands

logger = logging.getLogger('covid-19')

class Reddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    red = praw.Reddit(client_id=config.redditID,
                    client_secret=config.redditSecret,
                    password=config.redditPW,
                    user_agent=config.user_agent,
                    username=config.redditName)

    #Reddit Command | Returns 5 posts (Hot, New, Top) from the subreddit r/Coronavirus
    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def reddit(self, ctx, category = 'Hot'):

        icon = {'Hot' : '🔥',
                'New' : '🆕',
                'Top' : '🔝'}
        left = '⬅️'
        right = '➡️'
        reactions = [left, right]

        category = category.title()

        if category == 'Hot':
            submissions = list(self.red.subreddit('Coronavirus').hot(limit=5))
        elif category == 'New':
            submissions = list(self.red.subreddit('Coronavirus').new(limit=5))
        elif category == 'Top':
            submissions = list(self.red.subreddit('Coronavirus').top(limit=5))
        else:
            await ctx.send('Please enter one of the following categories: Hot, New, Top')
            return

        index = 1

        description = f'{icon[category]} | Bot needs permission to **manage messages** to flip pages'
        timestamp = datetime.utcnow()
        url = 'https://www.reddit.com/r/Coronavirus/'
        embed = discord.Embed(title='/r/Coronavirus', description=description, colour=discord.Colour.red(), timestamp=timestamp, url=url)

        for s in submissions:
            embed.add_field(name=f'<:upvote:689186080070959207> **{s.score}** | Posted by u/{s.author} on {datetime.fromtimestamp(s.created).strftime("%m/%d/%y %H:%M:%S")}', value=f'[{s.title}](https://www.reddit.com{s.permalink})', inline=False)

        embed.set_thumbnail(url='https://styles.redditmedia.com/t5_2x4yx/styles/communityIcon_ex5aikhvi3i41.png')
        embed.set_footer(text=f'Requested by {ctx.message.author} • Page {index} of 10', icon_url=ctx.message.author.avatar_url)
        msg = await ctx.send(embed=embed)
        logger.info('Reddit command used')

        def predicate(message, l, r):
            def check(reaction, user):
                if reaction.message.id != message.id or user == self.client.user:
                    return False
                if l and reaction.emoji == left and user == ctx.message.author:
                    return True
                if r and reaction.emoji == right and user == ctx.message.author:
                    return True
                return False
            return check

        while True:
            for reaction in reactions:
                await msg.add_reaction(reaction)
            l = index != 1
            r = index != 10
            try:
                react, self.user = await self.client.wait_for('reaction_add', check=predicate(msg, l, r), timeout=300)
            except asyncio.TimeoutError:
                try:
                    await msg.delete()
                except:
                    pass
            if react.emoji == left and index > 1:
                index -= 1
                await msg.remove_reaction(left, self.user)
            elif react.emoji == right and index < 10:
                index += 1
                await msg.remove_reaction(right, self.user)

            embed.clear_fields()
            number = index * 5

            if category == 'Hot':
                submissions = list(self.red.subreddit('Coronavirus').hot(limit=50))[number-5:number]
            elif category == 'New':
                submissions = list(self.red.subreddit('Coronavirus').new(limit=50))[number-5:number]
            elif category == 'Top':
                submissions = list(self.red.subreddit('Coronavirus').top(limit=50))[number-5:number]

            for s in submissions:
                embed.add_field(name=f'<:upvote:689186080070959207> **{s.score}** | Posted by u/{s.author} on {datetime.fromtimestamp(s.created).strftime("%m/%d/%y %H:%M:%S")}', value=f'[{s.title}](https://www.reddit.com{s.permalink})', inline=False)

            embed.set_footer(text=f'Requested by {ctx.message.author} • Page {index} of 10', icon_url=ctx.message.author.avatar_url)
            await msg.edit(embed=embed)

def setup(client):
    client.add_cog(Reddit(client))
