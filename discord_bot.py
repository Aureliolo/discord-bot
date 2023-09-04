import discord
from datetime import datetime, timedelta
import asyncio
import os

TOKEN = os.environ.get('TOKEN', '')  # Read from environment variable
CHANNELS_TIMESTAMPS = os.environ.get('CHANNELS_TIMESTAMPS', '')  # Read from environment variable

client = discord.Client()

async def update_channel():
    while True:
        now = datetime.utcnow()
        channel_data = CHANNELS_TIMESTAMPS.split(',')

        for data in channel_data:
            try:
                channel_id, target_hour, target_minute = map(int, data.split(':'))
            except ValueError:
                print(f"Skipping invalid data: {data}")
                continue

            target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
            if now > target_time:
                target_time += timedelta(days=1)

            time_left = target_time - now
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            channel = client.get_channel(channel_id)
            if channel:
                await channel.edit(name=f"Time left: {hours}h {minutes}m {seconds}s")

        await asyncio.sleep(1)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(update_channel())

client.run(TOKEN)
