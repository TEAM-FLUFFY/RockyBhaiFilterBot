import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR
from utils import temp

class Bot(Client):

    def __init__(self):
        super().__init__(
            session_name="AQCi9YBq_Mm0OEkdA59uIf_SJMvKgKRvfNOHkpe-HuBsVNpmNymNJXihHQx3ShI9Ajg5GQ8QaWnVSUsAswIBFzcnnoXynGYHuoCT4T6JJRR3oB6l0RW8boTdyXPF_ECsypVTBTHHGaYoco2YvT1E7kB8afbYtrzr1xBkVdoZkIXYZsHXea24MHHadzfRGMICaZCXtDkw7kZVhTRUK4gSGz0nTUfdaXWa_nsSb_Z3kGK65Qr37A1FO0qOyKd8oTisKsTU3FqGUBIMGDEgduaW_-lr7rQ1tMYXYzoQFAf1Kd4HmuK6aqCOUDUPaRmPwZDL9Grrrs23fCfAXCWy1zOFBz6_AAAAATU_rBwA",
            api_id="19143782",
            api_hash="43176648b57c393328f832939efb72da",
            bot_token="5195105310:AAGbfLtjvJybPv-THkNsViqkXRPYKpAy2rM"
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        logging.info(LOG_STR)

    async def stop(self, *args):
        await super().stop()
        logging.info("Restarting Ajax.")


app = Bot()
app.run()
