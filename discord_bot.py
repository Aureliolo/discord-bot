import discord
from datetime import datetime, timedelta
import asyncio
import os

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
            
            delta_days = (now - target_time).days
            if delta_days >= 0:
                cycles_passed = delta_days // repeat_days
                next_cycle = cycles_passed + 1
                days_to_add = next_cycle * repeat_days
                target_time += timedelta(days=days_to_add)

            time_left = target_time - now
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            channel = client.get_channel(channel_id)
            if channel:
                await channel.edit(name=f"Time left: {hours}h {minutes}m {seconds}s")

        await asyncio.sleep(30)  # Sleep for 30 seconds

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(update_channel())

client.run(TOKEN)
