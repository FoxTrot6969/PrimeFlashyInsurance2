import discord
from discord.ext import commands
import random


class Despedidas(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.canal_despedida_id = 1383595116828295321

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        canal = member.guild.get_channel(self.canal_despedida_id)
        if not canal:
            print(
                f"❌ Canal de despedidas no encontrado ({self.canal_despedida_id})"
            )
            return

        embed = self._crear_embed_despedida(member)

        try:
            await canal.send(embed=embed)
        except discord.Forbidden:
            print(
                "❌ No tengo permisos para enviar mensajes en el canal de despedidas."
            )
        except Exception as e:
            print(f"⚠️ Error inesperado al enviar despedida: {e}")

    def _crear_embed_despedida(self, member: discord.Member):
        gif_url = "https://media.discordapp.net/attachments/1381430087223611435/1383258341391728670/b73310c83432f77e325c0281924739bf.gif?ex=684f74b8&is=684e2338&hm=cebb9500f293b45f16403edf65d67a784f30ef03c8850de19d31c31a0d49bf49&="

        titulos = [
            "💔 Otro ha caído...", "🚫 El exiliado del océano...",
            "🥀 Fin del viaje para uno más...",
            "🦈 Ya no nada entre nosotros...",
            "😔 Adiós, traidor del cardumen..."
            "🐟 Dormirás con los peces..."
        ]

        descripciones = [
            f"{member.mention} decidió abandonar el reinado de los tiburones. Se fue nadando hacia aguas desconocidas.",
            f"{member.mention} traicionó la causa tiburónica... y ahora nada solo en el océano.",
            f"{member.mention} se quitó las branquias y huyó del reino submarino. Inaceptable.",
            f"{member.mention} fue visto subiendo a tierra firme. Ha desertado del santuario marino.",
            f"{member.mention} eligió el camino de las sardinas. Ya no es bienvenido entre los tiburones."
        ]

        embed = discord.Embed(
            title=random.choice(titulos),
            description=random.choice(descripciones),
            color=0x3498db
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=gif_url)
        return embed


async def setup(bot: commands.Bot):
    await bot.add_cog(Despedidas(bot))
