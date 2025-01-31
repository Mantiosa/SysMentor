import hashlib
import discord
from discord.ext import commands
from database import db

@commands.command(name="add")
async def add_command(ctx, name, ip, ssh_user, ssh_password, port: int = 22):
    # Validations
    if not name.strip():
        await ctx.send("Error: Server name cannot be empty.")
        return
    if db.get_server(ctx.author.id, name):
        await ctx.send(f"Error: A server with the name '{name}' already exists.")
        return
    if not ip.strip() or len(ip.split(".")) != 4:  # Check for basic IPv4 format
        await ctx.send("Error: Invalid IP address format. Use IPv4 format (e.g., 192.168.1.1).")
        return
    if not ssh_user.strip():
        await ctx.send("Error: SSH username cannot be empty.")
        return
    if not ssh_password.strip():
        await ctx.send("Error: SSH password cannot be empty.")
        return

    
    if db.add_server(ctx.author.id, name, ip, ssh_user, ssh_password, port):
        await ctx.send(f"Server '{name}' added successfully on port {port}!")
        try:
            await ctx.message.delete()
            await ctx.send("Your message containing server details has been deleted for security.")
        except discord.errors.Forbidden:
            await ctx.send("I don't have permission to delete messages. Please delete your command manually.")
    else:
        await ctx.send("Error: Could not add the server. Please try again.")


