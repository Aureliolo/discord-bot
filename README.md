# Discord Countdown Bot

This is a Discord bot that updates multiple channel names to display a countdown to specified times in UTC. You can set it to update daily or weekly at specific times.

## Usage

1. Set your Discord bot token and the channel IDs with target times as environment variables.
2. Build the Docker container.
3. Run the Docker container.

## Environment Variables

- `TOKEN`: Your Discord bot's token.
- `CHANNELS_TIMESTAMPS`: A comma-separated list of channel IDs with target times in UTC and repetition intervals. Format: `channel_id:weekday:hour:minute:repeat_interval`.

  - `weekday`: Day of the week (0 for Monday, 6 for Sunday).
  - `hour`: Hour of the day (0-23) in UTC.
  - `minute`: Minute of the hour (0-59).
  - `repeat_interval`: Either 'daily' or 'weekly'.

Example: `1234567890:0:15:30:daily,9876543210:0:20:45:weekly`

## Docker Commands

To build the Docker image:
```bash
docker build -t discord_bot .
docker run -e TOKEN="your_bot_token" -e CHANNELS_TIMESTAMPS="1234567890:0:15:30:daily,9876543210:0:20:45:weekly" discord_bot
```
Please replace `"your_bot_token"` and the example `CHANNELS_TIMESTAMPS` value with your actual Discord bot token and desired channel settings.