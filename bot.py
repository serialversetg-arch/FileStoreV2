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

# --- 🌐 Flask Web Server (For Port 8000 Health Check) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Running Smoothly! 🚀"

def run_web():
    try: app.run(host='0.0.0.0', port=8000)
    except Exception as e: logging.error(f"Flask Error: {e}")

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# --- 🤖 Telegram Bot Client ---
bot = Client(
    "FileStoreBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# --- ⌨️ Stylish Keyboards ---
def main_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 ᴜᴘᴅᴀᴛᴇs", url=Config.CHNL_LNK),
         InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=Config.SUPP_LNK)],
        [InlineKeyboardButton("📜 ᴀʙᴏᴜᴛ", callback_data="about"),
         InlineKeyboardButton("🛡️ ʜᴇʟᴘ", callback_data="help")]
    ])

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ", callback_data="back")]])

# --- 🏠 Start & Link Handler ---
@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    # User ko DB mein save karo
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)

    # Check if user came from a Link (File or Batch)
    if len(message.command) > 1:
        data = message.command[1]
        
        # --- Smart Force Subscribe (Only for Links) ---
        if Config.FSUB_ON:
            try:
                await client.get_chat_member(int(Config.FSUB_CHANNEL), message.from_user.id)
            except (UserNotParticipant, Exception):
                btn = [[InlineKeyboardButton("📢 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ", url=Config.CHNL_LNK)],
                       [InlineKeyboardButton("🔄 ᴛʀʏ ᴀɢᴀɪɴ", url=f"https://t.me/{client.me.username}?start={data}")]]
                return await message.reply_photo(
                    photo=Config.FSUB_IMAGE,
                    caption=Config.FSUB_MSG,
                    reply_markup=InlineKeyboardMarkup(btn)
                )

        # --- Link Decoding & File Forwarding ---
        ms = await message.reply_text("<b>⌛ ꜰᴇᴛᴄʜɪɴɢ ʏᴏᴜʀ ꜰɪʟᴇs...</b>")
        try:
            if data.startswith("batch_"):
                # Range Batch Logic (e.g., batch_10-50)
                ids = data.replace("batch_", "").split("-")
                first_id, last_id = int(ids[0]), int(ids[1])
                for msg_id in range(first_id, last_id + 1):
                    try:
                        await client.copy_message(chat_id=message.from_user.id, from_chat_id=Config.DB_CHANNEL, message_id=msg_id)
                        await asyncio.sleep(0.5) # Flooding se bachne ke liye
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

    # Normal Start (No FSub Check here)
    await message.reply_photo(
        photo=random.choice(Config.START_IMAGES),
        caption=Config.START_MSG.format(user=message.from_user.mention),
        reply_markup=main_buttons()
    )

# --- 📂 Range Batch Generator (For Owner) ---
@bot.on_message(filters.command("batch") & filters.user(Config.OWNER_ID))
async def batch_generator(client, message):
    await message.reply_text(
        "<b>✨ ʀᴀɴɢᴇ ʙᴀᴛᴄʜ ᴍᴏᴅᴇ ✨</b>\n\n"
        "1. ᴀᴘɴᴇ DB ᴄʜᴀɴɴᴇʟ sᴇ <b>ꜰɪʀsᴛ ꜰɪʟᴇ</b> ᴋᴀ ʟɪɴᴋ ʙʜᴇᴊᴏ.\n"
        "2. ᴘʜɪʀ <b>ʟᴀsᴛ ꜰɪʟᴇ</b> ᴋᴀ ʟɪɴᴋ ʙʜᴇᴊᴏ."
    )

@bot.on_message(filters.private & filters.text & filters.user(Config.OWNER_ID))
async def handle_admin_links(client, message):
    if "t.me/" in message.text and "/start" not in message.text:
        try:
            msg_id = int(message.text.split('/')[-1])
            if not hasattr(client, "temp_id"):
                client.temp_id = msg_id
                await message.reply_text("<b>✅ ꜰɪʀsᴛ ʟɪɴᴋ sᴀᴠᴇᴅ!</b>\n\nɴᴏᴡ sᴇɴᴅ ᴛʜᴇ <b>ʟᴀsᴛ ꜰɪʟᴇ ʟɪɴᴋ</b>.")
            else:
                first_id = client.temp_id
                last_id = msg_id
                delattr(client, "temp_id")
                
                batch_link = f"https://t.me/{client.me.username}?start=batch_{first_id}-{last_id}"
                await message.reply_text(
                    f"<b>✅ ʙᴀᴛᴄʜ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ!</b>\n\n"
                    f"🔗 <b>ʟɪɴᴋ:</b> <code>{batch_link}</code>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔗 sʜᴀʀᴇ", url=f"https://t.me/share/url?url={batch_link}")]])
                )
        except:
            await message.reply_text("❌ Invalid Link! DB Channel ka link bhejo.")

# --- 📁 Single File Link Generator ---
@bot.on_message(filters.private & (filters.document | filters.video | filters.audio) & filters.user(Config.OWNER_ID))
async def single_file(client, message):
    msg = await message.copy(Config.DB_CHANNEL)
    link = f"https://t.me/{client.me.username}?start=file_{msg.id}"
    await message.reply_text(f"<b>✅ sɪɴɢʟᴇ ʟɪɴᴋ:</b>\n<code>{link}</code>")

# --- 📢 Broadcast & Stats ---
@bot.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID) & filters.reply)
async def broadcast(client, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text("🚀 Broadcasting...")
    success, failed = 0, 0
    async for user in users:
        try:
            await b_msg.copy(chat_id=int(user['id']))
            success += 1
        except: failed += 1
    await sts.edit(f"✅ Done!\nSuccess: {success} | Failed: {failed}")

@bot.on_message(filters.command("stats") & filters.user(Config.OWNER_ID))
async def stats(client, message):
    total = await db.total_users_count()
    await message.reply_text(f"📊 Total Users: {total}")

# --- 🖱️ Button Callbacks ---
@bot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    try:
        if query.data == "about":
            await query.message.edit_caption(caption=Config.ABOUT_MSG, reply_markup=back_button())
        elif query.data == "help":
            await query.message.edit_caption(caption=Config.HELP_MSG, reply_markup=back_button())
        elif query.data == "back":
            await query.message.edit_caption(caption=Config.START_MSG.format(user=query.from_user.mention), reply_markup=main_buttons())
        await query.answer()
    except MessageNotModified: pass

if __name__ == "__main__":
    keep_alive() # Starts Flask on Port 8000
    logging.info("Bot is starting...")
    bot.run()
