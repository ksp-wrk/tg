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
    if not txt:
        return ""
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

    print("\nFetching messages...\n")
    messages = await client.get_messages(bot, limit=50)

    print(f"📨 Total messages fetched: {len(messages)}")

    TARGET_KEYWORDS = [
        "اکانت با شماره",
        "جهت تایید اکانت"
    ]

    TARGET_BUTTON = clean("‎تایید اکانت ☑️")

    total_buttons = 0
    matched_messages = 0
    clicked = 0

    print("\n================ DEBUG START ================\n")

    for i, msg in enumerate(messages):
        print(f"\n🔹 Message #{i}")

        if not msg.text:
            print("No text")
            continue

        print("TEXT:", msg.text[:100])

        # ✅ message match
        if all(k in msg.text for k in TARGET_KEYWORDS):
            print("✅ TARGET MESSAGE MATCHED")
            matched_messages += 1

            if not msg.buttons:
                print("❌ No buttons in this message")
                print("RAW BUTTONS:", msg.buttons)
                continue

            print("✅ Buttons found!")

            for r, row in enumerate(msg.buttons):
                for c, btn in enumerate(row):
                    total_buttons += 1

                    print(f"\n   ➤ Button [{r},{c}]")
                    print("   TEXT:", btn.text)
                    print("   REPR:", repr(btn.text))
                    print("   CLEAN:", clean(btn.text))

                    # 🔥 TRY 1: exact text match
                    try:
                        if clean(btn.text) == TARGET_BUTTON:
                            print("   🎯 MATCHED TARGET BUTTON!")
                            await msg.click(text=btn.text)
                            print("   ✅ CLICKED (text match)")
                            clicked += 1
                            await asyncio.sleep(2)
                            continue
                    except Exception as e:
                        print("   ❌ Text click error:", e)

                    # 🔥 TRY 2: click by index
                    try:
                        print("   ⚡ Trying index click...")
                        await msg.click(r, c)
                        print("   ✅ CLICKED (index)")
                        clicked += 1
                        await asyncio.sleep(2)
                        continue
                    except Exception as e:
                        print("   ❌ Index click error:", e)

                    # 🔥 TRY 3: first button fallback
                    try:
                        print("   ⚡ Trying fallback click(0)...")
                        await msg.click(0)
                        print("   ✅ CLICKED (fallback)")
                        clicked += 1
                        await asyncio.sleep(2)
                        continue
                    except Exception as e:
                        print("   ❌ Fallback error:", e)

        else:
            print("Not target message")

    print("\n================ SUMMARY ================\n")
    print(f"Matched messages: {matched_messages}")
    print(f"Total buttons seen: {total_buttons}")
    print(f"Total clicks done: {clicked}")

    print("\nDONE. Script exiting.\n")

    await client.disconnect()


asyncio.run(main())
