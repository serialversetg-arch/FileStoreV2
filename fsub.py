import asyncio
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

async def get_fsub(client, message, data):
    """
    Checks if the user is a member/admin/creator of the FSub channel.
    Returns True if joined, False if not.
    """
    # Agar FSub off hai toh seedha True bhejo
    if not Config.FSUB_ON:
        return True

    try:
        # User ka status check karein (Member/Admin/Creator)
        user = await client.get_chat_member(int(Config.FSUB_CHANNEL), message.from_user.id)
        
        # Status check: Agar inme se kuch bhi hai toh wo Joined hai
        if user.status in ["member", "administrator", "creator"]:
            return True
        else:
            raise UserNotParticipant

    except (UserNotParticipant, Exception):
        # Ye tabhi chalega jab user JOINED NAHI hoga
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
