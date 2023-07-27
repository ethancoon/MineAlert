# The different settings for all functionality of the bot
config = {
    # Who can access which commands
    "command_config": {

    },
    # Modifying how the bot interacts with the Minecraft server
    "server_config": {
        # Placeholder values
        "server_name": None, # Should be a string when set
        "server_description": "Description",

        # Server version, may modify future functionality
        "server_version": None,
        
        # The domain or address of the server, in this case in the general format of ###.###.###.### 
        "server_ip": "###.###.###.###",
        # The default port for a Minecraft server is typically 25565
        "server_port": "25565",
    }
}

# Updates the global config so all files maintain synchronicity
def update_config(modified_group, modified_setting, new_value):
    config[modified_group][modified_setting] = new_value