import paramiko
from discord.ext import commands
from database import Database

db = Database("servers.db")

@commands.command(name="bash")
async def bash_command(ctx, server_name, *command):
    server = db.get_server(ctx.author.id, server_name)
    if not server:
        await ctx.send("Server not found.")
        return

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server[1], username=server[2], password=server[3])

        if command:
            stdin, stdout, stderr = ssh.exec_command(" ".join(command))
            output = stdout.read().decode()
            await ctx.send(f"Command output:\n```\n{output}\n```")
        else:
            await ctx.send("Interactive SSH is not yet implemented.")
        
        ssh.close()
    except Exception as e:
        await ctx.send(f"Error connecting to the server: {str(e)}")

@commands.command(name="bashend")
async def bashend_command(ctx):
    await ctx.send("Interactive SSH session closed.")
