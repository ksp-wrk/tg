import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'
botToken = '7753879828:AAHcGFNikwY6clhpXJx345rgTlP6z9AvMUA' # master

bot_username = "YOUR_BOT_USERNAME"  # example: @abc_bot

async def get_me_ssn(group_id: int, message_id: int) -> str:
    """
    নির্দিষ্ট গ্রুপের নির্দিষ্ট মেসেজের টেক্সট রিটার্ন করে
    """
    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        await client.start(bot_token=botToken)
        message = await client.get_messages(group_id, ids=message_id)
        return message.text or ""  # যদি মেসেজ খালি থাকে, তাহলে "" রিটার্ন করবে



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
