import discord
from discord.ext import commands
import asyncio
import random
import os
from dotenv import load_dotenv
from datetime import datetime

# Import our modules
from config import BOT_TOKEN, COMMAND_PREFIX, EMBED_COLORS, STATUS_MESSAGES
from scraper import QuestionScraper

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.none()  # Start with no intents
intents.message_content = True
intents.guilds = True
intents.messages = True
# Explicitly disable privileged intents
intents.members = False
intents.presences = False

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# Initialize the scraper
scraper = QuestionScraper()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    
    # Set bot status
    status = random.choice(STATUS_MESSAGES)
    await bot.change_presence(activity=discord.Game(name=status))

@bot.command(name='truth')
async def truth(ctx):
    """Get a random truth question"""
    async with ctx.typing():
        question, category = await scraper.get_random_question('truth')
        if question:
            embed = discord.Embed(
                title="🤔 Truth Question",
                description=question,
                color=EMBED_COLORS['truth']
            )
            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, I couldn't get a truth question right now. Try again later!")

@bot.command(name='dare')
async def dare(ctx):
    """Get a random dare question"""
    async with ctx.typing():
        question, category = await scraper.get_random_question('dare')
        if question:
            embed = discord.Embed(
                title="🎯 Dare Challenge",
                description=question,
                color=EMBED_COLORS['dare']
            )
            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, I couldn't get a dare question right now. Try again later!")

@bot.command(name='would_you_rather')
async def would_you_rather(ctx):
    """Get a random 'Would You Rather' question"""
    async with ctx.typing():
        question, category = await scraper.get_random_question('would_you_rather')
        if question:
            embed = discord.Embed(
                title="🤷 Would You Rather",
                description=question,
                color=EMBED_COLORS['would_you_rather']
            )
            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, I couldn't get a 'Would You Rather' question right now. Try again later!")

@bot.command(name='random')
async def random_question(ctx):
    """Get a random question of any type"""
    async with ctx.typing():
        question, category = await scraper.get_random_question()
        if question:
            # Create appropriate embed based on category
            if category == 'truth':
                title = "🤔 Random Truth Question"
                color = EMBED_COLORS['truth']
            elif category == 'dare':
                title = "🎯 Random Dare Challenge"
                color = EMBED_COLORS['dare']
            else:
                title = "🤷 Random Would You Rather"
                color = EMBED_COLORS['would_you_rather']
            
            embed = discord.Embed(
                title=title,
                description=question,
                color=color
            )
            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, I couldn't get a random question right now. Try again later!")

@bot.command(name='stats')
async def stats(ctx):
    """Show bot statistics"""
    cache_info = scraper.get_cache_info()
    
    embed = discord.Embed(
        title="📊 Bot Statistics",
        color=EMBED_COLORS['random']
    )
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Users", value=len(bot.users), inline=True)
    embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
    
    # Add cache information
    cache_text = ""
    for category, info in cache_info.items():
        status = "✅ Fresh" if info['is_fresh'] else "🔄 Stale"
        cache_text += f"{category.title()}: {info['question_count']} questions ({status})\n"
    
    if cache_text:
        embed.add_field(name="Cache Status", value=cache_text, inline=False)
    
    embed.set_footer(text="Truth and Truth Bot")
    await ctx.send(embed=embed)

@bot.command(name='refresh')
async def refresh_cache(ctx):
    """Refresh the question cache"""
    async with ctx.typing():
        await scraper.refresh_cache()
        embed = discord.Embed(
            title="🔄 Cache Refreshed",
            description="The question cache has been refreshed!",
            color=EMBED_COLORS['random']
        )
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

@bot.command(name='info')
async def info_command(ctx):
    """Show help information"""
    embed = discord.Embed(
        title="🎮 Truth and Truth Bot - Help",
        description="Get random questions to spice up your conversations!",
        color=EMBED_COLORS['random']
    )
    embed.add_field(
        name="Commands",
        value="""
        `!truth` - Get a random truth question
        `!dare` - Get a random dare challenge
        `!would_you_rather` - Get a random "Would You Rather" question
        `!random` - Get a random question of any type
        `!stats` - Show bot statistics
        `!refresh` - Refresh the question cache
        `!info` - Show this help message
        """,
        inline=False
    )
    embed.add_field(
        name="How it works",
        value="The bot scrapes questions from popular websites and generates random ones for you. If web scraping fails, it uses a curated list of fallback questions.",
        inline=False
    )
    embed.add_field(
        name="Features",
        value="• Web scraping from multiple sources\n• Intelligent caching system\n• Fallback questions if scraping fails\n• Beautiful Discord embeds\n• Multiple question categories",
        inline=False
    )
    embed.set_footer(text="Have fun and be respectful!")
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found! Use `!info` to see available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command!")
    else:
        await ctx.send(f"❌ An error occurred: {error}")

# Cleanup on bot shutdown
@bot.event
async def on_close():
    await scraper.close()

# Run the bot
if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Error: DISCORD_TOKEN not found in environment variables!")
        print("Please create a .env file with your Discord bot token.")
        print("See .env.example for reference.")
    else:
        bot.run(BOT_TOKEN) 