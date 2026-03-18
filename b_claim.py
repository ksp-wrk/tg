import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = 123456
api_hash = "your_api_hash"
session = "your_string_session"

bot_username = "YOUR_BOT_USERNAME"  # example: @abc_bot

async def main():
    client = TelegramClient(StringSession(session), api_id, api_hash)
    await client.start()

    # Get bot entity
    bot = await client.get_entity(bot_username)

    # Get last messages
    messages = await client.get_messages(bot, limit=5)

    for msg in messages:
        if msg.buttons:
            print("Found buttons!")

            for row in msg.buttons:
                for btn in row:
                    try:
                        print(f"Clicking: {btn.text}")
                        await msg.click(text=btn.text)
                        await asyncio.sleep(2)  # delay প্রয়োজন
                    except Exception as e:
                        print("Error:", e)

    await client.disconnect()

asyncio.run(main())
