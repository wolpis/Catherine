from typing import Optional

from discord import ButtonStyle, Embed, Interaction
from discord.ui import Button, View, button


class Paginator(View):
    def __init__(
        self,
        executor_id: int,
        embeds: list[Embed],
        urls: list[View],
        index: int = 0,
        timeout: Optional[float] = 60,
    ):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.executor_id = executor_id
        self.index = index
        self.urls = urls

    @property
    def total(self):
        return len(self.embeds)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if user := interaction.user:
            if user.id == self.executor_id:
                return True

            await interaction.response.send_message(
                "명령어 실행자만 상호작용이 가능합니다.", ephemeral=True
            )

        return False

    @button(label="이전", style=ButtonStyle.primary, emoji="◀")
    async def prev_page(self, interaction: Interaction, _):
        self.index -= 1
        if self.index < 0:
            self.index = self.total - 1
        view = Paginator(
            executor_id=self.executor_id, embeds=self.embeds, urls=self.urls
        )
        view.add_item(
            Button(label="바로가기", style=ButtonStyle.url, url=self.urls[self.index])
        )
        await interaction.response.edit_message(
            embed=self.embeds[self.index], view=view
        )

    @button(label="다음", style=ButtonStyle.primary, emoji="▶️")
    async def next_page(self, interaction: Interaction, _):
        self.index += 1

        if self.index >= self.total:
            self.index = 0
        view = Paginator(
            executor_id=self.executor_id,
            embeds=self.embeds,
            urls=self.urls,
            index=self.index,
        )
        view.add_item(
            Button(label="바로가기", style=ButtonStyle.url, url=self.urls[self.index])
        )
        await interaction.response.edit_message(
            embed=self.embeds[self.index], view=view
        )

    @button(label="닫기", style=ButtonStyle.danger, emoji="❌")
    async def close(self, interaction: Interaction, _):
        if message := interaction.message:
            self.stop()
            await message.delete()
