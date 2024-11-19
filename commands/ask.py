from discord.ext import commands

@commands.command(name="ask")
async def ask_command(ctx, *, question):
    answers = {
        "restart service": "To restart a service, use `systemctl restart <service>`.",
        "check disk space": "Use `df -h` to check disk space."
    }
    for key in answers:
        if key in question.lower():
            await ctx.send(answers[key])
            return
    await ctx.send("Sorry, I don't understand your question yet.")
