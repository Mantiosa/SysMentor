from discord.ext import commands
from nlp import TaskFinder

task_finder = TaskFinder("tasks.json")

@commands.command(name="ask")
async def ask_command(ctx, *, question):
    try:
        best_task = task_finder.find_best_match(question)
        
        if best_task:
            answer = best_task.get("answer", "No answer available.")
            await ctx.send(f"Question: {question}\nAnswer: {answer}")
        else:
            await ctx.send("I'm sorry, I couldn't understand your question.")
    except Exception as e:
        await ctx.send(f"An error occurred while processing your question: {e}")
