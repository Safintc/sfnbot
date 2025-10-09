import re
from os import environ
from Script import script
from time import time

# Regex for numeric IDs
id_pattern = re.compile(r'^-?\d+$')

# Helper to parse boolean strings
def is_enabled(value, default=False):
    if isinstance(value, bool):
        return value
    if str(value).lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif str(value).lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# -------------------- Bot Info --------------------
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ.get('API_ID', '21116415'))
API_HASH = environ.get('API_HASH', '8e23c9d97d71d525741e33f6b3584f45')
BOT_TOKEN = environ.get('BOT_TOKEN', '8420823401:AAF5SEgM6vwB5swBQRbUjfdlmU6RU8nv5yY')

# -------------------- Bot Settings --------------------
BOT_START_TIME = time()
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = is_enabled(environ.get('USE_CAPTION_FILTER', False))
PICS = (environ.get('PICS', 'https://ibb.co/0jvxD3Tj')).split()

# -------------------- Admins, Channels & Users --------------------
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '21116415').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1002577824824').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '21116415').split()]
AUTH_USERS = auth_users + ADMINS if auth_users else ADMINS

auth_channel = environ.get('AUTH_CHANNEL', '-1002584950282')
auth_grp = environ.get('AUTH_GROUP', '-1002584950282')
AUTH_CHANNEL = [int(ch) for ch in auth_channel.split() if id_pattern.search(ch)]
AUTH_GROUPS = [int(ch) for ch in auth_grp.split() if id_pattern.search(ch)] if auth_grp else []

FORCE_SUB1 = environ.get('FORCE_SUB1', 'https://t.me/moviestoreupdates')
FORCE_SUB2 = environ.get('FORCE_SUB2', 'https://t.me/sfn_moviestore')

# -------------------- MongoDB --------------------
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://safin:x0EwcqRWeyafnQIo@cluster0.1qpfh4t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'files')

# -------------------- Other Settings --------------------
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002955494336'))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'sfn_moviestore')
P_TTI_SHOW_OFF = is_enabled(environ.get('P_TTI_SHOW_OFF', 'True'))
IMDB = is_enabled(environ.get('IMDB', 'False'), True)
SINGLE_BUTTON = is_enabled(environ.get('SINGLE_BUTTON', 'True'))
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CUSTOM_FILE_CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION",
                                 "📂 <em>File Name</em>: <code>{file_name}</code>\n\n ♻ <em>File Size</em>:{file_size} \n\n <b><i>Latest Movies -</i> [ELDORADO](https://t.me/moviestoreupdates) </b>")
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE",
                            "🏷 𝖳𝗂𝗍𝗅𝖾: <a href={url}>{title}</a> \n🔮 𝖸𝖾𝖺𝗋: {year} \n⭐️ 𝖱𝖺𝗍𝗂𝗇𝗀𝗌: {rating}/10 \n🎭 𝖦𝖾𝗇𝖾𝗋𝗌: {genres} \n\n🎊 𝖯𝗈𝗐𝖾𝗋𝖾𝖽 𝖡𝗒 [Sfn Bot](https://t.me/sfnmoviesbot)")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"))
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"))
MAX_LIST_ELM = int(environ.get("MAX_LIST_ELM", 0)) if environ.get("MAX_LIST_ELM") else None

INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in environ.get('FILE_STORE_CHANNEL', '-1002964079847').split()]
MELCOW_NEW_USERS = is_enabled(environ.get("MELCOW_NEW_USERS", "True"))
PROTECT_CONTENT = is_enabled(environ.get("PROTECT_CONTENT", "False"))
PUBLIC_FILE_STORE = is_enabled(environ.get("PUBLIC_FILE_STORE", "False"))

# -------------------- Logging Info --------------------
LOG_STR = f"""
Current Bot Configuration:
- IMDB Results: {"Enabled" if IMDB else "Disabled"}
- P_TTI_SHOW_OFF: {"Enabled" if P_TTI_SHOW_OFF else "Disabled"}
- SINGLE_BUTTON: {"Enabled" if SINGLE_BUTTON else "Disabled"}
- CUSTOM_FILE_CAPTION: {CUSTOM_FILE_CAPTION}
- LONG_IMDB_DESCRIPTION: {"Enabled" if LONG_IMDB_DESCRIPTION else "Disabled"}
- SPELL_CHECK_REPLY: {"Enabled" if SPELL_CHECK_REPLY else "Disabled"}
- MAX_LIST_ELM: {MAX_LIST_ELM if MAX_LIST_ELM else "Full list"}
- IMDB_TEMPLATE: {IMDB_TEMPLATE}
"""


