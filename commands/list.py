from discord.ext import commands
from database import db

@commands.command(name="list")
async def list_command(ctx):
    servers = db.list_servers(ctx.author.id)
    if not servers:
        await ctx.send("You have no servers added.")
    else:
        await ctx.send("\n".join(f"{s[0]} - {s[1]}" for s in servers))
