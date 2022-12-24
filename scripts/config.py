from discord import Intents


class CatherineConfig:

    token: str = (
        "MTA1MjI2NDAzMDEzMzMwNTM2NA.GYRH6M.bBNvLoKbjsL2BLWcyJ6Q-D8NI6DO7tNe9gBd84"
    )
    guild_id: int = 1052256039455707176
    prefix: str = "?"
    public: bool = True

    def intents() -> Intents:
        intents = Intents.default()
        intents.message_content = True
        return intents
