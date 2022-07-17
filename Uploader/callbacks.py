import os
from Uploader.functions.display_progress import progress_for_pyrogram, humanbytes
from Uploader.config import Config
from Uploader.dl_button import ddl_call_back
from Uploader.button import youtube_dl_call_back

from Uploader.script import Translation, TEXT
from pyrogram import Client, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from Uploader.commands import *
from Uploader.thumbnail import delete_thumbnail











@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m):
    await m.answer()
    await help(c, m, True)


@Client.on_callback_query(filters.regex('^donate$'))
async def donate(c, m):
    button = [[
        InlineKeyboardButton('🏕️ Home', callback_data='back'),
        InlineKeyboardButton('📘 About', callback_data='about')
        ],[
        InlineKeyboardButton('❌ Close', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    await m.answer()
    await m.message.edit(
        text=TEXT.DONATE_USER.format(m.from_user.first_name),
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


@Client.on_callback_query(filters.regex('^close$'))
async def close_cb(c, m):
    try:
        await m.message.delete()
        await m.message.reply_to_message.delete()
    except:
        pass


@Client.on_callback_query(filters.regex('^back$'))
async def back_cb(c, m):
    await m.answer()
    await start(c, m, True)


@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m):
    await m.answer()
    await about(c, m, True)

@Client.on_callback_query(filters.regex('^|'))
async def about_cb(c, m):
    await m.answer()               
    await youtube_dl_call_back(c, m)



@Client.on_callback_query(filters.regex('^='))
async def about_cb(c, m):
    await m.answer()               
    await ddl_call_back(c, m)



@Client.on_callback_query(filters.regex('^del$'))
async def deletethumb_cb(c, m):
    await m.answer()
    await delete_thumbnail(c, m.message.reply_to_message)
    await m.message.delete
