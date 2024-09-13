# Don't Remove Credit Tg - @I_AM_RADHA
# Ask Doubt on telegram @I_AM_RADHA


from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

class Bot(Client):

    def __init__(self):
        super().__init__(
            "Radha_savelogin",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="Radha"),
            workers=50,
            sleep_threshold=10
        )

      
    async def start(self):
            
        await super().start()
        print('Bot Started Powered By @I_AM_RADHA')

    async def stop(self, *args):

        await super().stop()
        print('Bot Stopped Bye')

# Don't Remove Credit Tg - @I_AM_RADHA
# Ask Doubt on telegram @I_AM_RADHA
