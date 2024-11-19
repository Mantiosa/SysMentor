# Import required libraries
import os
from dotenv import load_dotenv
from discord.ext import commands
import discord

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Set up intents
intents = discord.Intents.default()
intents.messages = True  # Allow the bot to process message events
intents.message_content = True  # Allow the bot to read message content (required for commands)

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Example command: Ping
@bot.command()
async def ping(ctx):
    """Replies with 'Pong!' when you type !ping."""
    await ctx.send("Pong!")

# Example command: Hello
@bot.command()
async def hello(ctx):
    """Replies with 'Hello, <username>!'."""
    await ctx.send(f"Hello, {ctx.author.name}!")

# Add your other commands here
# Load commands from other files
from commands import ask, add, list, delete, bash

bot.add_command(ask.ask_command)
bot.add_command(add.add_command)
bot.add_command(list.list_command)  # Fixed to import the correct 'list' command file
bot.add_command(delete.delete_command)
bot.add_command(bash.bash_command)
bot.add_command(bash.bashend_command)

# Run the bot
bot.run(TOKEN)
