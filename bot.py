import os
import asyncio
import random
import logging
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, MessageNotModified
from config import Config
from database import db
from fsub import get_fsub # Correct Import

# --- 🌐 Flask Web Server for Health Checks ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive! 🚀"
def run_web():
    try: app.run(host='0.0.0.0', port=8000)
    except: pass
def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# --- 🤖 Bot Client ---
bot = Client("FileStore", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

def main_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 ᴜᴘᴅᴀᴛᴇs", url=Config.CHNL_LNK),
         InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=Config.SUPP_LNK)],
        [InlineKeyboardButton("📜 ᴀʙᴏᴜᴛ", callback_data="about"),
         InlineKeyboardButton("🛡️ ʜᴇʟᴘ", callback_data="help")]
    ])

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await db.add_user(message.from_user.id)
    
    if len(message.command) > 1:
        data = message.command[1]
        
        # SMART FSUB: Only for Links
        is_joined = await get_fsub(client, message, data)
        if not is_joined:
            return # User not joined, FSub message sent from fsub.py

        # IF JOINED, FETCH FILE
        ms = await message.reply_text("<b>⌛ ꜰᴇᴛᴄʜɪɴɢ ʏᴏᴜʀ ꜰɪʟᴇ...</b>")
        try:
            if data.startswith("batch_"):
                ids = data.replace("batch_", "").split("-")
                for msg_id in range(int(ids[0]), int(ids[1]) + 1):
                    await client.copy_message(message.from_user.id, Config.DB_CHANNEL, msg_id)
                    await asyncio.sleep(0.5)
            else:
                msg_id = int(data.replace("file_", ""))
                await client.copy_message(message.from_user.id, Config.DB_CHANNEL, msg_id)
            await ms.delete()
        except:
            await ms.edit("❌ ꜰɪʟᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ!")
        return

    # Normal Start
    await message.reply_photo(
        photo=random.choice(Config.START_IMAGES),
        caption=Config.START_MSG.format(user=message.from_user.mention),
        reply_markup=main_buttons()
    )

# --- 📂 Range Batch Generator ---
@bot.on_message(filters.command("batch") & filters.user(Config.OWNER_ID))
async def batch_cmd(client, message):
    await message.reply_text("<b>sᴇɴᴅ ꜰɪʀsᴛ ᴀɴᴅ ʟᴀsᴛ ʟɪɴᴋ ꜰʀᴏᴍ ᴅʙ ᴄʜᴀɴɴᴇʟ.</b>")

@bot.on_message(filters.private & filters.text & filters.user(Config.OWNER_ID))
async def admin_links(client, message):
    if "t.me/" in message.text and "/start" not in message.text:
        msg_id = int(message.text.split('/')[-1])
        if not hasattr(client, "temp_id"):
            client.temp_id = msg_id
            await message.reply_text("✅ First Link Saved! Now send Last Link.")
        else:
            link = f"https://t.me/{client.me.username}?start=batch_{client.temp_id}-{msg_id}"
            await message.reply_text(f"✅ Batch Link: <code>{link}</code>")
            delattr(client, "temp_id")

# --- 📢 Broadcast ---
@bot.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID) & filters.reply)
async def broadcast(client, message):
    users = await db.get_all_users()
    sts = await message.reply_text("🚀 Broadcasting...")
    success, failed = 0, 0
    async for user in users:
        try:
            await message.reply_to_message.copy(chat_id=int(user['id']))
            success += 1
        except: failed += 1
    await sts.edit(f"✅ Done! Success: {success}")

# --- 🖱️ Callbacks ---
@bot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    try:
        if query.data == "about":
            await query.message.edit_caption(Config.ABOUT_MSG, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back")]]))
        elif query.data == "help":
            await query.message.edit_caption(Config.HELP_MSG, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back")]]))
        elif query.data == "back":
            await query.message.edit_caption(Config.START_MSG.format(user=query.from_user.mention), reply_markup=main_buttons())
        await query.answer()
    except MessageNotModified: pass

if __name__ == "__main__":
    keep_alive()
    bot.run)
