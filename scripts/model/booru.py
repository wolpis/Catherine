import httpx
from discord import Embed, ButtonStyle, Interaction
from discord.ui import Button, View
from .error import HTTPException
from .page import Paginator


class BooruModel:
    BASE_URL = "https://safebooru.org"
    IMAGE_URL = BASE_URL + "/images/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    def __init__(self) -> None:
        pass

    def embed(self, title: str = None, description: str = None) -> Embed:
        return Embed(title=title, description=description, color=0xFFE08C)

    async def request(self, endpoint: str):
        async with httpx.AsyncClient() as requests:
            re = await requests.get(self.BASE_URL + endpoint, headers=self.headers)
        if re.status_code == 200:
            return re.json()
        else:
            raise HTTPException(re.status_code)

    async def post(self, id: int):
        data: list[str] = await self.request("/index.php?page=dapi&s=post&q=index&json=1")
        embeds = []
        urls = []
        image = [val for val in data if val["image"].endswith(".gif") == False]
        total = len(image)
        index = 1
        for image in data:
            embed = self.embed()
            embed.set_image(
                url=self.IMAGE_URL + image["directory"] + "/" + image["image"]
            )
            embed.set_footer(text=f"{index}/{total}")
            embeds.append(embed)
            urls.append(
                self.BASE_URL + "/index.php?page=post&s=view&id=" + str(image["id"])
            )
            index += 1
        view = Paginator(id, embeds, urls)
        view.add_item(Button(label="바로가기", style=ButtonStyle.url, url=urls[0]))
        return [embeds[0], view]

    async def search(self, id: int, tag: str):
        try:
            data: list[str] = await self.request(
                "/index.php?page=dapi&s=post&q=index&json=1&tags=" + tag
            )
            embeds = []
            urls = []
            image = [val for val in data if val["image"].endswith(".gif") == False]
            total = len(image)
            index = 1
            for image in data:
                embed = self.embed()
                embed.set_image(
                    url=self.IMAGE_URL + image["directory"] + "/" + image["image"]
                )
                embed.set_footer(text=f"{index}/{total}")
                embeds.append(embed)
                urls.append(
                    self.BASE_URL + "/index.php?page=post&s=view&id=" + str(image["id"])
                )
                index += 1
            view = Paginator(id, embeds, urls)
            view.add_item(Button(label="바로가기", style=ButtonStyle.url, url=urls[0]))
            return [embeds[0], view]
        except Exception as e:
            print(e)
            embed = self.embed(title="검색어를 찾을 수 없습니다!")
            return [embed, None]
