from discord import Intents


class CatherineConfig:

    token: str = (
        "token"
    )
    guild_id: int = 1052256039455707176
    prefix: str = "?"
    public: bool = True

    def intents() -> Intents:
        intents = Intents.default()
        intents.message_content = True
        return intents
