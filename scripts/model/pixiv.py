import requests
from discord import Embed, ButtonStyle
from discord.ui import Button, View
from .error import HTTPException


class PixivModel:

    BASE_URL = "https://www.pixiv.net"
    PROXY = "pixiv.cat"

    def __init__(self) -> None:
        pass

    def image_proxy(self, url: str):
        return url.replace("pximg.net", "pixiv.cat")

    def embed(self, title: str = "", description: str = "") -> Embed:
        return Embed(title=title, description=description, color=0x0096FA)

    def request(self, endpoint: str):
        re = requests.get(self.BASE_URL + endpoint)
        if re.status_code == 200:
            return re.json()
        else:
            raise HTTPException(re.status_code)

    def image_embed(self, data: dict[str]):
        if data["error"] == True:
            return [
                self.embed(title="작품을 찾을 수 없습니다.", description="ID를 다시 확인해주세요!"),
                None,
            ]
        embed = self.embed()
        embed.set_image(url=self.image_proxy(data["body"]["urls"]["regular"]))
        view = View()
        view.add_item(
            Button(
                label="바로가기",
                style=ButtonStyle.url,
                url=self.BASE_URL + "/artworks/" + data["body"]["illustId"],
            )
        )
        return [embed, view]

    def random_embed(self, data: dict[str]):
        pass

    def ranking_embed(self, data: dict[str]):
        pass

    def tag_embed(self, data: dict[str]):
        pass
