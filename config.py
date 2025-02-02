import os

#Bot token @Botfather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

#Your API ID from my.telegram.org
API_ID = int(os.environ.get("API_ID", ""))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

#Admin IDs
ADMIN_ID = list(map(int, os.getenv("ADMIN_ID", "").split(",")))

#Database 
DB_URI = os.environ.get("DB_URI", "")

#Your Logs Channel/Group ID
LOGS_CHAT_ID = int(os.environ.get("LOGS_CHAT_ID", ""))

#Force Sub Channel ID
FSUB_ID = int(os.environ.get("FSUB_ID", ""))

#Force Sub Channel Invite Link
FSUB_INV_LINK = os.environ.get("FSUB_INV_LINK", "")
