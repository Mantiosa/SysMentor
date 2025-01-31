from discord.ext import commands
from database import db

@commands.command(name="delete")
async def delete_command(ctx, name):
    if db.delete_server(ctx.author.id, name):
        await ctx.send(f"Server {name} deleted successfully.")
    else:
        await ctx.send(f"Server {name} not found.")