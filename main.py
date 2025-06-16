import discord
import os
import asyncio
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True  # Recomendado si luego vas a hacer comandos con texto
intents.members = True  # Necesario para detectar nuevos miembros

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user.name} ({bot.user.id})')
    print(f'✅ Conectado a {len(bot.guilds)} servidores.')

    try:
        synced = await bot.tree.sync()
        print(f"🔄 Se sincronizaron {len(synced)} comandos slash.")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="a los nuevos miembros"))


async def main():
    token = os.environ.get("DISCORD_TOKEN")
    if token is None:
        print("❌ ERROR: Token no configurado.")
        return

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

    keep_alive()
    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
