import os

class Config(object):
    # --- API & Tokens ---
    API_ID = int(os.environ.get("API_ID", "26910777"))
    API_HASH = os.environ.get("API_HASH", "8601f2f24993f6fdbcbac3bb27ceec38")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
    
    # --- Database (MongoDB) ---
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://King:Cobra765592@cluster0.qy4m5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    OWNER_ID = int(os.environ.get("OWNER_ID", "5232142502"))
    
    # --- Channels (Must be Integers) ---
    FSUB_CHANNEL = int(os.environ.get("FSUB_CHANNEL", "-1002730333831")) 
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002605527708")) 
    FSUB_ON = True 

    # --- Links ---
    CHNL_LNK = "https://t.me/Hindi_Tv_Verse"
    SUPP_LNK = "https://t.me/SerialVerse_support"

    # --- 🖼️ Premium Images ---
    START_IMAGES = [
        "https://i.ibb.co/S7609P4B/x.jpg",
        "https://i.ibb.co/G3Q974K3/x.jpg",
        "https://i.ibb.co/fzZTRQh8/x.jpg",
        "https://i.ibb.co/9Hnpgttg/x.jpg"
    ]
    FSUB_IMAGE = "https://i.ibb.co/S7609P4B/x.jpg"

    # --- 🎭 Stylish Texts ---
    START_MSG = """<b>✨ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ꜰɪʟᴇ sᴛᴏʀᴇ ✨</b>

<b>ʜᴇʟʟᴏ {user}, 👋</b>
<i>ɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ꜰɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ. sᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ, ᴀɴᴅ ɪ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ sʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ!</i>

<b>📊 sᴛᴀᴛᴜs:</b> <code>ᴀᴄᴛɪᴠᴇ ✅</code>
<b>🛡️ sᴇᴄᴜʀɪᴛʏ:</b> <code>ʜɪɢʜ 🔒</code>"""

    FSUB_MSG = """<b>🛑 ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ 🛑</b>

<b>ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜɴʟᴏᴄᴋ ᴛʜᴇ ꜰɪʟᴇs!</b>
<i>ᴅᴜᴇ ᴛᴏ sᴇᴄᴜʀɪᴛʏ ʀᴇᴀsᴏɴs, ᴏɴʟʏ sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʙᴏᴛ.</i>"""

    ABOUT_MSG = """<b>📝 ᴀʙᴏᴜᴛ ᴛʜɪs ʙᴏᴛ</b>

<b>● ɴᴀᴍᴇ:</b> <code>ꜰɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ</code>
<b>● ᴅᴇᴠᴇʟᴏᴘᴇʀ:</b> <a href='https://t.me/SerialVerse_support'>sᴇʀɪᴀʟ ᴠᴇʀsᴇ</a>
<b>● ᴄʜᴀɴɴᴇʟ:</b> <a href='https://t.me/Hindi_Tv_Verse'>ʜɪɴᴅɪ ᴛᴠ ᴠᴇʀsᴇ</a>
<b>● ʟɪʙʀᴀʀʏ:</b> <code>ᴘʏʀᴏɢʀᴀᴍ</code>

<b><i>ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀᴅᴠᴀɴᴄᴇᴅ ᴄʟᴏᴜᴅ sᴇʀᴠᴇʀs ⚡</i></b>"""

    HELP_MSG = """<b>🛠️ ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs</b>

<b>• /start -</b> ᴛᴏ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ.
<b>• /batch -</b> ᴄʀᴇᴀᴛᴇ ʀᴀɴɢᴇ ʙᴀᴛᴄʜ (ᴀᴅᴍɪɴ).
<b>• /stats -</b> ᴄʜᴇᴄᴋ ʙᴏᴛ sᴛᴀᴛs (ᴀᴅᴍɪɴ).
<b>• ᴜᴘʟᴏᴀᴅ -</b> sᴇɴᴅ ᴀɴʏ ꜰɪʟᴇ ᴛᴏ ɢᴇᴛ ʟɪɴᴋ.

<b>⚠️ ɴᴏᴛᴇ:</b> ɪꜰ ʏᴏᴜ ꜰᴀᴄᴇ ᴀɴʏ ɪssᴜᴇ, ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ."""
