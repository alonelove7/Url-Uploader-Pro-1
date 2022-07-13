#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | @Tellybots | @PlanetBots

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import requests, urllib.parse, filetype, os, time, shutil, tldextract, asyncio, json, math
from PIL import Image
from Uploader.config import Config
import time
from Uploader.script import Translation
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import filters
from pyrogram import Client, enums
from Uploader.functions.forcesub import handle_force_subscribe
from Uploader.functions.display_progress import humanbytes
from Uploader.functions.help_uploadbot import DownLoadFile
from Uploader.functions.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from Uploader.functions.ran_text import random_char
from Uploader.database.database import db
from Uploader.database.add import AddUser

from pyrogram.types import Thumbnail

f = filters.private & filters.regex(pattern=".*http.*")

@Client.on_message(f)
async def echo(bot, update):
    await AddUser(bot, update)
    if Config.LOG_CHANNEL:
        try:
            log_message = await update.forward(Config.LOG_CHANNEL)
            log_info = "Message Sender Information\n"
            log_info += "\nFirst Name: " + update.from_user.first_name
            log_info += "\nUser ID: " + str(update.from_user.id)
            log_info += "\nUsername: @" + update.from_user.username if update.from_user.username else ""
            log_info += "\nUser Link: " + update.from_user.mention
            await log_message.reply_text(
                text=log_info,
                disable_web_page_preview=True,
                quote=True
            )
        except Exception as error:
            print(error)


    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, update)
      if fsub == 400:
        return
    logger.info(update.from_user)
    url = update.text
    youtube_dl_username = None
    youtube_dl_password = None
    file_name = None

    print(url)
    if "|" in url:
        url_parts = url.split("|")
        if len(url_parts) == 2:
            url = url_parts[0]
            file_name = url_parts[1]
        elif len(url_parts) == 4:
            url = url_parts[0]
            file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in update.entities:
                if entity.type == "text_link":
                    url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    url = url[o:o + l]
        if url is not None:
            url = url.strip()
        if file_name is not None:
            file_name = file_name.strip()
        # https://stackoverflow.com/a/761825/4723940
        if youtube_dl_username is not None:
            youtube_dl_username = youtube_dl_username.strip()
        if youtube_dl_password is not None:
            youtube_dl_password = youtube_dl_password.strip()
        logger.info(url)
        logger.info(file_name)
    else:
        for entity in update.entities:
            if entity.type == "text_link":
                url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                url = url[o:o + l]
    if Config.HTTP_PROXY != "":
        command_to_exec = [
            "yt-dlp",
            "--no-warnings",
            "--skip-unavailable-fragments",
            #"--youtube-skip-dash-manifest",
            "-j",
            url,
            "--proxy", Config.HTTP_PROXY
        ]
    elif "/shorts/" in url:
        command_to_exec = [
            "yt-dlp",
            "--no-warnings",
           # "--youtube-skip-dash-manifest",
            "--skip-unavailable-fragments",
            "-j",
            url
        ]        
    else:
        command_to_exec = [
            "yt-dlp",
            "--no-warnings",
            "--skip-unavailable-fragments",
            #"--youtube-skip-dash-manifest",
            "-j",
            url
        ]

    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)

    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)
    logger.info(command_to_exec)
    chk = await bot.send_message(
            chat_id=update.chat.id,
            text=f'ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ʟɪɴᴋ ⌛',
            disable_web_page_preview=True,
            reply_to_message_id=update.id
            
          )
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    logger.info(e_response)
    t_response = stdout.decode().strip()
    #logger.info(t_response)
    # https://github.com/rg3/youtube-dl/issues/2630#issuecomment-38635239
    if e_response and "nonnumeric port" not in e_response:
        # logger.warn("Status : FAIL", exc.returncode, exc.output)
        error_message = e_response.replace("please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.", "")
        if "This video is only available for registered users." in error_message:
            error_message += Translation.SET_CUSTOM_USERNAME_PASSWORD
        await chk.delete()
        time.sleep(1)
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.NO_VOID_FORMAT_FOUND.format(str(error_message)),
            reply_to_message_id=update.id,
            
            disable_web_page_preview=True
        )
        return False
    if t_response:
        # logger.info(t_response)
        x_reponse = t_response
        if "\n" in x_reponse:
            x_reponse, _ = x_reponse.split("\n")
        response_json = json.loads(x_reponse)
        randem = random_char(5)
        save_ytdl_json_path = Config.DOWNLOAD_LOCATION + \
            "/" + str(update.from_user.id) + f'{randem}' + ".json"
        with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
        # logger.info(response_json)
        inline_keyboard = []
        duration = None
        if "duration" in response_json:
            duration = response_json["duration"]

        if 'entries' in response_json:
            for i in ['144', '240', '360', '480', '720', '1080', '1440', '2160']:
                video_format = f"bv*[height<={i}][ext=mp4]"
                buttons.sbutton(f"{i}-mp4", f"qu {msg_id} {video_format} t")
                video_format = f"bv*[height<={i}][ext=webm]"
                buttons.sbutton(f"{i}-webm", f"qu {msg_id} {video_format} t")
            buttons.sbutton("Audios", f"qu {msg_id} audio t")
            buttons.sbutton("Best Videos", f"qu {msg_id} {best_video} t")
            buttons.sbutton("Best Audios", f"qu {msg_id} {best_audio} t")
            buttons.sbutton("Cancel", f"qu {msg_id} cancel")
            YTBUTTONS = InlineKeyboardMarkup(buttons.build_menu(3))
            listener_dict[msg_id] = [listener, user_id, link, name, YTBUTTONS, args]
            bmsg = sendMarkup('Choose Playlist Videos Quality:', bot, message, YTBUTTONS)
        else:
            formats = response_json.get('formats')
            formats_dict = {}
            if formats is not None:
                for frmt in formats:
                    if not frmt.get('tbr') or not frmt.get('height'):
                        continue

                    if frmt.get('fps'):
                        quality = f"{frmt['height']}p{frmt['fps']}-{frmt['ext']}"
                    else:
                        quality = f"{frmt['height']}p-{frmt['ext']}"

                    if frmt.get('filesize'):
                        size = frmt['filesize']
                    elif frmt.get('filesize_approx'):
                        size = frmt['filesize_approx']
                    else:
                        size = 0

                    if quality in list(formats_dict.keys()):
                        formats_dict[quality][frmt['tbr']] = size
                    else:
                        subformat = {}
                        subformat[frmt['tbr']] = size
                        formats_dict[quality] = subformat

                for _format in formats_dict:
                    if len(formats_dict[_format]) == 1:
                        qual_fps_ext = re_split(r'p|-', _format, maxsplit=2)
                        height = qual_fps_ext[0]
                        fps = qual_fps_ext[1]
                        ext = qual_fps_ext[2]
                        if fps != '':
                            video_format = f"bv*[height={height}][fps={fps}][ext={ext}]"
                        else:
                            video_format = f"bv*[height={height}][ext={ext}]"
                        size = list(formats_dict[_format].values())[0]
                        buttonName = f"{_format} ({get_readable_file_size(size)})"
                        buttons.sbutton(str(buttonName), f"qu {msg_id} {video_format}")
                    else:
                        buttons.sbutton(str(_format), f"qu {msg_id} dict {_format}")
            buttons.sbutton("Audios", f"qu {msg_id} audio")
            buttons.sbutton("Best Video", f"qu {msg_id} {best_video}")
            buttons.sbutton("Best Audio", f"qu {msg_id} {best_audio}")
            buttons.sbutton("Cancel", f"qu {msg_id} cancel")
            YTBUTTONS = InlineKeyboardMarkup(buttons.build_menu(2))
            listener_dict[msg_id] = [listener, user_id, link, name, YTBUTTONS, args, formats_dict]
            bmsg = sendMarkup('Choose Video Quality:', bot, message, YTBUTTONS)




