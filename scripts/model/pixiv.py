import requests
from discord import Embed, ButtonStyle, Interaction
from discord.ui import Button, View
from .error import HTTPException
from .page import Paginator


class PixivModel:

    BASE_URL = "https://www.pixiv.net"
    PROXY = "pixiv.cat"
    RANDOM_URL = (
        "https://setu.yuban10703.xyz/setu?num=1&replace_url=https%3A%2F%2Fi.pixiv.cat"
    )

    def __init__(self) -> None:
        pass

    def image_proxy(self, url: str) -> str:
        return url.replace("pximg.net", "pixiv.cat")

    def embed(self, title: str = None, description: str = None) -> Embed:
        return Embed(title=title, description=description, color=0x0096FA)

    def request(self, endpoint: str) -> dict[str, str]:
        re = requests.get(self.BASE_URL + endpoint)
        if re.status_code == 200:
            return re.json()
        else:
            raise HTTPException(re.status_code)

    def image_embed(self, data: dict[str]) -> list[Embed, View]:
        if data["error"] == True:
            return [
                self.embed(title="작품을 찾을 수 없습니다.", description="ID를 다시 확인해주세요!"),
                None,
            ]
        embed = self.embed()
        embed.set_image(url=self.image_proxy(data["body"]["urls"]["original"]))
        view = View()
        view.add_item(
            Button(
                label="바로가기",
                style=ButtonStyle.url,
                url=self.BASE_URL + "/artworks/" + data["body"]["illustId"],
            )
        )
        return [embed, view]

    def random_embed(self) -> list[Embed, View]:
        re = requests.get(self.RANDOM_URL)
        if re.status_code == 200:
            data = re.json()
        else:
            raise HTTPException(re.status_code)
        embed = self.embed()
        embed.set_image(url=data["data"][0]["urls"]["original"])
        view = View()
        button = Button(label="새로고침", style=ButtonStyle.green)
        button.callback = self.random_callback
        view.add_item(
            Button(
                label="바로가기",
                style=ButtonStyle.url,
                url=self.BASE_URL
                + "/artworks/"
                + str(data["data"][0]["artwork"]["id"]),
            )
        )
        view.add_item(button)
        return [embed, view]

    async def random_callback(self, inter: Interaction) -> None:
        re = requests.get(self.RANDOM_URL)
        if re.status_code == 200:
            data = re.json()
        else:
            raise HTTPException(re.status_code)
        embed = self.embed()
        embed.set_image(url=data["data"][0]["urls"]["original"])
        await inter.response.edit_message(embed=embed)

    def r18_embed(self) -> list[Embed, View]:
        re = requests.get(self.RANDOM_URL + "&r18=1")
        if re.status_code == 200:
            data = re.json()
        else:
            raise HTTPException(re.status_code)
        embed = self.embed()
        embed.set_image(url=data["data"][0]["urls"]["original"])
        view = View()
        button = Button(label="새로고침", style=ButtonStyle.green)
        button.callback = self.r18_callback
        view.add_item(
            Button(
                label="바로가기",
                style=ButtonStyle.url,
                url=self.BASE_URL
                + "/artworks/"
                + str(data["data"][0]["artwork"]["id"]),
            )
        )
        view.add_item(button)
        return [embed, view]

    async def r18_callback(self, inter: Interaction) -> None:
        re = requests.get(self.RANDOM_URL + "&r18=1")
        if re.status_code == 200:
            data = re.json()
        else:
            raise HTTPException(re.status_code)
        embed = self.embed()
        embed.set_image(url=data["data"][0]["urls"]["original"])
        await inter.response.edit_message(embed=embed)

    def ranking_embed(self, id: int, data: dict[str]) -> list[Embed, View]:
        embeds = []
        urls = []
        page = 1
        len_page = len(data["contents"])
        for i in data["contents"]:
            embed = self.embed()
            embed.set_image(url=self.image_proxy(url=i["url"]))
            embed.set_footer(text=f"{page}/{len_page}")
            embeds.append(embed)
            urls.append(self.BASE_URL + "/artworks/" + str(i["illust_id"]))
            page += 1
        view = Paginator(executor_id=id, embeds=embeds, urls=urls)
        view.add_item(Button(label="바로가기", style=ButtonStyle.url, url=urls[0]))
        return [embeds[0], view]

    def tag_embed(self, tag: str, r18: bool):
        if r18:
            re = requests.get(self.RANDOM_URL + f"&tags={tag}&r18=1")
        else:
            re = requests.get(self.RANDOM_URL + f"&tags={tag}")
        if re.status_code == 200:
            data = re.json()
        else:
            raise HTTPException(re.status_code)
        embed = self.embed()
        embed.set_image(url=data["data"][0]["urls"]["original"])
        view = View()
        view.add_item(
            Button(
                label="바로가기",
                style=ButtonStyle.url,
                url=self.BASE_URL
                + "/artworks/"
                + str(data["data"][0]["artwork"]["id"]),
            )
        )
        return [embed, view]
