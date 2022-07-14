#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | @Tellybots

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
import json
import math
import os
import shutil
import time
from datetime import datetime
from pyrogram import enums 
from Uploader.config import Config
from Uploader.script import Translation
from Uploader.thumbnail import *
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram.types import *
from Uploader.functions.display_progress import progress_for_pyrogram, humanbytes
from Uploader.database.database import db
from PIL import Image
from Uploader.functions.ran_text import random_char




       
            start_time = time.time()

            # try to upload file

            if (await db.get_upload_as_doc(update.from_user.id)) is False:
                thumbnail = await Gthumb01(bot, update)
                await bot.send_document(
                    chat_id=update.message.chat.id,
                    document=download_directory,
                    thumb=thumbnail,
                    caption=description,
                    #parse_mode="HTML",
                    reply_to_message_id=update.message.reply_to_message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        #custom_file_name,
                        start_time
                    )
                )

            elif tg_send_type == "video":
                 width, height, duration = await Mdata01(download_directory)
                 thumbnail = await Gthumb02(bot, update, duration, download_directory)
                 await bot.send_video(
                    chat_id=update.message.chat.id,
                    video=download_directory,
                    caption=description,
                    # parse_mode="HTML",
                    duration=duration,
                    width=width,
                    height=height,
                    thumb=thumbnail,
                    supports_streaming=True,
                    reply_to_message_id=update.message.reply_to_message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        #custom_file_name,
                        start_time
                    )
                )
            if tg_send_type == "audio":
                duration = await Mdata03(download_directory)
                thumbnail = await Gthumb01(bot, update)
                await bot.send_audio(
                    chat_id=update.message.chat.id,
                    audio=download_directory,
                    caption=description,
                   # parse_mode="HTML",
                    duration=duration,
                    thumb=thumbnail,
                    reply_to_message_id=update.message.reply_to_message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        #custom_file_name,
                        start_time
                    )
                ) 
            elif tg_send_type == "vm":
                width, duration = await Mdata02(download_directory)
                thumbnail = await Gthumb02(bot, update, duration, download_directory)
                await bot.send_video_note(
                    chat_id=update.message.chat.id,
                    video_note=download_directory,
                    duration=duration,
                    length=width,
                    thumb=thumb_image_path,
                    reply_to_message_id=update.message.reply_to_message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        #custom_file_name,
                        start_time
                    )
                )           
            
     
            else:
                logger.info("✅ " + custom_file_name)
            end_two = datetime.now()
            try:
                os.remove(download_directory)
                os.remove(thumb_image_path)
            except:
                pass
            time_taken_for_download = (end_one - start).seconds
            time_taken_for_upload = (end_two - end_one).seconds
            await bot.edit_message_text(
                text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload),
                chat_id=update.message.chat.id,
                message_id=update.message.id,
                disable_web_page_preview=True
            )

            logger.info("✅ Downloaded in: " + str(time_taken_for_download))
            logger.info("✅ Uploaded in: " + str(time_taken_for_upload))
