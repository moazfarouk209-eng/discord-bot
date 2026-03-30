import discord
import random
import os
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread

# ===== SETTINGS =====
TOKEN = os.getenv("TOKEN")  
CHANNEL_ID = 1488178204358344774  
GUILD_ID = 1487738172464037978  

tasks_list = [
    "100+ من كل موارد الزبالة",
  "100+من كل موارد الازاز",
  "100+ من كل موارد النفط",
  "taxi minimum 5k",
]

# ===== BOT SETUP =====
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== FLASK SERVER TO KEEP BOT ALIVE =====
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ===== ON READY =====
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    auto_assign.start()

# ===== AUTO ASSIGN TASK LOOP =====
@tasks.loop(minutes=5)
async def auto_assign():
    guild = bot.get_guild(GUILD_ID)
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found")
        return

    members = [m for m in guild.members if not m.bot]
    if not members:
        return

    member = random.choice(members)
    task = random.choice(tasks_list)
    await channel.send(f"{member.mention}, your task is: **{task}**")

# ===== MANUAL COMMAND =====
@bot.command()
async def assign(ctx):
    members = [m for m in ctx.guild.members if not m.bot]
    if not members:
        await ctx.send("No players found")
        return

    member = random.choice(members)
    task = random.choice(tasks_list)
    await ctx.send(f"{member.mention}, your task is: **{task}**")

# ===== START EVERYTHING =====
keep_alive()
bot.run(TOKEN)