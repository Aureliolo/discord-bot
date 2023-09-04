import discord
from datetime import datetime, timedelta
import asyncio
import os
from discord.errors import Forbidden

intents = discord.Intents.default()
client = discord.Client(intents=intents)

TOKEN = os.environ.get('TOKEN', '')  # Read from environment variable
CHANNELS_TIMESTAMPS = os.environ.get('CHANNELS_TIMESTAMPS', '')  # Read from environment variable

async def update_channel():
    while True:
        now = datetime.utcnow()
        channel_data = CHANNELS_TIMESTAMPS.split(',')

        for data in channel_data:
            try:
                channel_id, target_hour, target_minute, repeat_days = map(int, data.split(':'))
            except ValueError:
                print(f"Skipping invalid data: {data}")
                continue

            target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
            
            # Make sure target_time is in the future
            while target_time <= now:
                target_time += timedelta(days=repeat_days)

            time_left = target_time - now
            days, time_left_seconds = divmod(time_left.total_seconds(), 86400)  # 86400 seconds in a day
            hours, remainder = divmod(time_left_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            channel = client.get_channel(channel_id)
            
            if channel:
                permissions = channel.permissions_for(channel.guild.me)
                print(f"Permissions for bot in channel {channel.name}: {permissions}")
                
                if permissions.manage_channels:
                    try:
                        if days:
                            await channel.edit(name=f"Time left: {int(days)}d {int(hours)}h {int(minutes)}m")
                        else:
                            await channel.edit(name=f"Time left: {int(hours)}h {int(minutes)}m")
                    except Forbidden:
                        print(f"The bot does not have permission to edit the channel {channel.name}.")
                else:
                    print(f"The bot does not have 'manage_channels' permission in channel {channel.name}.")
                
        await asyncio.sleep(30)  # Sleep for 30 seconds

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(update_channel())

client.run(TOKEN)
