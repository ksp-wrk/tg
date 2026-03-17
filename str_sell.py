import time
import pickle
import os
import requests
import random
import shlex
import subprocess
from telethon.sync import TelegramClient, events, functions
from telethon.sessions import StringSession
from telethon.sessions.string import StringSession
import telethon.tl.types
#from telethon.tl.types import ChannelParticipantsPending
from datetime import datetime, timedelta

import crypter

#Telegram : 777000


api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'
pass_2fa = "542543"

TARGET_BOT = '@B172dhhsijsbwusi_bot'

cwd = os.getcwd()


def kill_others(client):
    me = client.get_me()
    print(f"{me.phone}_killing Sessions")
    GetSessions = client(functions.account.GetAuthorizationsRequest()) 

    if len(GetSessions.authorizations)>1:
        print("Another Session    :\tYes")
        for ss in GetSessions.authorizations:
            SessionHash = ss.hash
            SessionIp   = ss.country
            d_mdl       = ss.device_model
            
            print(f"{d_mdl}\n{str(SessionHash)}\n{str(SessionIp)}\n{ss.date_created}\n\n") 
            if SessionHash>0:
                result = client(functions.account.ResetAuthorizationRequest(hash=SessionHash))
                print(f"{d_mdl}   :\t {str(SessionIp)}")
        return False
    else:
        time.sleep(2)
        print("Another Session    :\tNo")
        return True

    


async def get_chat_message_count(chat_id):
    """Retrieves the total number of messages in a chat."""
    try:
        # Ensure chat_id is an integer
        if isinstance(chat_id, str):
            chat_id = int(chat_id)
        
        # Make the request to get the message count
        count = await client(GetChatMessageCountRequest(chat_id=chat_id))
        print(f"Total messages in chat {chat_id}: {count}")
        return count
    except Exception as e:
        print(f"Error getting message count: {e}")
        return None


mClient = TelegramClient('me', api_id, api_hash).start(max_attempts=10)
hn = mClient.get_me().id
print(hn)

ssn_for_sell = 0
ssn_for_sell = input(f'How many SSNs You Want to Sell? ')

all_ssns = []
for message in mClient.get_messages(2576914746, None):
    
    if (
          message.replies and
          hasattr(message.replies, 'replies') and
          message.replies.replies == 0 and
          message.message.startswith("880")
      ):
        #senderUID = mClient.get_entity(message.from_id.user_id).username
        #if (senderUID):
        #print( f"{message.text}" )
        num = message.text.split('\n\n')[0].replace("`", "")
        print(num)
        ssn = message.text.split('\n\n')[1].replace("`", "")
        print(ssn)
        if ssn.startswith("b'") and ssn.endswith("'"):
            ssn = ssn.replace("b'", "").replace("'", "")
        ssn = crypter.password_decrypt(ssn.encode(), 'KsP@542543').decode()
        all_ssns.append(ssn)

        client = TelegramClient(StringSession(ssn), api_id, api_hash).start(password=pass_2fa,max_attempts=10)
        cPhn = client.get_me().phone
        print(f"Logged in as : {cPhn}")

        if kill_others(client) == True:


            mClient.send_message(TARGET_BOT, "📤 ارسال اکانت")
            print("📤 Order sent")
            time.sleep(2)
            mClient.send_message(TARGET_BOT, message='+'+cPhn)
            login_detected = False

            
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
                        try:
                            await client.edit_2fa('542543')
                            print("2FA disabled successfully.")
                        except Exception as e:
                            print(f"An error occurred: {e}")

                    #await client.send_message('@k_ofcl', otp)
                    time.sleep(5)
                    await mClient.send_message(TARGET_BOT, otp)

                    if (
                        "logged in" in text.lower() or
                        "new login" in text.lower() or
                        "successfully logged in" in text.lower()
                    ):
                        login_detected = True
                    
                    if (
                        "two-step verification" in text.lower() or
                        "2-step verification" in text.lower()
                    ):
                        login_detected = True


                    if login_detected:
                        print("🚀 Done → Logging out")
                        await client.log_out()
                    
                    await client.disconnect()

                    
                    

                    #await client.log_out()


            client.run_until_disconnected()

            if login_detected == TRUE:
                msgID = message.id
                mClient.send_message(2576914746, message='Sold!!', reply_to=msgID)
                print(f"{num} SOLD successfully")
                login_detected = False
                print(f"{str(len(all_ssns))} Sessions are SOLD successfully")



            
            #msgID = message.id
            #mClient.send_message(2576914746, message='Sold!!', reply_to=msgID)
            #print(f"{num} SOLD successfully")
            #print(f"{str(len(all_ssns))} Sessions are SOLD successfully")
            
            time.sleep(5)
            if str(len(all_ssns)) == ssn_for_sell:
                exit()
        else:
            print(f"Other Logins Found. Skipping this")
        
print(f"{str(len(all_ssns))} All Sessions are SOLD successfully")
            
