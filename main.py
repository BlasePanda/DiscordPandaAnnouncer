import pyttsx3
import time
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FFMPEG_LOCATION = os.getenv('FFMPEG')
AUDIO_FILE = os.getenv('AUDIO')


intents = discord.Intents.all()
client = discord.Client(intents=intents)
# bot = commands.Bot(command_prefix="?", intents=intents)


@client.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        # We are saving list of user so bot can access the last one
        list_of_users = []
        if str(member) != "PandaAnnouncer#3353":
            list_of_users.append(str(member))
            last_user = list_of_users[-1].split("#")

            engine = pyttsx3.init()
            engine.save_to_file(f"Welcome {last_user[0]}", "new.mp3")
            engine.runAndWait()

            user_voice_channel = after.channel.id
            # print(user_voice_channel)
            # print(member)
            channel = client.get_channel(user_voice_channel)

            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_LOCATION,
                                           source=AUDIO_FILE))
            audio = AudioSegment.from_file("new.mp3")

            duration = audio.duration_seconds
            time.sleep(float(duration))

            voice_client = channel.guild.voice_client
            await voice_client.disconnect()
            print('Bot joined the channel.')


client.run(TOKEN)
