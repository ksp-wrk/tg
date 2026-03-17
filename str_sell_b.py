import time
import asyncio
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
import crypter

# ================= CONFIG =================
api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'
pswd = "khALid@542543"
pass_2fa = "542543"

TARGET_BOT = '@B172dhhsijsbwusi_bot'
SOURCE_CHAT = 2576914746
# ==========================================

mClient = TelegramClient('me', api_id, api_hash).start(password=pswd)

# ================= 🔥 SESSION CLEAN (UPDATED) =================
def kill_others(client):
    try:
        sessions = client(functions.account.GetAuthorizationsRequest())
        total = len(sessions.authorizations)

        if total > 1:
            print(f"⚠️ Multiple sessions found: {total} → cleaning...")

            # নিজেরটা রেখে বাকিগুলো kill
            for s in sessions.authorizations:
                if not s.current:
                    try:
                        client(functions.account.ResetAuthorizationRequest(hash=s.hash))
                    except Exception as e:
                        print(f"❌ Failed to kill session: {e}")

            # 🔁 আবার check
            time.sleep(2)
            sessions = client(functions.account.GetAuthorizationsRequest())
            total_after = len(sessions.authorizations)

            if total_after > 1:
                print(f"❌ Still multiple sessions ({total_after}) → skipping")
                return False
            else:
                print("✅ Other sessions removed")

        return True

    except Exception as e:
        print(f"❌ Session check error: {e}")
        return False


# ================= GLOBAL STATE =================
otp_sent_set = set()


# ================= MAIN =================
ssn_for_sell = input("How many SSNs You Want to Sell? ")
all_ssns = []

messages = mClient.get_messages(SOURCE_CHAT, None)

for message in messages:
    if (
        message.replies and
        hasattr(message.replies, 'replies') and
        message.replies.replies == 0 and
        message.message.startswith("880")
    ):

        num = message.text.split('\n\n')[0].replace("`", "")
        ssn = message.text.split('\n\n')[1].replace("`", "")

        if ssn.startswith("b'") and ssn.endswith("'"):
            ssn = ssn.replace("b'", "").replace("'", "")

        ssn = crypter.password_decrypt(ssn.encode(), 'KsP@542543').decode()
        all_ssns.append(ssn)

        # ================= 🔥 LOGIN FIXED =================
        try:
            temp_client = TelegramClient(StringSession(ssn), api_id, api_hash)
            temp_client.connect()

            if not temp_client.is_user_authorized():
                print(f"❌ Session invalid → {num}")
                temp_client.disconnect()
                continue

            me = temp_client.get_me()
            cPhn = me.phone if me and me.phone else num

            print(f"📱 Trying: +{cPhn}")

            temp_client.disconnect()

        except Exception as e:
            print(f"❌ Session load error → {num} | {e}")
            continue

        client = TelegramClient(StringSession(ssn), api_id, api_hash)

        try:
            client.connect()

            if not client.is_user_authorized():
                print(f"❌ Skip (dead session): +{cPhn}")
                client.disconnect()
                continue

        except Exception as e:
            print(f"❌ Login error → +{cPhn} | {e}")
            try:
                client.disconnect()
            except:
                pass
            continue

        print(f"✅ Logged in: +{cPhn}")

        # ================= 🔥 SESSION CHECK =================
        if not kill_others(client):
            client.disconnect()
            continue

        # ================= STATE =================
        state = {
            "otp_sent": False,
            "login_detected": False,
            "number_requested": False
        }

        # ================= BOT HANDLER =================
        async def bot_handler(event):
            text = event.raw_text

            if "لطفا شماره مجازی خود را" in text and not state["number_requested"]:
                print("📱 Sending number...")
                await mClient.send_message(TARGET_BOT, '+' + cPhn)
                state["number_requested"] = True

        # ================= OTP HANDLER =================
        async def otp_handler(event):
            text = event.raw_text
            print("📩 777000:", text)

            if not state["number_requested"]:
                return

            if text.startswith("Login code:") and not state["otp_sent"]:

                if cPhn in otp_sent_set:
                    return

                otp = text.replace("Login code: ", "").split('.')[0]
                print(f"🔑 OTP: {otp}")

                try:
                    result = await client(functions.account.GetPasswordRequest())
                    if result.has_password:
                        print("🔐 Disabling 2FA...")
                        await client.edit_2fa(pass_2fa)
                        print("✅ 2FA disabled")
                except Exception as e:
                    print(f"❌ 2FA error: {e}")

                await mClient.send_message(TARGET_BOT, otp)

                state["otp_sent"] = True
                otp_sent_set.add(cPhn)

            if (
                "logged in" in text.lower() or
                "new login" in text.lower() or
                "successfully logged in" in text.lower()
            ):
                state["login_detected"] = True

            if (
                "two-step verification" in text.lower() or
                "2-step verification" in text.lower()
            ):
                state["login_detected"] = True

            if state["otp_sent"] and state["login_detected"]:
                print("🚀 Done → Logging out")

                await client.log_out()
                await client.disconnect()

        # ================= ADD HANDLERS =================
        mClient.add_event_handler(
            bot_handler,
            events.NewMessage(incoming=True, chats=TARGET_BOT)
        )

        client.add_event_handler(
            otp_handler,
            events.NewMessage(incoming=True, chats=777000)
        )

        # ================= START BOT =================
        mClient.send_message(TARGET_BOT, "📤 ارسال اکانت")
        print("📤 Order sent")

        # ================= RUN =================
        try:
            client.run_until_disconnected()
        except:
            pass

        # ================= CLEAN HANDLERS =================
        mClient.remove_event_handler(bot_handler)
        client.remove_event_handler(otp_handler)

        # ================= MARK SOLD =================
        mClient.send_message(SOURCE_CHAT, 'Sold!!', reply_to=message.id)

        print(f"💰 {num} SOLD")
        print(f"📊 Total sold: {len(all_ssns)}")

        time.sleep(5)

        if str(len(all_ssns)) == ssn_for_sell:
            break

print("✅ All Done")
