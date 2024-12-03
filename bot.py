# Import required libraries
import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
from discord.ext.commands import Bot, CommandNotFound

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Set up intents
intents = discord.Intents.default()
intents.messages = True  # Allow the bot to process message events
intents.message_content = True  # Allow the bot to read message content (required for commands)

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Import active_sessions from commands/bash.py
from commands.bash import active_sessions

# Load commands from other files
from commands import ask, add, list, delete, bash, commands

bot.add_command(ask.ask_command)
bot.add_command(add.add_command)
bot.add_command(list.list_command)  # Fixed to import the correct 'list' command file
bot.add_command(delete.delete_command)
bot.add_command(bash.bash_command)
bot.add_command(bash.bashend_command)
bot.add_command(commands.commands_command)

# Handle invalid commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):  # Use CommandNotFound explicitly
        await ctx.send("Invalid command. To check available commands, use `!commands`.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")
# Event handler for interactive SSH sessions
@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author.bot:
        return

    # Check if the user has an active session
    session = active_sessions.get(message.author.id)
    if session and session['interactive']:
        # If the message starts with "!", treat it as a bot command
        if message.content.startswith("!"):
            await bot.process_commands(message)
        else:
            # Otherwise, treat the message as input for the SSH session
            ssh = session['ssh']
            try:
                stdin, stdout, stderr = ssh.exec_command(message.content)
                output = stdout.read().decode()
                if output.strip():
                    await message.channel.send(f"```\n{output.strip()}\n```")
                error = stderr.read().decode()
                if error.strip():
                    await message.channel.send(f"Error:\n```\n{error.strip()}\n```")
            except Exception as e:
                await message.channel.send(f"Error: {str(e)}")
        return  # Stop further processing of the message

    # Process other bot commands
    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
