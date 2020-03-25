import discord
import os
import config
import asyncio
import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler
from discord.utils import find
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from datetime import datetime

logging_client = google.cloud.logging.Client()
cloud_logger = logging_client.logger('covid-19')
logger = logging.getLogger('covid-19')
logger.setLevel(logging.DEBUG)
handler = CloudLoggingHandler(logging_client)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Coronavirus(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=when_mentioned_or('.c '),
            activity=discord.Game(name="Loading...")
            )
        self.remove_command('help')
        self.load()

    def load(self):
        for filename in os.listdir('./cogs'):
            try:
                if filename.endswith('.py'):
                    self.load_extension(f'cogs.{filename[:-3]}')
                    logger.info(f'{filename} loaded successfully')
            except Exception:
                logger.exception(f'{filename} failed to load')

    def unload(self):
        for filename in os.listdir('./cogs'):
            try:
                if filename.endswith('.py'):
                    self.unload_extension(f'cogs.{filename[:-3]}')
                    logger.info(f'{filename} unloaded successfully')
            except Exception:
                logger.exception(f'{filename} failed to unload')

    async def on_ready(self):
        await self.wait_until_ready()
        while True:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(bot.guilds)} servers | .c help'))
            self.unload_extension('cogs.Stats')
            self.load_extension('cogs.Stats')
            logger.info('Stats reloaded')
            await asyncio.sleep(600)

    async def on_guild_join(self, guild: discord.Guild):
        general = find(lambda x: x.name == 'general', guild.text_channels)
        channel = bot.get_channel(686768403339542687)
        embed_join = discord.Embed(description=f'Joined server **{guild.name}** with **{len(guild.members)}** members | Total: **{len(self.guilds)}** servers', timestamp=datetime.utcnow(), colour=discord.Colour.green())
        await channel.send(embed=embed_join)
        if general and general.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                    title='Coronavirus (COVID-19) Discord Bot',
                    description='Thanks for inviting me! | Use **.c help** for more info on commands \n •Please vote for me on [TOP.GG](https://top.gg/bot/683462722368700526/vote) <:dbl:689485017667469327>',
                    colour=discord.Colour.red()
                    )
            embed.add_field(name='Command Prefix', value='`.c` or `@mention`')
            users = 0
            for s in self.guilds:
                users += len(s.members)
            embed.add_field(name='Servers | Shards', value=f'<:servers:689502498251341953> {len(self.guilds)} | {len(self.shards)}')
            embed.add_field(name='Users', value=f'<:user:689502620590669912> {users}')
            embed.add_field(name='Bot Source Code', value='<:github:689501322969350158> [Github](https://github.com/picklejason/coronavirus-bot)')
            embed.add_field(name='Bot Invite', value='<:discord:689486285349715995> [Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)')
            embed.add_field(name='Donate', value='<:Kofi:689483361785217299> [Ko-fi](https://ko-fi.com/picklejason)')
            embed.set_footer(text='Made by PickleJason#5293 | Feel free to message me for any issues or suggestions')
            await general.send(embed=embed)

    async def on_guild_remove(self, guild: discord.Guild):
        channel = bot.get_channel(686768403339542687)
        embed_leave = discord.Embed(description=f'Left server **{guild.name}** with **{len(guild.members)}** members | Total: **{len(self.guilds)}** servers', timestamp=datetime.utcnow(), colour=discord.Colour.red())
        await channel.send(embed=embed_leave)

if __name__ == '__main__':
    bot = Coronavirus()
    bot.run(config.token)
