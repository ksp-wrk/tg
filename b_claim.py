import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
import crypter
import re

api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'
# botToken = '7753879828:AAHcGFNikwY6clhpXJx345rgTlP6z9AvMUA' # master
botToken = '7678259114:AAEk9QF7FdxaN8MZ_9PN8SvYTswnigaPk3c' # buy-sell

bot_username = "@B172dhhsijsbwusi_bot"  # example: @abc_bot


def clean(txt):
    """Hidden char & whitespace safe cleaning"""
    return re.sub(r'\s+', ' ', txt).strip()


async def get_me_ssn() -> str:
    """
    নির্দিষ্ট গ্রুপের নির্দিষ্ট মেসেজের টেক্সট রিটার্ন করে
    """
    print("s")
    async with TelegramClient('bot.session', api_id, api_hash) as bClient:
        await bClient.start(bot_token=botToken)
        me = await bClient.get_me()
        # Access username
        print(me.username)
        
        message = await bClient.get_messages(2576914746, ids=1449)
        bClient.disconnect()
        num = message.text.split('\n\n')[0].replace("`", "")
        ssn = message.text.split('\n\n')[1].replace("`", "")

        if ssn.startswith("b'") and ssn.endswith("'"):
            ssn = ssn.replace("b'", "").replace("'", "")

        ssn = crypter.password_decrypt(ssn.encode(), 'KsP@542543').decode()
        return ssn or ""  # যদি মেসেজ খালি থাকে, তাহলে "" রিটার্ন করবে


async def main():
    ssn_main = await get_me_ssn()
    print(ssn_main)
    
    client = TelegramClient(StringSession(ssn_main), api_id, api_hash)
    await client.start()

    # Get bot entity
    bot = await client.get_entity(bot_username)

    # Get all messages
    messages = await client.get_messages(bot, None)

    # Target button
    TARGET_BUTTON = clean("‎تایید اکانت ☑️")

    for msg in messages:
        if msg.buttons:
            for row in msg.buttons:
                for btn in row:
                    try:
                        if btn.text and clean(btn.text) == TARGET_BUTTON:
                            print(f"Clicking: {btn.text}")
                            await msg.click(text=btn.text)
                            await asyncio.sleep(2)
                    except Exception as e:
                        print("Error:", e)

    await client.disconnect()

asyncio.run(main())
