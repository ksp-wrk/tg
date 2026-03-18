import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
import crypter
import re

api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'
botToken = '7678259114:AAEk9QF7FdxaN8MZ_9PN8SvYTswnigaPk3c'

bot_username = "@B172dhhsijsbwusi_bot"


def clean(txt):
    return re.sub(r'\s+', ' ', txt).strip()


async def get_me_ssn() -> str:
    print("s")
    async with TelegramClient('bot.session', api_id, api_hash) as bClient:
        await bClient.start(bot_token=botToken)
        me = await bClient.get_me()
        print("BOT USER:", me.username)
        
        message = await bClient.get_messages(2576914746, ids=1449)
        bClient.disconnect()

        num = message.text.split('\n\n')[0].replace("`", "")
        ssn = message.text.split('\n\n')[1].replace("`", "")

        if ssn.startswith("b'") and ssn.endswith("'"):
            ssn = ssn.replace("b'", "").replace("'", "")

        ssn = crypter.password_decrypt(ssn.encode(), 'KsP@542543').decode()
        return ssn or ""


async def main():
    ssn_main = await get_me_ssn()
    print("SESSION:", ssn_main)
    
    client = TelegramClient(StringSession(ssn_main), api_id, api_hash)
    await client.start()

    bot = await client.get_entity(bot_username)

    print("Fetching messages...")
    messages = await client.get_messages(bot, limit=50)

    print(f"Total messages fetched: {len(messages)}")

    TARGET_BUTTON_RAW = "‎تایید اکانت ☑️"
    TARGET_BUTTON = clean(TARGET_BUTTON_RAW)

    print("TARGET (repr):", repr(TARGET_BUTTON_RAW))
    print("TARGET CLEAN:", repr(TARGET_BUTTON))
    print("="*50)

    found_any = False

    for i, msg in enumerate(messages):
        print(f"\n--- Message #{i} ---")

        if not msg.buttons:
            print("No buttons")
            continue

        print("Buttons found!")

        for r, row in enumerate(msg.buttons):
            for c, btn in enumerate(row):
                try:
                    print(f"[Row {r} Col {c}]")
                    print("BTN TEXT:", btn.text)
                    print("BTN REPR:", repr(btn.text))
                    print("BTN CLEAN:", repr(clean(btn.text)))

                    if btn.text and clean(btn.text) == TARGET_BUTTON:
                        print(">>> MATCH FOUND! CLICKING...")
                        await msg.click(text=btn.text)
                        found_any = True
                        await asyncio.sleep(2)
                    else:
                        print("Not matched")

                    print("-"*30)

                except Exception as e:
                    print("Error:", e)

    if not found_any:
        print("\n❌ No matching button found!")

    print("\nDONE. Script will exit now.")
    await client.disconnect()


asyncio.run(main())
