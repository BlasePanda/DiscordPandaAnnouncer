# Welcome Bot with Google Search

This is a Discord bot that welcomes users when they join a voice channel and performs a Google search based on user queries.

## Features

- Welcomes users with their names when they join a voice channel
- Responds to Google search queries with the top result
- Environment variable-based configuration

## Dependencies

- discord.py
- python-dotenv
- boto3
- pydub
- googlesearch-python
- ffmpeg

## Setup and Installation

1. Install dependencies using pip:

   ```pip install discord.py python-dotenv boto3 pydub googlesearch-python```

   Make sure to also have **ffmpeg** installed on your system.

2. Set up environment variables in a .env file in the project directory:

   - DISCORD_TOKEN=your_discord_token
   
   - FFMPEG_LOCATION=path_to_ffmpeg_executable
   
   - AWS_KEY_ID=your_aws_access_key_id
   
   - AWS_ACCESS_KEY=your_aws_secret_access_key
   
   - NAME_OF_THE_BOT=name_of_your_bot
   

   Replace the placeholders with your actual values.

3. Run the bot:

   python3 panda_bot.py

## Usage

- The bot will automatically welcome users when they join a voice channel.
- Use the $google <query> command to perform a Google search and receive the top result inside Discord chat.






[![(http://hits.dwyl.com/BlasePanda/DiscordPandaAnnouncer.svg)]](http://hits.dwyl.com/BlasePanda/DiscordPandaAnnouncer)

