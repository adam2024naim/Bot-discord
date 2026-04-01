import discord
from discord.ext import commands
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import io

# Database setup
conn = sqlite3.connect('xp_system.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, xp INTEGER DEFAULT 0)''')
conn.commit()

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# XP System
def add_xp(user_id, amount):
    c.execute('INSERT OR IGNORE INTO users (id, xp) VALUES (?, ?)', (user_id, 0))
    c.execute('UPDATE users SET xp = xp + ? WHERE id = ?', (amount, user_id))
    conn.commit()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    add_xp(message.author.id, 1)  # Award XP for each message
    await bot.process_commands(message)

# Image Generation Example
@bot.command(name='generate_image')
async def generate_image(ctx):
    image = Image.new('RGB', (100, 100), color = 'blue')
    d = ImageDraw.Draw(image)
    d.text((10,10), "Hello", fill=(255,255,0))

    byte_arr = io.BytesIO()
    image.save(byte_arr, format='PNG')
    byte_arr.seek(0)

    await ctx.send(file=discord.File(byte_arr, 'image.png'))

# Slash command example
@bot.slash_command(name='xp', description='Check your XP points')
async def xp(ctx):
    c.execute('SELECT xp FROM users WHERE id = ?', (ctx.user.id,))
    xp_points = c.fetchone()
    await ctx.response.send_message(f'You have {xp_points[0] if xp_points else 0} XP points.')

# Run the bot
bot.run('YOUR_TOKEN_HERE')
