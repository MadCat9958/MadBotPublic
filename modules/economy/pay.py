import discord

from discord.ext import commands
from discord import app_commands
from discord import utils as dutils
from typing import Optional
from tools import models, db

class EconomyPay(commands.Cog):
    def __init__(self, bot: models.MadBot):
        self.bot = bot

    @app_commands.command(name="pay", description="Передать деньги человеку")
    @app_commands.describe(
        member="Участник, которому переводятся деньги",
        amount="Количество денег для перевода",
        comment="Комментарий к переводу"
    )
    @app_commands.rename(reason="comment")
    async def _pay(
        self, 
        interaction: discord.Interaction, 
        member: discord.Member,
        amount: app_commands.Range[int, 1, 2000000000],
        reason: Optional[str]
    ):
        if member.bot:
            embed = discord.Embed(
                title="Ошибка!",
                color=discord.Color.red(),
                description="Боту нельзя переводить деньги!"
            ).set_image(url="https://http.cat/400")
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        if member.id == interaction.user.id:
            embed = discord.Embed(
                title="Ошибка!",
                color=discord.Color.red(),
                description="Нельзя переводить деньги самому себе!"
            ).set_image("https://http.cat/400")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        user = db.get_guild_user(
            interaction.guild.id, 
            interaction.user.id
        ) or models.GuildUser(
            interaction.guild.id,
            interaction.user.id,
            0, 0, 0, []    
        )
        if (user.balance - amount) < 0:
            embed = discord.Embed(
                title="Ошибка!",
                color=discord.Color.red(),
                description="Недостаточно средств для перевода!"
            ).add_field(
                name="Ваш баланс:",
                value=f"{user.balance:,}"
            ).add_field(
                name="Необходимо для перевода:",
                value=f"{amount:,}"
            ).set_image(url="https://http.cat/400")
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        db.update_money(
            models.TransferAction(
                interaction.guild.id,
                interaction.user.id,
                member.id,
                reason=reason,
                amount=amount
            )
        )
        
        command = await self.bot.tree.fetch_commands()
        command = dutils.get(command, name=interaction.command.name)

        embed = discord.Embed(
            title="Перевод денег",
            color=discord.Color.orange(),
            description="Успешно совершён перевод денег другому пользователю. Вот Ваш чек.\n"
            f"Чтобы посмотреть свой баланс, воспользуйтесь командой {command.mention}."
        ).add_field(
            name="Отправитель",
            value=f"{interaction.user.mention} ({dutils.escape_markdown(str(interaction.user))})"
        ).add_field(
            name="Получатель",
            value=f"{member.mention} ({dutils.escape_markdown(str(member))})"
        ).add_field(
            name="Сумма",
            value=f"{amount:,}"
        ).set_image(
            url="https://http.cat/200"
        )
        await interaction.response.send_message(embed=embed, content=member.mention)

async def setup(bot: models.MadBot):
    await bot.add_cog(EconomyPay(bot))
