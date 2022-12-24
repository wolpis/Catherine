import requests
from discord import Embed, ButtonStyle, Interaction
from discord.ui import Button, View
from .error import HTTPException
from .page import Paginator


class KonachanModel:

    BASE_URL = "https://konachan.net"

    def __init__(self) -> None:
        pass

    def embed(self, title: str = None, description: str = None) -> Embed:
        return Embed(title=title, description=description, color=0xFF007F)

    def request(self, endpoint: str):
        re = requests.get(self.BASE_URL + endpoint)
        if re.status_code == 200:
            return re.json()
        else:
            raise HTTPException(re.status_code)

    def post(self, id):
        data = self.request("/post.json")
        embeds = []
        urls = [self.BASE_URL + "/post/show/" + str(var["id"]) for var in data]
        index = 1
        for i in data:
            embed = self.embed()
            embed.set_image(url=i["jpeg_url"])
            embed.set_footer(text=f"{index}/{len(data)}")
            index += 1
            embeds.append(embed)
        view = Paginator(id, embeds, urls)
        view.add_item(Button(label="바로가기", style=ButtonStyle.url, url=urls[0]))
        return [embeds[0], view]

    def popular(self, id, mode):
        data = self.request(f"/post/{mode}.json")
        embeds = []
        urls = [self.BASE_URL + "/post/show/" + str(var["id"]) for var in data]
        index = 1
        for i in data:
            embed = self.embed()
            embed.set_image(url=i["jpeg_url"])
            embed.set_footer(text=f"{index}/{len(data)}")
            index += 1
            embeds.append(embed)
        view = Paginator(id, embeds, urls)
        view.add_item(Button(label="바로가기", style=ButtonStyle.url, url=urls[0]))
        return [embeds[0], view]
