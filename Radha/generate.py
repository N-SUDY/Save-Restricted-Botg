# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import traceback
from pyrogram.types import Message
from pyrogram import Client, filters
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
from Radha.strings import strings
from Radha.save import is_member
from config import API_ID, API_HASH, LOGS_CHAT_ID, FSUB_ID, FSUB_INV_LINK
from database.db import database
import logging
logging.basicConfig(level=logging.INFO)

SESSION_STRING_SIZE = 351

def get(obj, key, default=None):
    try:
        return obj[key]
    except:
        return default

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["logout"]))
async def logout(_, message: Message):
    user_data = database.sessions.find_one({"user_id": message.from_user.id})
    if user_data is None or not user_data.get('logged_in', False):
        await message.reply("**You are not logged in! Please /login first.**")
        return 
    data = {
        'logged_in': False,
        'session': None,
        '2FA': None
    }
    database.update_one({'_id': user_data['_id']}, {'$set': data})
    await msg.reply("**Logout Successfully** ♦")

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["login"]))
async def login(bot: Client, message: Message):
    logging.info(f"Login command received from {message.chat.id}")
    
    try:
        # Check if the user already has a session
        if not database.sessions.find_one({"user_id": message.from_user.id}):
            logging.info("Inserting new user session data")
            database.sessions.insert_one({
                'user_id': message.from_user.id,
                'logged_in': False,
                'session': None,
                '2FA': None
            })

        user_data = database.sessions.find_one({"user_id": message.from_user.id})
        logging.info(f"User data for login: {user_data}")
        
        if get(user_data, 'logged_in', True):
            await message.reply("You are already logged in.")
            return
        
        user_id = int(message.from_user.id)
        phone_number_msg = await bot.ask(chat_id=user_id, text="Please send your phone number including the country code.")
        if phone_number_msg.text == '/cancel':
            return await phone_number_msg.reply('Process cancelled!')
        
        phone_number = phone_number_msg.text
        client = Client(":memory:", api_id=API_ID, api_hash=API_HASH)
        await client.connect()
        await phone_number_msg.reply("Sending OTP...")

        try:
            code = await client.send_code(phone_number)
            phone_code_msg = await bot.ask(user_id, "Please send OTP.", timeout=600)

        except PhoneNumberInvalid:
            await phone_number_msg.reply('Phone number is invalid.')
            return
        
        if phone_code_msg.text == '/cancel':
            return await phone_code_msg.reply('Process cancelled!')

        try:
            phone_code = phone_code_msg.text.replace(" ", "")
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)

        except PhoneCodeInvalid:
            await phone_code_msg.reply('OTP is invalid.')
            return
        except PhoneCodeExpired:
            await phone_code_msg.reply('OTP is expired.')
            return
        except SessionPasswordNeeded:
            two_step_msg = await bot.ask(user_id, 'Please enter the 2FA password.', timeout=300)
            if two_step_msg.text == '/cancel':
                return await two_step_msg.reply('Process cancelled!')
            try:
                password = two_step_msg.text
                await client.check_password(password=password)
            except PasswordHashInvalid:
                await two_step_msg.reply('Invalid password provided.')
                return

        string_session = await client.export_session_string()
        await client.disconnect()

        if len(string_session) < SESSION_STRING_SIZE:
            return await message.reply('Invalid session string.')
        
        # Update the session data in the database
        data = {
            'logged_in': True,
            'session': string_session,
            '2FA': password if 'password' in locals() else None
        }
        
        database.sessions.update_one({'user_id': message.from_user.id}, {'$set': data})
        await bot.send_message(message.from_user.id, "Login successful.")
    
    except Exception as e:
        logging.error(f"Error in login: {str(e)}")
        await message.reply(f"Error during login: {str(e)}")
        traceback.print_exc()
