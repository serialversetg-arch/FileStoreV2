import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from config import *

@Client.on_message(filters.private & filters.incoming)
async def forcesub(c, m):
    # Agar Admin message kar raha hai toh FSub skip karo
    if m.from_user.id == int(OWNER_ID):
        return await m.continue_propagation()

    if UPDATE_CHANNEL:
        try:
            # STATUS CHECK: Sabse important step
            user = await c.get_chat_member(UPDATE_CHANNEL, m.from_user.id)
            
            # Agar user joined hai (Member/Admin/Owner), toh aage badhne do
            if user.status in ["member", "administrator", "creator"]:
                return await m.continue_propagation()
                
            # Agar user banned hai
            if user.status == "banned":
                await m.reply_text("**Hey, you are banned from using me! 😜**", quote=True)
                return

        except UserNotParticipant:
            # YE TABHI CHALEGA JAB USER JOINED NAHI HOGA
            buttons = [[InlineKeyboardButton(text='Updates Channel 🔖', url=f"https://t.me/{UPDATE_CHANNEL}")]]
            
            # Smart Refresh Button: Sirf tab dikhao jab banda link se aaya ho
            if m.text and len(m.text.split()) > 1 and 'start' in m.text:
                data = m.text.split()[1]
                buttons.append([InlineKeyboardButton('🔄 Refresh', callback_data=f'refresh#{data}')])
            
            await m.reply_text(
                f"Hey {m.from_user.mention} 👋\n\n"
                "**You must join my updates channel to use me!**\n\n"
                "__Press the button below to join now 👇__",
                reply_markup=InlineKeyboardMarkup(buttons),
                quote=True
            )
            return
        except Exception as e:
            # Agar koi aur error aaye (jaise bot admin na ho)
            print(f"FSub Error: {e}")
            return await m.continue_propagation()
    
    await m.continue_propagation()

@Client.on_callback_query(filters.regex('^refresh'))
async def refresh_cb(c, m):
    data = m.data.split("#")[1]
    try:
        user = await c.get_chat_member(UPDATE_CHANNEL, m.from_user.id)
        if user.status in ["member", "administrator", "creator"]:
            # Agar ab joined hai, toh use start message pe bhej do
            await m.message.delete()
            # Redirect to start with data
            return await c.send_message(
                m.from_user.id, 
                f"/start {data}"
            )
        else:
            await m.answer('You are still not joined! 😐', show_alert=True)
    except UserNotParticipant:
        await m.answer('Join the channel first! 🧐', show_alert=True)
    except Exception as e:
        print(f"Refresh Error: {e}")
