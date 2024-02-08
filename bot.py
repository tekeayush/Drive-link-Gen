from time import sleep, time
import re
from secrets import choice
import aiohttp
import hashlib
import json
import base64
import logging
import requests
import urllib.parse
import cloudscraper
from lxml import etree
from os import environ
from bs4 import BeautifulSoup
from base64 import b64decode
from urllib.parse import unquote
from pyrogram import Client, filters
from modules.appdrive import appdrive_dl
from modules.katdrive import katdrive_dl
from modules.kolop import kolop
from urllib.parse import urlparse,parse_qs
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup, Chat
import random


logging.basicConfig(level=logging.INFO)
for log_name, log_obj in logging.Logger.manager.loggerDict.items():
     if log_name != 'pyrogram':
          log_obj.disabled = True

LOGGER = logging.getLogger(__name__)


conatact = ""
API_ID = ''
API_HASH =''
BOT_TOKEN = ''
GDTOT = ["UGNidkdhTnpLLytlYjUxY3ZBdWZQbDI5dzc0QldtTU1ZSDczUC9UUXFqZz0%3D", "eWhlVlFTc2xLV201eWxKczNFNUJnTUI4WnBGdm1GWTNjMzU0MmpiSHNpQT0%3D", "eXU2cDlzYWhzRk93eXV4cTQzMXFCeHE2UElEcUtJcEY1U0Y5N1hCWmY0ST0%3D", "U3g2ZkhNY1hjWVg3K296UnJoNHY0K21SWVRCRVpPVGc0VzNvTGpEMm1UQT0%3D", "YVV1a25VaHljNGY5cmV2RHF0VDZ2cm1SNSt2UVJVK3N1b3ltWk9SM05iaz0%3D"]
HUB_CRYPT = ["MjQvQXNwT0pPVmY0Rm02enhEMTRVbGpsY1dzenc2ZzBCVnREbnFXazl0dz0%3D", "Y0kzMk1nTTRHaW1XV2tNVm80RjJJa0lYdzhjVnZraXk1ZHZyRWpkRzMwWT0%3D", "OWI3Z1JwNkFtd2hDZjkwb0lWU2M5d0RIUjdSK3VUSDlYT2hZM1FuUXJ1bz0%3D", "TmloUTduYU5wajFUajZYNjFreVlReUQ5NHNXUnlhaWE1K1hHOEF5aXdiOD0%3D", "ZHl6cDFqSVJ2OGFHR2xyUW03WGNZWnJtY2ZqOTBuM3drNmZhbWhOY2FBND0%3", "UGxKN1B2MWxmTFhiaU8ybGRrRVMreldPUDN4Qm5malpGV25SMEYzcmEyaz0%3D", "d1RuWnVOWUtqS3p2bVZjKzMyOUxrRm9uRnQ0WElvTkpqaTIxWklRekFZbz0%3D"]
FORCE_CHNL = "bypassurl"
CHNL_ID = -1001715931550

