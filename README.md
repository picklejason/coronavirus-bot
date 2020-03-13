[![Discord Bots](https://top.gg/api/widget/683462722368700526.svg)](https://top.gg/bot/683462722368700526)

# Coronavirus Bot

This is a Discord bot coded in Python with [discord.py](https://discordpy.readthedocs.io/en/latest/) for providing info on the novel coronavirus (COVID-19) by [picklejason](https://github.com/picklejason).

Current features include stats showing total confirmed, deaths, and recovered cases. A graph is also displayed showing confirmed and recovered cases from late January to current day. In addition, the bot also can retrieve posts from the subreddit [r/Coronavirus](https://www.reddit.com/r/Coronavirus/).

Data for the stats and graph are from the [data repository](https://github.com/CSSEGISandData/COVID-19) by Johns Hopkins CSSE

## Usage

* Invite the bot to your server using the following link: [invite](https://discordapp.com/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)

* The command prefix for the bot is `.c ` or `@mention`

* Use the `help` command for further info

### Features

* `.c stat "all"` Stats of all locations

* <img align="center" style="float: centrer; margin: 0 10px 0 0;" src="https://i.gyazo.com/944b49e0e3445cd0991d38bc397459b1.png" height="430" width="350"/>

* `.c stat "other"` Stats of locations other than China

* <img align="center" style="float: center; margin: 0 10px 0 0;" src="https://i.gyazo.com/2a85c00a97c2ae36bebc18ab976bb881.png" height="430" width="350"/>

* `.c stat "country name"` Stats of a specific country

* <img align="center" style="float: centrer; margin: 0 10px 0 0;" src="https://i.gyazo.com/6971562b7ee89defa08bc76cee2d67d5.png" height="430" width="350"/>

* `.c reddit [category]` Reddit posts from [r/Coronavirus](https://www.reddit.com/r/Coronavirus/) | category = `Hot` `New` `Top` | Use :rewind: and :fast_forward: to scroll through

* <img align="center" style="float: center; margin: 0 10px 0 0;" src="https://i.gyazo.com/d0db2aca336b4dd6ad2847eacdb610e6.png" height="430" width="420"/>
