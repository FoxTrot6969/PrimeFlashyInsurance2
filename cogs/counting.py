import discord
from discord.ext import commands
import asyncio


class Counting(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.counting_channel_id = 1382238417546641408

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.id != self.counting_channel_id:
            return

        content = message.content.strip()

        # Verifica que el mensaje sea solo un número positivo
        if not content.isdigit():
            await message.delete()
            await self._advertir(message.channel, message.author,
                                 "⛔ Solo se permiten números positivos.")
            return

        current_number = int(content)

        # Busca el último número válido anterior
        async for msg in message.channel.history(limit=100,
                                                 before=message.created_at):
            if msg.author.bot:
                continue
            if msg.content.strip().isdigit():
                last_number = int(msg.content.strip())
                last_user_id = msg.author.id
                break
        else:
            # No hay mensajes válidos, solo se permite empezar con 1
            if current_number != 1:
                await message.delete()
                await self._advertir(message.channel, message.author,
                                     "⚠️ El conteo debe comenzar en 1.")
            else:
                await message.add_reaction("🐳")
            return

        # Reglas
        if current_number != last_number + 1:
            await message.delete()
            await self._advertir(
                message.channel, message.author,
                f"❌ El número correcto era **{last_number + 1}**.")
            return

        if message.author.id == last_user_id:
            await message.delete()
            await self._advertir(
                message.channel, message.author,
                "⚠️ Esperá tu turno. No podés contar dos veces seguidas.")
            return

        # Mensaje válido: agrega reacción 🐳
        await message.add_reaction("🐳")

    async def _advertir(self, channel: discord.TextChannel, user: discord.User,
                        mensaje: str):
        advertencia = await channel.send(f"{user.mention} {mensaje}")
        await asyncio.sleep(3)
        try:
            await advertencia.delete()
        except discord.NotFound:
            pass


async def setup(bot):
    await bot.add_cog(Counting(bot))
