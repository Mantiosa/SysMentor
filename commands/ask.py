from discord.ext import commands
from nlp import TaskFinder

task_finder = TaskFinder("tasks.json")

@commands.command(name="ask")
async def ask_command(ctx, *, question):
    """Finds the best match for the user's question and provides a solution."""
    try:
        match = task_finder.find_best_match(question)
        await ctx.send(f"**Question:** {match['question']}\n**Answer:** {match['answer']}")
    except Exception as e:
        await ctx.send(f"Sorry, I couldn't find an answer. Error: {str(e)}")
