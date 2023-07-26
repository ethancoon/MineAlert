# MineAlertBot

A Discord bot for Minecraft servers. Planned features include server uptime, player counts, version number, and songs from Minecraft. 

## Commands
|Command|Description|
|---|-----|
| !hello | Just a simple greeting. |
| !seed   | Randomly generates a Minecraft world seed, ranging from -9223372036854775808 (the lowest possible Minecraft seed) to 9223372036854775807 (the highest possible Minecraft seed).|
| !about | Some information about the creation of this bot. |
| !setip | Sets the IP the bot will look for in order to get information on the Minecraft server |
| !setport | Sets the port the bot will look for in order to get information on the Minecraft server (your query port and Minecraft server port should be the same!) |
| !serverinfo | Basic information about the server, including the number of online players, the maximum number of players, the server description, and version! |
| !serverstatus | If not already used, this command starts the monitoring of the Minecraft server, and (currently) the status will be updated in the bot's server nickname |

## Planned Features

- Minecraft server uptime statistic
- Alert if Minecraft server goes down
- !modpack command
- Ability to download world backups
- Using the Minecraft console from Discord server
- Support for multiple Minecraft servers per Discord server
- Icons of player heads for active player list
- Many more options for customization of bot functionality