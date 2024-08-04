#Show Hidden Files
#Go To .replit [hidden]
#disableGuessImports = true
#entrypoint = "main.py"
#modules = ["python-3.10"]
#disableGuessImports = true
#Go Tools > Dependencies > + Add new package > py-cord

import os
import discord #upm package(py-cord)
import asyncio
from dotenv import load_dotenv
from flask import Flask
import threading

# Çevresel değişkenleri yükle
load_dotenv()

# Flask uygulamasını oluştur
app = Flask(__name__)

# Discord botunu başlat
bot = discord.Bot()
bot.load_extension('commands')

# Discord bot komutları
@bot.slash_command(
    contexts={discord.InteractionContextType.private_channel},
    integration_types={discord.IntegrationType.user_install},
)
async def selamla(ctx: discord.ApplicationContext, user: discord.User):
    await ctx.respond(f"Nabıyon Kardeş. Wgni Tarat Bakayım., {user}!")

@bot.slash_command(
    integration_types={
        discord.IntegrationType.guild_install,
        discord.IntegrationType.user_install,
    },
)
async def merhaba_eren(ctx: discord.ApplicationContext):
    await ctx.respond("Sanada Merhaba. Wargods Tarat Hadi")

@bot.event
async def on_ready():
    print(f'Bot {str(bot.user)} works')

# Flask route tanımları
@app.route('/')
def index():
    return "Flask is working!"

# Flask'ı çalıştıran iş parçacığı
def run_flask():
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

# Discord botunu çalıştıran ana fonksiyon
def run_bot():
    asyncio.run(bot.start(os.getenv("DISCORD_TOKEN")))

if __name__ == "__main__":
    # Flask'ı ayrı bir iş parçacığında başlat
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Discord botunu başlat
    run_bot()
