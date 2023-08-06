# MineAlertBot

A simple Discord bot for Minecraft servers with numerous features planned.

## Commands

|Command|Description|
|---|-----|
| /hello | Just a simple greeting. |
| /seed   | Randomly generates a Minecraft world seed, ranging from -9223372036854775808 (the lowest possible Minecraft seed) to 9223372036854775807 (the highest possible Minecraft seed).|
| /about | Some information about the creation of this bot. |
| /set \<option\> \<value\> | Can choose to change the value of a setting from the list of options. |
| /serverinfo | Basic information about the server, including the number of online players, the maximum number of players, the server description, and version! |
| /servercheck | If not already used, this command starts the monitoring of the Minecraft server, and (currently) the status will be updated in the bot's server nickname. |
| /profile | Will retrieve information on a specified player's username, UUID, skin, and skin variant. |
| /coords | A Discord embed containing a list of coords users have added for a particular Minecraft server. |
| /addcoords \<name\> \<x\> \<y\> \<z\> | Users can add coords using this command. These added coords will then appear with /coords. |
