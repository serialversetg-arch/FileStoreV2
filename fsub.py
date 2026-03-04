from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

async def get_fsub(client, message, data):
    try:
        # User ka status check karein
        user = await client.get_chat_member(int(Config.FSUB_CHANNEL), message.from_user.id)
        
        # Agar user ka status niche diye gaye list mein hai, toh wo JOINED hai
        if user.status in ["member", "administrator", "creator"]:
            return True 
        else:
            raise UserNotParticipant

    except (UserNotParticipant, Exception):
        # Ye block tabhi chalega jab user JOINED NAHI hoga
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
