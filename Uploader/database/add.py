
        


from pyrogram import Client
from Uploader.database.access import client
from pyrogram.types import Message


async def add_user_to_database(bot: Client, update: Message):
    if not await client.is_user_exist(update.from_user.id):
           await client.add_user(update.from_user.id)
