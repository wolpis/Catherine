from discord import Intents


class CatherineConfig:

    token: str = (
        "MTA1MjI2NDAzMDEzMzMwNTM2NA.GofqON.uwfqpQBV3QoWU3wkd-iIw8Kya02oha762a-j9g"
    )
    guild_id: int = 1052256039455707176
    prefix: str = "?"
    public: bool = False

    def intents() -> Intents:
        intents = Intents.default()
        intents.message_content = True
        return intents
