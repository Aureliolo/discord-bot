# Discord Countdown Bot

This is a Discord bot that updates multiple channel names to show a countdown to specified times in UTC, with optional repetition every X days.

## Usage

1. Set your Discord bot token and the channel IDs with target times as environment variables.
2. Build the Docker container.
3. Run the Docker container.

## Environment Variables

- `TOKEN`: Your Discord bot's token.
- `CHANNELS_TIMESTAMPS`: A comma-separated list of channel IDs with target times in UTC and repetition days. Format: `channel_id:hour:minute:repeat_days`.

Example: `1234567890:15:30:7,9876543210:20:45:1`

## Docker Commands

To build:
```bash
docker build -t discord_bot .
