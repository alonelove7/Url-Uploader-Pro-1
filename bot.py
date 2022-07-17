
import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import os
import pytz
import datetime
from Uploader.config import Config
from pyrogram import Client
from Uploader.database.database import Database


def main():

    Renamer = Client("DKBOTZ",
                 bot_token=Config.BOT_TOKEN,
                 api_id=Config.API_ID,
                 api_hash=Config.API_HASH,
                 plugins=dict(root="Uploader/plugins"),
                 workers=16)

    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

    time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    Config.RESTART_TIME.append(time)

    Renamer.db = Database(Config.DATABASE_URL, Config.BOT_USERNAME)
    Renamer.broadcast_ids = {}
    Renamer.run()


if __name__ == "__main__":
    main()
