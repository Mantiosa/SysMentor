import hashlib
from discord.ext import commands
from database import Database

db = Database("servers.db")

@commands.command(name="add")
async def add_command(ctx, name, ip, ssh_user, ssh_password):
    hashed_password = hashlib.sha256(ssh_password.encode()).hexdigest()
    if db.add_server(ctx.author.id, name, ip, ssh_user, hashed_password):
        await ctx.send(f"Server {name} added successfully!")
    else:
        await ctx.send("Server already exists.")
