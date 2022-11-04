import asyncio
import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from izzymusik import LOGGER, app, userbot
from izzymusik.core.call import Anon
from izzymusik.plugins import ALL_MODULES
from izzymusik.utils.database import get_banned_users, get_gbanned

loop = asyncio.get_event_loop()


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("izzymusik").error(
            "no string detected..."
        )
        return
    if (
        not config.SPOTIFY_CLIENT_ID
        and not config.SPOTIFY_CLIENT_SECRET
    ):
        LOGGER("izzymusik").warning(
            "no spotify client, unnable to play from spotify."
        )
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("izzymusik.plugins" + all_module)
    LOGGER("izzymusik.plugins").info(
        "Necessary Modules Imported Successfully."
    )
    await userbot.start()
    await Anon.start()
    try:
        await Anon.stream_call(
            "https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4"
        )
    except NoActiveGroupCall:
        LOGGER("izzymusik").error(
            "[ERROR] - \n\nno active voice call, firstly open telegram and turn on voice chat in Logger Group."
        )
        sys.exit()
    except:
        pass
    await Anon.decorators()
    LOGGER("izzymusik").info("Music Bot Started Successfully,")
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("izzymusik").info("Stopping Music Bot")
