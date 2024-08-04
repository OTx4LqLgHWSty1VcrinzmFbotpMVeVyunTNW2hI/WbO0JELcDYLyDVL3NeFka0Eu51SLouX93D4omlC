#Show Hidden Files
#Go To .replit [hidden]
#disableGuessImports = true
#entrypoint = "main.py"
#modules = ["python-3.10"]
#disableGuessImports = true
#Go Tools > Dependencies > + Add new package > py-cord

import discord #upm package(py-cord)

import os


# debug_guilds must not be set if we want to set contexts and integration_types on commands
bot = discord.Bot()
bot.load_extension('commands')


@bot.slash_command(
    # Can only be used in private messages
    contexts={discord.InteractionContextType.private_channel},
    # Can only be used if the bot is installed to your user account,
    # if left blank it can only be used when added to guilds
    integration_types={discord.IntegrationType.user_install},
)
async def selamla(ctx: discord.ApplicationContext, user: discord.User):
    await ctx.respond(f"Nabıyon Kardeş. Wgleri Tarat Bakayım., {user}!")


@bot.slash_command(
    # This command can be used by guild members, but also by users anywhere if they install it
    integration_types={
        discord.IntegrationType.guild_install,
        discord.IntegrationType.user_install,
    },
)
async def merhaba_eren(ctx: discord.ApplicationContext):
    await ctx.respond("Sanada Merhaba. Wargods Tarat Hadi")


@bot.event
async def on_ready():
    
    #await bot.tree.sync()
    print(f'Bot {str(bot.user)} works')



bot.run(os.getenv("DISCORD_TOKEN"))
