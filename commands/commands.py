from discord.ext import commands

@commands.command(name="commands")
async def commands_command(ctx):
    command_list = [
        ("!add <name> <ip> <ssh_user> <ssh_password>", "Adds a new server with the given details."),
        ("!delete <name>", "Removes a server from your list by name."),
        ("!list", "Lists all servers you have added."),
        ("!bash <name> <command>", "Executes a single command on the specified server."),
        ("!bash <name>", "Starts an SSH session with the specified server."),
        ("!bashend", "Closes the current SSH session."),
        ("!ask <query>", "Asks the bot a question about Linux administration."),
        ("!commands", "Lists all available commands and what they do."),
    ]

    response = "**Available Commands:**\n"
    response += "\n".join([f"`{cmd}` - {desc}" for cmd, desc in command_list])

    await ctx.send(response)
