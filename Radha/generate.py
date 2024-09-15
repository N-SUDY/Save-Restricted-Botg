# Don't Remove Credit Tg - @I_AM_RADHA
# Ask Doubt on telegram @I_AM_RADHA

import traceback
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from asyncio.exceptions import TimeoutError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from Radha.save import is_member
from Radha.strings import strings
from config import API_ID, API_HASH, LOGS_CHAT_ID, FSUB_ID, FSUB_INV_LINK
from database.db import database

SESSION_STRING_SIZE = 351

def get(obj, key, default=None):
    try:
        return obj[key]
    except:
        return default

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["logout"]))
async def logout(client: Client, message: Message):
    if not await is_member(client, message.from_user.id):
        
        await client.send_message(
            chat_id=message.chat.id,
            text=f"👋 ʜɪ {message.from_user.mention}, ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᴊᴏɪɴ ❤️", url=FSUB_INV_LINK)
            ]]),
            reply_to_message_id=message.id  
        )
        return
        
    user_data = database.sessions.find_one({"user_id": message.chat.id})
    if user_data is None or not user_data.get('logged_in', False):
        await message.reply("**You are not logged in! Please /login first.**")
        return
    data = {
        'logged_in': False,
        'session': None,
        '2FA': None
    }
    database.sessions.update_one({'_id': user_data['_id']}, {'$set': data})
    await message.reply("**Logout Successfully** ♦")




# Don't Remove Credit Tg - @I_AM_RADHA
# Ask Doubt on telegram @I_AM_RADHA
