import os
from Uploader.functions.display_progress import progress_for_pyrogram, humanbytes
from Uploader.config import Config
from Uploader.dl_button import ddl_call_back
from Uploader.button import youtube_dl_call_back
from Uploader.settings.settings import OpenSettings
from Uploader.script import Translation
from pyrogram import Client, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Uploader.database.database import db
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



@Client.on_callback_query()
async def button(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            reply_markup=Translation.START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=Translation.HELP_TEXT,
            reply_markup=Translation.HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=Translation.ABOUT_TEXT,
            reply_markup=Translation.ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "OpenSettings":
        await update.answer()
        await OpenSettings(update.message)
    elif update.data == "showThumbnail":
        thumbnail = await db.get_thumbnail(update.from_user.id)
        if not thumbnail:
            await update.answer("You didn't set any custom thumbnail!", show_alert=True)
        else:
            await update.answer()
            await bot.send_photo(update.message.chat.id, thumbnail, "Custom Thumbnail",
                               reply_markup=types.InlineKeyboardMarkup([[
                                   types.InlineKeyboardButton("Delete Thumbnail",
                                                              callback_data="deleteThumbnail")
                               ]]))
    elif update.data == "deleteThumbnail":
        await db.set_thumbnail(update.from_user.id, None)
        await update.answer("Okay, I deleted your custom thumbnail. Now I will apply default thumbnail.", show_alert=True)
        await update.message.delete(True)
    elif update.data == "setThumbnail":
        await update.message.edit_text(
            text=Translation.TEXT,
            reply_markup=Translation.BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "triggerUploadMode":
        await update.answer()
        upload_as_doc = await db.get_upload_as_doc(update.from_user.id)
        if upload_as_doc:
            await db.set_upload_as_doc(update.from_user.id, False)
        else:
            await db.set_upload_as_doc(update.from_user.id, True)
        await OpenSettings(update.message)
    

    elif "close" in update.data:
        await update.message.delete(True)
    
    if update.data.startswith("cancel"):
        cmf = update.data.split("|")
        chat_id, mes_id, from_usr = cmf[1], cmf[2], cmf[3]
        if (int(update.from_user.id) == int(from_usr)) or g:
            await bot.answer_callback_query(
                update.id, text="Trying to cancel...", show_alert=False
            )
            gDict[int(chat_id)].append(int(mes_id))

    elif "|" in update.data:


        await youtube_dl_call_back(bot, update)
    elif "DelMedia" in update.data:
        saved_file_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".FFMpegRoBot.mkv"
        try:
            os.remove(saved_file_path)
            print(saved_file_path, " removed/deleted successfully.")
            await bot.edit_message_text(chat_id=update.message.chat.id, message_id=update.message.id, text=f"✅ Media file deleted successfully.")
        except Exception as fc:
            print(fc)
    elif "NO-delM" in update.data:
        await bot.edit_message_text(chat_id=update.message.chat.id, message_id=update.message.id, text=f"Media file is not deleted.")
    elif "//" in update.data:
        szze, ms_id = update.data.rsplit('//')
        download_directory = Config.DOWNLOAD_LOCATION + "/" + str(ms_id)
        smze, vtt = 0, 0
        '''ToStr = ' •• '.join(map(str, os.listdir(download_directory)))
        await bot.send_message(chat_id = update.message.chat.id, text=ToStr)
        print(os.listdir(download_directory), "cb_buttons")
        print('\n\n', update.data, 'cb_buttons')'''
        if os.path.isdir(download_directory):
          lsst=os.listdir(download_directory)
          try:
            for vt in lsst:
              if ".vtt" in vt:
                vtt+=1
            for ele in os.scandir(download_directory):
              smze+=os.path.getsize(ele)
              siio = humanbytes(int(smze))
          except Exception as vit:
            print(vit, "Error Exception vtt")
            pass
        if not os.path.isdir(download_directory):
            siio='This file is not present in the directory!'
            await update.answer(siio)
            '''elif:
            for ele in os.scandir(download_directory):
                smze+=os.path.getsize(ele)
            if smze>int(update.data.split("//")[1])*1.2:
                await update.answer("Video Downloded Successfully. \n\n Now Downloading audio", show_alert="True")
             elif:
            for ele in os.scandir(download_directory):
                smze+=os.path.getsize(ele)
            if smze>int(update.data.split("//")[1]):
                await update.answer("Video, audio downloaded sucessfully. \n\n Upload starts soon.", show_alert="True")'''
        elif len(lsst)-vtt == 4:
            await update.answer("Video & Audio downloaded sucessfully\n\nUploading starts soon. . .")
        elif "N/A" in update.data:
            await update.answer(f'Downloaded: {siio} of {"N/A"}')
        elif "None" in update.data:
            await update.answer(f'Downloaded: {siio} of {"N/A"}')
        else:
            if int(smze)<int(szze):
                await update.answer(f'Downloaded: {siio} of {humanbytes(int(szze))}')
            else:
                diff = int(smze)-int(szze)
                print(lsst, "video downloaded successfully")
                await update.answer(f'Video Downloded Successfully: {humanbytes(int(szze))} \n\n Now Downloading audio: {humanbytes(diff)}', show_alert="True")
    elif "=" in update.data:
        await ddl_call_back(bot, update)

    else:
        await update.message.delete()

