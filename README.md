# Coronavirus Bot

This is a Discord bot coded in Python with [discord.py](https://discordpy.readthedocs.io/en/latest/) for providing info on the novel coronavirus (COVID-19) by [picklejason](https://github.com/picklejason).

Current features include stats showing total confirmed, deaths, and recovered cases. A graph is also displayed showing confirmed and recovered cases from late January to current day. In addition, the bot also can retrieve posts from the subreddit [r/Coronavirus](https://www.reddit.com/r/Coronavirus/).

Data for the stats and graph are from the [data repository](https://github.com/CSSEGISandData/COVID-19) by Johns Hopkins CSSE

## Usage

* Invite the bot to your server using the following link: [invite](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=0&scope=bot)

* The command prefix for the bot is `.c `

* Use the `help` command for further info

### Features

* `.c stat "all"` Stats of all locations

* <img align="center" style="float: centrer; margin: 0 10px 0 0;" src="https://i.gyazo.com/2610c48959a97f5bf5ce4f1ea50c7711.png" height="405" width="365"/>

* `.c stat "other"` Stats of locations other than China

* <img align="center" style="float: center; margin: 0 10px 0 0;" src="https://i.gyazo.com/0c2460d923e600a995cf2cddce328674.png" height="405" width="365"/>

* `.c stat "country name"` Stats of a specific country

* <img align="center" style="float: centrer; margin: 0 10px 0 0;" src="https://i.gyazo.com/8b4867f480eb6e18d7b29bc1134eb1da.png" height="405" width="365"/>

* `.c reddit [category]` Reddit posts from [r/Coronavirus](https://www.reddit.com/r/Coronavirus/) | category = `Hot` `New` `Top` | Use :rewind: and :fast_forward: to scroll through

* <img align="center" style="float: center; margin: 0 10px 0 0;" src="https://i.gyazo.com/e60c7f80e624c09d3e151e67d7f1fdcf.png" height="425" width="450"/>
