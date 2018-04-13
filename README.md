# rank-bot
rank-bot is a discord bot to be used along with the mobile game Star Wars Galaxy of Heroes. When deployed it will allow arena shards to keep track of whose turn it is to take a certain rank.
### Dependencies:
discord.py - https://github.com/Rapptz/discord.py

### Setup:
1. Set up a new bot user on discordapp.com/developers and obtain a bot token.
2. Copy config.ini.template and remove the .template extension
3. Paste your bot token into the bot_token field and change the bot prefix if desired
4. time_refresh.py will rotate every payout. Schedule this to run once per day using cron or another scheduler.