bot = Client('shorturlbypasserbot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


async def send_log(chat_id: Chat, text: str):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except FloodWait as f:
        sleep(f.x * 1)
        return send_log(chat_id, text)
    except Exception as e:
        LOGGER.error(str(e))


def link_checker(url):
    if "gdtot" in url:
        return is_gdtot(url)
    elif "hubdrive" in url:
        return is_hub(url)
    elif "appdrive" or "driveapp" in url:
        return is_appdrive(url)
    elif "katdrive" in url:
        return is_kat(url)
    elif "kolop" in url:
        return is_kolop(url)
    else:
        raise Exception(f'No Bypass Function Found For {url}')

msg = "Support For Gdtot is Temporary Not Availabe"

def is_gdtot(url):
    return msg

def is_appdrive(url):
    return appdrive_dl(url)

def is_hub(url):
    return hubdrive_dl(url)

def is_kolop(url):
    return kolop(url)

def is_kat(url):
    return katdrive_dl(url)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    if FORCE_CHNL:
        try:
            user = await bot.get_chat_member(FORCE_CHNL, message.from_user.id)
            if user.status == "kicked out":
                await message.reply_text(f"You Are Banned\nContact @BC_contact_bot To get Unbanned")
                return
        except UserNotParticipant:
            await message.reply_text(
                text = f"You Haven't Joined My Updates Channel @{FORCE_CHNL}\n\n Join It Using Below Link",
                reply_markup = InlineKeyboardMarkup([[
                    InlineKeyboardButton("Updates channel", url=f"t.me/{FORCE_CHNL}")
                ]])
            )
            return
    LOGGER.info(f"{message.chat.first_name} Just Started me")
    text = f"Hey {message.chat.first_name}\n\n I'm A public link generator bot.\n\nFollowing are the supported sites\n\n<b>1.GDTOT\n2.Appdrive/Driveapp\n3.HubDrive\n4.KatDrive\n5.kolop"
    BUTTONS = [
        [
            InlineKeyboardButton("Updates Channel", url=f"t.me/{FORCE_CHNL}"),
            InlineKeyboardButton("Conatct Owner", url=f"t.me/{conatact}")
        ],
        [
            InlineKeyboardButton("Linkvertise Bypass", url=f"t.me/linkvertis_bot"),
            InlineKeyboardButton("BYPASSER Bot", url=f"t.me/bypasss_bot")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(BUTTONS)
    await message.reply((text), reply_markup=reply_markup)


@bot.on_message(filters.regex(r'[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)') & filters.private)
async def link_handler(bot, message):
    url = message.matches[0].group(0)
    if FORCE_CHNL:
        try:
            user = await bot.get_chat_member(FORCE_CHNL, message.from_user.id)
            if user.status == "kicked out":
                await message.reply_text("You Are Banned\nContact @BC_contact_bot To get Unbanned")
                return
        except UserNotParticipant:
            await message.reply_text(
                text = f"You Haven't Joined My Updates Channel @{FORCE_CHNL}\n\n Join It Using Below Link",
                reply_markup = InlineKeyboardMarkup([[
                    InlineKeyboardButton("Updates Channel", url=f"t.me/{FORCE_CHNL}")
                ]])
            )
            return
    LOGGER.info(f"reciverd new link from {message.from_user.id} {message.chat.first_name} Bypassing {url}")
    try:
     await message.reply(f'wait for few sec')
     bypass = link_checker(url)
     await send_log(CHNL_ID, f'<b>name</b>:<code>{message.from_user.username}</code>\n</b>Id</b>:<code>{message.from_user.id}</code>\n<b>Source Link</b>:<code>{url}</code>\n<b>bypassed Link</b>:<code>{bypass}</code>')
     await message.reply(f"Here is your Public Drive Link\n\n{bypass}")
    except Exception as e:
        LOGGER.error(e)
        await message.reply(f"{e}", quote=True)                


# ==========================================

def gd_parse(res):
    title = re.findall(">(.*?)<\/h5>", res.text)[0]
    info = re.findall('<td\salign="right">(.*?)<\/td>', res.text)
    parsed_info = {
        'error': True,
        'message': 'Link Invalid.',
        'title': title,
        'size': info[0],
        'date': info[1]
    }
    return parsed_info

# ==========================================

def gdtot_dl(url):
    client = requests.Session()
    creds = (random.choice(GDTOT))
    client.cookies.update({'crypt': creds})
    domain = url.split('/')[2]
    url2 = url.replace(domain, "new2.gdtot.sbs")
    res = client.get(url2)
    res = client.get(f"https://new2.gdtot.sbs/dld?id={url2.split('/')[-1]}")
    url2 = re.findall(r'URL=(.*?)"', res.text)[0]
    info = {}
    info["error"] = False
    params = parse_qs(urlparse(url2).query)
    if "gd" not in params or not params["gd"] or params["gd"][0] == "false":
        info["error"] = True
        if "msgx" in params:
            info["message"] = params["msgx"][0]
        else:
            info["message"] = "Invalid link"
    else:
        gd_id = base64.b64decode(str(params["gd"][0])).decode("utf-8")
        drive_link = f"https://drive.google.com/open?id={gd_id}"
        info["gdrive_link"] = drive_link
        lol = info['gdrive_link']
    if not info["error"]:
        return lol



def parse_info(res):
    info_parsed = {}
    title = re.findall('>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall('>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed

def hubdrive_dl(url):
    if "hubdrive.in" in url:
        url = url.replace(".in", ".me")
    elif "hubdrive.cc" in url:
        url = url.replace(".cc", ".me")
    else:
        pass
    client = requests.Session()
    creds = (random.choice(HUB_CRYPT))
    client.cookies.update({'crypt': creds})
    LOGGER.info(f'using {creds}')
    
    res = client.get(url)
    info_parsed = parse_info(res)
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    
    data = { 'id': file_id }
    
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except: return {'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url
    lol = info_parsed['gdrive_url']

    return lol
# ==============================================
LOGGER.info('I AM ALIVE')
bot.run()
