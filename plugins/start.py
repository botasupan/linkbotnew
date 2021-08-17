#(©)Codexbotz

import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, START_MSG, OWNER_ID, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON
from helper_func import subscribed, encode, decode, get_messages

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Sabar ya...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Terjadi masalah..!")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = 'html', reply_markup = reply_markup)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = 'html', reply_markup = reply_markup)
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔑 𝗢𝗣𝗘𝗡", callback_data = "about"),
                    InlineKeyboardButton("🔒 𝗖𝗟𝗢𝗦𝗘", callback_data = "close")
                ],[
                    InlineKeyboardButton("📥 𝐕𝐈𝐃𝐄𝐎 𝐕𝐈𝐑𝐀𝐋", url="https://t.me/bokepviralindonesia_terbaru")
                  ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    text = "<b>Anda harus JOIN Channel/Group terlebih dahulu untuk menggunakan BOT ini.\n\nKalau belum JOIN, BOT tidak akan menampilkan Video. Jika sudah JOIN, silahkan klik GET FILE</b>"
    message_text = message.text
    try:
        command, argument = message_text.split()
        text = text + f"<a href='https://t.me/{client.username}?start={argument}'></a>"
    except ValueError:
        pass
    reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔞 JOIN HERE 🔞", url = client.invitelink),
                ],[
                    InlineKeyboardButton("🔄 GET FILE", url = f'https://t.me/{client.username}?start={argument}')
                  ]
            ]
        )
   
    await message.reply(
        text = text,
        reply_markup = reply_markup,
        quote = True,
        disable_web_page_preview = True
    )
