import discord
from discord.ext import commands


class Bienvenida(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("⚙️  Cog 'Bienvenida' cargado.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel_id = 1382088209009479841  # <-- CAMBIÁ este ID si usás otro canal de bienvenida

        channel = member.guild.get_channel(channel_id)
        if not channel:
            print(f"❌ Canal con ID {channel_id} no encontrado.")
            return

        embed = self._crear_embed_bienvenida(member)

        try:
            message = await channel.send(embed=embed)
            await message.add_reaction("🦈")
        except discord.errors.Forbidden:
            print("❌ El bot no tiene permisos en el canal.")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

    def _crear_embed_bienvenida(self, member: discord.Member):
        gif_url = "https://media.discordapp.net/attachments/1381430087223611435/1383258340209201294/9556a4c877b7a222692baba7f7eadfd6.gif"

        info_channel = "<#1382087503825211432>"
        soporte_channel = "<#1382234783052206120>"
        presentate_channel = "<#1382160286491869317>"

        descripcion = (
            f"¡Bienvenido/a al servidor, {member.mention}!\n"
            f"Nos alegra un montón tenerte por acá. Esta es una comunidad con buena onda, ganas de compartir y pasarla bien.\n\n"
            f"📌 **Leé primero:** {info_channel} – Ahí vas a encontrar toda la info importante del servidor.\n"
            f"📨 **¿Tenés un problema?** Pasate por {soporte_channel} y te damos una mano.\n"
            f"🗣️ **Presentate en** {presentate_channel} – Queremos conocerte un poco más :)\n\n"
            f"<a:flechazul:1383221441574731878> ¡Esperamos que la pases genial con nosotros!"
        )

        embed = discord.Embed(
            title=f"💫 {member.display_name} acaba de aterrizar...",
            description=descripcion,
            color=0x3498db  # Azul moderno
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=gif_url)
        embed.set_footer(
            text=f"Miembro #{member.guild.member_count} • {member.guild.name}",
            icon_url=member.guild.icon.url if member.guild.icon else None)
        return embed


async def setup(bot: commands.Bot):
    await bot.add_cog(Bienvenida(bot))
