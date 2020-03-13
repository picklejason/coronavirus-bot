import discord
import os
import sys
import config
import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler
from discord import File
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
            command_prefix=when_mentioned_or(".c "),
            activity=discord.Game(name="Loading..."),
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
        #Waits until the client's internal cache is all ready
        await self.wait_until_ready()
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(client.guilds)} servers | .c help'))

    async def on_guild_join(self, guild: discord.Guild):
        general = find(lambda x: x.name == 'general', guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                    title='Coronavirus (COVID-19) Discord Bot',
                    description='Thanks for inviting me! | Use **.c help** for more info on commands \n Please vote for me on [TOP.GG](https://top.gg/bot/683462722368700526/vote) 👍',
                    colour=discord.Colour.red()
                )
            embed.add_field(name='Command Prefix', value='.c or @mention')
            users = 0
            for s in self.guilds:
                users += len(s.members)
            embed.add_field(name='Servers', value=len(self.guilds))
            embed.add_field(name='Users', value=users)
            embed.add_field(name='Bot Invite', value='[Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)')
            embed.add_field(name ='Bot Source Code', value='[Github](https://github.com/picklejason/coronavirus-bot)')

            logger.info(f'Server joined | Currently on {len(self.guilds)} servers')
            await general.send(embed=embed)

if __name__ == '__main__':
    client = Coronavirus()
    client.run(config.token)
