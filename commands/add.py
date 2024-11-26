import hashlib
from discord.ext import commands
from database import Database

db = Database("servers.db")

@commands.command(name="add")
async def add_command(ctx, name, ip, ssh_user, ssh_password):
    """
    Adds a server to the database and deletes the user's message for security.
    """
    hashed_password = hashlib.sha256(ssh_password.encode()).hexdigest()

    if db.add_server(ctx.author.id, name, ip, ssh_user, hashed_password):
        await ctx.send(f"Server {name} added successfully!")
        
        # Delete the user's original message
        try:
            await ctx.message.delete()
            await ctx.send("Your message containing server details has been deleted for security.")
        except discord.errors.Forbidden:
            await ctx.send("I don't have permission to delete messages. Please delete your command manually.")
    else:
        await ctx.send("A server with this name already exists.")