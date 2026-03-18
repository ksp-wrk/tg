from telethon import TelegramClient, events
from telethon.tl.types import (
    ReplyKeyboardMarkup, 
    KeyboardButtonRow, 
    KeyboardButtonRequestPhone,
    ReplyKeyboardHide
)

# আপনার API ID, Hash এবং Token এখানে দিন
api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'
bot_token = '7678259114:AAEk9QF7FdxaN8MZ_9PN8SvYTswnigaPk3c' # buy-sell # Get this from BotFather


client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    # সরাসরি RequestPhone বাটন তৈরি করা
    button = KeyboardButtonRequestPhone(text="আমার ফোন নম্বর দিন")
    
    # বাটনটিকে একটি কিবোর্ড লেআউটে সাজানো
    keyboard = ReplyKeyboardMarkup(
        rows=[KeyboardButtonRow(buttons=[button])],
        resize=True,
        single_use=True
    )
    
    await event.respond("দয়া করে নিচের বাটনে ক্লিক করে আপনার নম্বর শেয়ার করুন:", buttons=keyboard)



@client.on(events.NewMessage(func=lambda e: e.contact))
async def contact_handler(event):
    phone = event.message.contact.phone_number
    sender = await event.get_sender()
    await event.respond(
        f"✅ Thanks {sender.first_name}!\n\n"
        f"Your number is: {phone}"
    )
    
print("বটটি চলছে...")
client.run_until_disconnected()
