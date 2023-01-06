import httpx
from discord import Embed, ButtonStyle, Interaction
from discord.ui import Button, View, button
from typing import Optional
from .error import HTTPException
from .page import Paginator
import json


class ZeroChanModel:

    BASE_URL = "https://www.zerochan.net"

    def __init__(self) -> None:
        pass

    def embed(self, title: str = None, description: str = None) -> Embed:
        return Embed(title=title, description=description, color=0xABF200)

    async def request(self, endpoint: str):
        async with httpx.AsyncClient() as requests:
            re = requests.get(self.BASE_URL + endpoint)
        if re.status_code == 200:
            re = re.text.replace("\\", "")
            return json.loads(re)
        else:
            raise HTTPException(re.status_code)

    def s_id(self, id: int):
        data = self.request("/?s=id&json=1")
        ids = [str(var["id"]) for var in data["items"]]
        urls = []
        for i in ids:
            urls.append(self.BASE_URL + "/" + i)
        view = Paginator(id, ids, urls)
        view.add_item(Button(label="바로가기", style=ButtonStyle.url, url=urls[0]))
        embed: Embed = self.embed()
        data = self.request("/" + ids[0] + "?json=1")
        embed.set_image(url=data["large"])
        embed.set_footer(text=f"1/{len(ids)}")
        return [embed, view]

    def f_id(self, id: int):
        data = self.request("/?s=fav&json=1")
        ids = [str(var["id"]) for var in data["items"]]
        urls = []
        for i in ids:
            urls.append(self.BASE_URL + "/" + i)
        view = Paginator(id, ids, urls)
        view.add_item(Button(label="바로가기", style=ButtonStyle.url, url=urls[0]))
        embed: Embed = self.embed()
        data = self.request("/" + ids[0] + "?json=1")
        embed.set_image(url=data["large"])
        embed.set_footer(text=f"1/{len(ids)}")
        return [embed, view]


class Paginator(View, ZeroChanModel):
    def __init__(
        self,
        executor_id: int,
        ids: list[str],
        urls: list[View],
        index: int = 0,
        timeout: Optional[float] = 60,
    ):
        super().__init__(timeout=timeout)
        self.ids = ids
        self.executor_id = executor_id
        self.index = index
        self.urls = urls

    @property
    def total(self):
        return len(self.ids)

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
        view = Paginator(executor_id=self.executor_id, ids=self.ids, urls=self.urls)
        view.add_item(
            Button(label="바로가기", style=ButtonStyle.url, url=self.urls[self.index])
        )
        data = self.request("/" + self.ids[self.index] + "?json=1")
        embed: Embed = self.embed()
        embed.set_image(url=data["large"])
        embed.set_footer(text=f"{self.index + 1}/{len(self.ids)}")
        await interaction.response.edit_message(embed=embed, view=view)

    @button(label="다음", style=ButtonStyle.primary, emoji="▶️")
    async def next_page(self, interaction: Interaction, _):
        self.index += 1

        if self.index >= self.total:
            self.index = 0
        view = Paginator(
            executor_id=self.executor_id,
            ids=self.ids,
            urls=self.urls,
            index=self.index,
        )
        view.add_item(
            Button(label="바로가기", style=ButtonStyle.url, url=self.urls[self.index])
        )
        data = self.request("/" + self.ids[self.index] + "?json=1")
        embed: Embed = self.embed()
        embed.set_image(url=data["large"])
        embed.set_footer(text=f"{self.index + 1}/{len(self.ids)}")
        await interaction.response.edit_message(embed=embed, view=view)

    @button(label="닫기", style=ButtonStyle.danger, emoji="❌")
    async def close(self, interaction: Interaction, _):
        if message := interaction.message:
            self.stop()
            await message.delete()
