import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
from discord.ext.commands import Bot, CommandNotFound

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.messages = True  # Allow the bot to process message events
intents.message_content = True  # Allow the bot to read message content (required for commands)

bot = commands.Bot(command_prefix="!", intents=intents)

from commands.bash import active_sessions

from commands import ask, add, list, delete, bash, commands
bot.add_command(ask.ask_command)
bot.add_command(add.add_command)
bot.add_command(list.list_command) 
bot.add_command(delete.delete_command)
bot.add_command(bash.bash_command)
bot.add_command(bash.bashend_command)
bot.add_command(commands.commands_command)

# Handle invalid commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound): 
        await ctx.send("Invalid command. To check available commands, use `!commands`.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")
# Event handler for interactive SSH sessions
@bot.event
async def on_message(message):
    # Ignore bot msg
    if message.author.bot:
        return

    # Check if the user has an active session
    session = active_sessions.get(message.author.id)
    if session and session['interactive']:
        if message.content.startswith("!"):
            await bot.process_commands(message)
        else:
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
        return 

    await bot.process_commands(message)

bot.run(TOKEN)
