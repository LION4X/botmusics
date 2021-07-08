from pyrogram import Client, filters
import asyncio
import os
from pytube import YouTube
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from youtubesearchpython import VideosSearch
from AlexaSongBot import app, LOGGER
from AlexaSongBot.sql.chat_sql import add_chat_to_db
import aiohttp



from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent



def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()

 #For private messages        
 #Ignore commands
 #No bots also allowed
@app.on_message(filters.private & ~filters.bot & ~filters.command("help") & ~filters.command("start") & ~filters.command("[s],[song]"))  
#Lets Keep this Simple
async def song(client, message):
  # Hope this will fix the args issue
  # defining args as a array instead of direct defining
  # also splitting text for correct yt search
  

    message.chat.id
    user_id = message.from_user["id"]
    chat_id = message.chat.id
    args = message.text.split(None, 1)
    add_chat_to_db(str(chat_id))
    args = str(args)
    # Adding +song for better  searching
    args = args + " " + "song"
    #Defined above.. THINK USELESS
    #args = get_arg(message) + " " + "song"

    #Added while callback... I think Useless    
    #if args.startswith("/help"):
        #return ""    
    status = await message.reply(
             text="<b>Downloading your song, Plz wait 😉 \n\n🎶•••🎵•••🎧•••</b>",
             disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                    InlineKeyboardButton(
                                        "𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙𝙞𝙣𝙜 •••", url="https://t.me/GalaxyLanka")
                                ]]
                        ),
               parse_mode="html",
        reply_to_message_id=message.message_id
      )
    video_link = yt_search(args)
    if not video_link:
        await status.edit("<b>Song not found 🥺</b>")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("<b>Failed to download song 🤕</b>")
        LOGGER.error(ex)
        return ""
    os.rename(download, f"{str(user_id)}.mp3")
    await app.send_chat_action(message.chat.id, "upload_audio")
    await app.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        thumb="C:\\Users\\MARIO\\Desktop\\pyTelegramBotAPI\\Song-Downloader-main\\cc.jpg",
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")    


print(
    """
Bot Started!
Join @HiTechRockets
"""
)



