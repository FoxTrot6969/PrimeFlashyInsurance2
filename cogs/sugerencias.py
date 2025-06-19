import discord
from discord.ext import commands

SUGERENCIAS_CHANNEL_ID = 1382213352964755556


class SugerenciaModal(discord.ui.Modal, title="Enviar una sugerencia"):

    sugerencia = discord.ui.TextInput(
        label="¿Cuál es tu sugerencia?",
        style=discord.TextStyle.paragraph,
        placeholder="Escribí tu idea o mejora...",
        required=True,
        max_length=1000
    )

    def __init__(self, autor: discord.User, canal_destino: discord.TextChannel):
        super().__init__()
        self.autor = autor
        self.canal_destino = canal_destino

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📨 Nueva sugerencia",
            description=self.sugerencia.value,
            color=0x3498db
        )
        embed.set_author(name=str(self.autor), icon_url=self.autor.display_avatar.url)
        embed.set_footer(text=f"Usuario ID: {self.autor.id}")

        try:
            mensaje = await self.canal_destino.send(embed=embed)
            await mensaje.add_reaction("✅")
            await mensaje.add_reaction("❌")
            await interaction.response.send_message("✅ ¡Sugerencia enviada!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class Sugerencias(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("⚙️  Cog 'Sugerencias' cargado.")

        @bot.tree.command(name="sugerir", description="Enviá una sugerencia para el servidor.")
        async def sugerir(interaction: discord.Interaction):
            canal = interaction.guild.get_channel(SUGERENCIAS_CHANNEL_ID)
            if not canal:
                await interaction.response.send_message("❌ No se encontró el canal de sugerencias.", ephemeral=True)
                return

            modal = SugerenciaModal(autor=interaction.user, canal_destino=canal)
            await interaction.response.send_modal(modal)


async def setup(bot):
    await bot.add_cog(Sugerencias(bot))
