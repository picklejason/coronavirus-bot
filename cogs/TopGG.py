import dbl
import discord
import config
from discord.ext import commands

class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, client):
        self.client = client
        self.token = config.dbl_token # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.client, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

    async def on_guild_post():
        print("Server count posted successfully")

def setup(client):
    client.add_cog(TopGG(client))
