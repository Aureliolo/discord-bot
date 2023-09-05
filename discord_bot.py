import discord
from datetime import datetime, timedelta
import asyncio
import os
from discord.errors import Forbidden
import sys

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
                parts = data.split(':')
                channel_id = int(parts[0])
                repeat_interval = parts[-1]  # Last item is the interval

                if repeat_interval == "daily":
                    target_hour = int(parts[1])
                    target_minute = int(parts[2])
                elif repeat_interval == "weekly":
                    weekday = int(parts[1])
                    target_hour = int(parts[2])
                    target_minute = int(parts[3])
                else:
                    raise ValueError("Invalid interval")
            except ValueError as e:
                print(f"Skipping invalid data: {data}. Error: {str(e)}")
                continue

            target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
            print(f"Initial target time: {target_time}")

            # Adjust for the correct weekday ONLY if repeat_interval is "weekly"
            if repeat_interval == "weekly":
                days_until_target = (weekday - now.weekday() + 7) % 7
                target_time += timedelta(days=days_until_target)

            # Make sure target_time is in the future
            while target_time <= now:
                if repeat_interval == "daily":
                    target_time += timedelta(days=1)
                elif repeat_interval == "weekly":
                    target_time += timedelta(days=7)

            time_left = target_time - now
            days, time_left_seconds = divmod(time_left.total_seconds(), 86400)  # 86400 seconds in a day
            hours, remainder = divmod(time_left_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            channel = client.get_channel(channel_id)
            if channel:
                permissions = channel.permissions_for(channel.guild.me)
                if permissions.manage_channels:
                    try:
                        if days:
                            await channel.edit(name=f"Time left: {int(days)}d {int(hours)}h {int(minutes)}m")
                        else:
                            await channel.edit(name=f"Time left: {int(hours)}h {int(minutes)}m")
                    except Exception as e:
                        print(f"An error occurred while trying to edit the channel {channel.name}. Error details: {str(e)}")
                else:
                    print(f"The bot does not have 'manage_channels' permission in channel {channel.name}.")

        sys.stdout.flush()  # Flush the stdout buffer explicitly
        await asyncio.sleep(305)  # Sleep for 305 seconds, rate limited to every 305

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(update_channel())

client.run(TOKEN)