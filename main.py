import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
import boto3
from pydub import AudioSegment
from googlesearch import search
import asyncio
import os

load_dotenv()
#Your token and other sensitive information should be loaded from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
FFMPEG_LOCATION = os.getenv('FFMPEG_LOCATION')
AWS_REGION = "eu-central-1"
AWS_ACCESS_KEY_ID = os.getenv('AWS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
NAME_OF_THE_BOT = os.getenv('NAME_OF_THE_BOT')


intents = discord.Intents.all()
client = commands.Bot(command_prefix='$', intents=intents)

# Set up Amazon Polly client
polly_client = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
).client('polly')


@client.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        list_of_users = [str(member)]
        curr_user = list_of_users[-1].split("#")[0]
        if str(member) is not NAME_OF_THE_BOT and os.path.exists(curr_user) is not True:
            list_of_users.append(str(member))
            last_user = list_of_users[-1].split("#")[0]

            response = polly_client.synthesize_speech(
                Text=f"Welcome {last_user}",
                OutputFormat="mp3",
                VoiceId="Joanna"
            )

            with open(f"{last_user}", "wb") as f:
                f.write(response['AudioStream'].read())

            user_voice_channel = after.channel.id
            channel = client.get_channel(user_voice_channel)
            time.sleep(2)
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_LOCATION, source=f"./{last_user}"))
            audio = AudioSegment.from_file(f"{last_user}")

            duration = audio.duration_seconds+1
            time.sleep(float(duration))

            voice_client = channel.guild.voice_client
            await voice_client.disconnect()
            print('Bot joined the channel.')
        else:
            print("User voice file already exists")
            user_voice_channel = after.channel.id
            channel = client.get_channel(user_voice_channel)
            time.sleep(2)
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_LOCATION, source=f"./{curr_user}"))
            audio = AudioSegment.from_file(f"{curr_user}")

            duration = audio.duration_seconds+1
            time.sleep(float(duration))

            voice_client = channel.guild.voice_client
            await voice_client.disconnect()
            print('Bot joined the channel from else part')


async def search_google(query, num_results=1):
    loop = asyncio.get_event_loop()
    search_results = await loop.run_in_executor(None, lambda: search(query, num_results=num_results))
    return search_results


@client.tree.command(name="google")
async def google(ctx, *, query: str):
    author = ctx.user.mention
    result_message = f"Here are the links related to your question {author} !"

    search_results = await search_google(query, num_results=1)
    for j in search_results:
        result_message += f"\n:point_right: {j}"

    result_message += "\nHave any more questions:question:\nFeel free to ask again :smiley: !"

    # Acknowledge the interaction
    await ctx.response.defer()

    # Send the follow-up message
    await ctx.followup.send(content=result_message, ephemeral=False)

client.run(TOKEN)
