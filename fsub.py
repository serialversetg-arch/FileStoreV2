import asyncio
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

async def get_fsub(client, message, data):
    """
    Check if user is subscribed. 
    Returns True if joined, False if not.
    """
    try:
        # ID ko integer mein convert karna zaroori hai
        user_status = await client.get_chat_member(int(Config.FSUB_CHANNEL), message.from_user.id)
        
        # Agar user kicked hai toh access nahi dena
        if user_status.status == "kicked":
            await message.reply_text("<b>sᴏʀʀʏ, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ.</b>")
            return False
            
        return True # User joined hai

    except (UserNotParticipant, Exception):
        # Yahan tabhi aayega jab user joined nahi hoga ya koi error aayega
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ", url=Config.CHNL_LNK)],
            [InlineKeyboardButton("🔄 ᴛʀʏ ᴀɢᴀɪɴ", url=f"https://t.me/{client.me.username}?start={data}")]
        ])
        
        await message.reply_photo(
            photo=Config.FSUB_IMAGE,
            caption=Config.FSUB_MSG,
            reply_markup=join_button
        )
        return False
