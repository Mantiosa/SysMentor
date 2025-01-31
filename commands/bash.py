from discord.ext import commands
import paramiko
from database import db

active_sessions = {}

@commands.command(name="bash")
async def bash_command(ctx, server_name, *command):
    server = db.get_server(ctx.author.id, server_name)
    if not server:
        await ctx.send("Server not found.")
        return

    try:
        if not command:
            # Open an interactive SSH session
            if ctx.author.id in active_sessions:
                await ctx.send("You already have an active session. Use !bashend to close it first.")
                return
            
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(server[1], username=server[2], password=server[3])
            active_sessions[ctx.author.id] = {'ssh': ssh, 'interactive': True}
            await ctx.send(f"Interactive SSH session opened with {server_name}. Send commands directly in the chat.")
        else:
            # Execute a single command if no interactive session is active
            if ctx.author.id not in active_sessions:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(server[1], username=server[2], password=server[3])
                stdin, stdout, stderr = ssh.exec_command(" ".join(command))
                output = stdout.read().decode() + stderr.read().decode() 
                ssh.close()
                await ctx.send(f"Command output:\n```\n{output}\n```")
            else:
                # Execute the command in the active session
                ssh = active_sessions[ctx.author.id]['ssh']
                stdin, stdout, stderr = ssh.exec_command(" ".join(command))
                output = stdout.read().decode() + stderr.read().decode()
                await ctx.send(f"Command output:\n```\n{output}\n```")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@commands.command(name="bashend")
async def bashend_command(ctx):
    session = active_sessions.pop(ctx.author.id, None)
    if session:
        session['ssh'].close()
        await ctx.send("SSH session closed.")
    else:
        await ctx.send("No active SSH session to close.")
