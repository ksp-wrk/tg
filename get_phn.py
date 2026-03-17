from telethon import TelegramClient, events
from telethon.tl.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Replace with your own API ID and API hash from my.telegram.org
api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'
bot_token = '7678259114:AAEk9QF7FdxaN8MZ_9PN8SvYTswnigaPk3c' # buy-sell # Get this from BotFather

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/request_phone'))
async def request_phone(event):
    """Sends a message with a button to request the user's phone number."""
    # Create a custom keyboard with a request_contact button
    button = KeyboardButton.with_request_contact("Share my phone number")
    keyboard = ReplyKeyboardMarkup([[button]], resize=True, one_time_keyboard=True)
    
    await event.respond("Please share your phone number using the button below:", buttons=keyboard)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    """Handles the shared contact message."""
    if event.message.contact:
        # Check if the contact belongs to the user who sent it
        if event.message.contact.user_id == event.message.sender_id:
            phone_number = event.message.contact.phone_number
            await event.respond(f"Thank you! Your phone number is: {phone_number}", buttons=ReplyKeyboardRemove())
        else:
            await event.respond("That doesn't seem to be your phone number. Please use the button.")

def main():
    print("Bot is running...")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
