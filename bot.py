import os
import asyncio
import random
import logging
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant, FloodWait, MessageNotModified
from config import Config
from database import db
from fsub import get_fsub # Separate FSub logic

# --- 🌐 Flask Web Server for Health Checks ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive! 🚀"

def run_web():
    try: app.run(host='0.0.0.0', port=8000)
    except Exception as e: print(f"Flask Error: {e}")

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# --- 🤖 Bot Client ---
bot = Client(
    "FileStoreBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# --- ⌨️ Stylish Buttons ---
def main_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 ᴜᴘᴅᴀᴛᴇs", url=Config.CHNL_LNK),
         InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=Config.SUPP_LNK)],
        [InlineKeyboardButton("📜 ᴀʙᴏᴜᴛ", callback_data="about"),
         InlineKeyboardButton("🛡️ ʜᴇʟᴘ", callback_data="help")]
    ])

# --- 🏠 Start Handler ---
@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    # Save User to DB
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)

    # Check if user clicked a Link
    if len(message.command) > 1:
        data = message.command[1]
        
        # --- SMART FSUB CHECK ---
        if Config.FSUB_ON:
            is_joined = await get_fsub(client, message, data)
            if not is_joined:
                return # Stop here if not joined

        # If Joined, Forward Files
        ms = await message.reply_text("<b>⌛ ꜰᴇᴛᴄʜɪɴɢ ʏᴏᴜʀ ꜰɪʟᴇs...</b>")
        try:
            if data.startswith("batch_"):
                # Range Batch Logic
                ids = data.replace("batch_", "").split("-")
                first_id, last_id = int(ids[0]), int(ids[1])
                for msg_id in range(first_id, last_id + 1):
                    try:
                        await client.copy_message(chat_id=message.from_user.id, from_chat_id=Config.DB_CHANNEL, message_id=msg_id)
                        await asyncio.sleep(0.5)
                    except: pass
                await ms.delete()
            else:
                # Single File Logic
                msg_id = int(data.replace("file_", ""))
                await client.copy_message(chat_id=message.from_user.id, from_chat_id=Config.DB_CHANNEL, message_id=msg_id)
                await ms.delete()
        except Exception as e:
            await ms.edit(f"❌ ᴇʀʀᴏʀ: ꜰɪʟᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ!\n`{e}`")
        return

    # Normal Start Message
    await message.reply_photo(
        photo=random.choice(Config.START_IMAGES),
        caption=Config.START_MSG.format(user=message.from_user.mention),
        reply_markup=main_buttons()
    )

# --- 📢 Broadcast ---
@bot.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID) & filters.reply)
async def broadcast_handler(client, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text("🚀 Broadcasting...")
    success, failed = 0, 0
    async for user in users:
        try:
            await b_msg.copy(chat_id=int(user['id']))
            success += 1
        except: failed += 1
    await sts.edit(f"✅ Success: {success} | Failed: {failed}")

# --- 📊 Stats ---
@bot.on_message(filters.command("stats") & filters.user(Config.OWNER_ID))
async def stats_handler(client, message):
    total = await db.total_users_count()
    await message.reply_text(f"📊 Total Users: {total}")

# --- 📂 Range Batch Generator ---
@bot.on_message(filters.command("batch") & filters.user(Config.OWNER_ID))
async def batch_cmd(client, message):
    await message.reply_text("<b>sᴇɴᴅ ꜰɪʀsᴛ ᴀɴᴅ ʟᴀsᴛ ʟɪɴᴋ ꜰʀᴏᴍ ᴅʙ ᴄʜᴀɴɴᴇʟ.</b>")

@bot.on_message(filters.private & filters.text & filters.user(Config.OWNER_ID))
async def admin_link_handler(client, message):
    if "t.me/" in message.text and "/start" not in message.text:
        msg_id = int(message.text.split('/')[-1])
        if not hasattr(client, "temp_id"):
            client.temp_id = msg_id
            await message.reply_text("✅ First Link Saved! Now send Last Link.")
        else:
            link = f"https://t.me/{client.me.username}?start=batch_{client.temp_id}-{msg_id}"
            await message.reply_text(f"✅ Batch Link: <code>{link}</code>")
            delattr(client, "temp_id")

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
    bot.run()
