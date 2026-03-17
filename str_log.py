
import asyncio
import crypter
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
from telethon.tl.functions.messages import SendReactionRequest, GetHistoryRequest
from telethon.tl.functions.channels import JoinChannelRequest, GetParticipantRequest
from telethon.errors import UserNotParticipantError
from telethon.tl.types import ReactionEmoji
#from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.errors import UserAlreadyParticipantError
import telethon.tl.types
#from telethon.tl.types import ChannelParticipantsPending
from datetime import datetime, timedelta


#Telegram : 777000


api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'
phn = "+8801778855999"
pswd = "khALid@542543"
pass_2fa = "542543"

cwd = os.getcwd()


async def fetch_entity(client, username):
    try:
        return await client.get_entity(username)
    except UserNotParticipantError:
        return await client(JoinChannelRequest(username))
    except Exception as e:
        if "private" in str(e).lower():
            raise ValueError("❌ Cannot use private channels.")
        raise

async def react_to_post(client, channel, msg_id, emoji, proxy=None):
    try:
        entity = await fetch_entity(client, channel)
        await client.get_messages(entity, ids=msg_id)
        await client(SendReactionRequest(
            peer=entity,
            msg_id=msg_id,
            reaction=[ReactionEmoji(emoticon=emoji)],
            big=True
        ))
        return True
    except Exception as e:
        print(f"❌ {e}")
        return False

async def random_delay(min_sec: int = 2, max_sec: int = 5):
    delay = random.uniform(min_sec, max_sec)
    print(f"⏳ Waiting for {delay:.2f} seconds...")
    await asyncio.sleep(delay)

async def safe_join_channel(client, channel_username, min_delay=3, max_delay=9):
    try:
        # Check if already joined
        try:
            entity = await client.get_entity(channel_username)
            await client(GetParticipantRequest(channel=entity, participant='me'))
            print(f"✅ Already in @{channel_username}")
        except UserNotParticipantError:
            # Not a member, so try joining
            await client(JoinChannelRequest(channel_username))
            print(f"➕ Joined @{channel_username}")
        except Exception as e:
            print(f"⚠️ Unknown membership check error: {e}")
            return

        # Optional delay after join
        delay = random.randint(min_delay, max_delay)
        print(f"⏳ Delay: {delay}s")
        await asyncio.sleep(delay)

    except Exception as e:
        print(f"❌ Error joining channel: {e}")


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


username = 'https://t.me/mktwnews'

REACTION_LIST = ['❤️', '🔥', '😍', '😢', '👍']

all_ssns = []
async def main():
    
    mClient = TelegramClient('me', api_id, api_hash)
    await mClient.start(phone='+8801778855999',password=pswd,max_attempts=10)
    hn = await mClient.get_me()
    print(hn.id)
    for message in await mClient.get_messages(2576914746, None):
        
        if (
            message.replies and
            hasattr(message.replies, 'replies') and
            message.replies.replies == 0 and
            message.message.startswith("880")
        ):
            #senderUID = mClient.get_entity(message.from_id.user_id).username
            #if (senderUID):
            #print( f"{message.text}\n\n\n\n" )
            num = message.text.split('\n\n')[0].replace("`", "")
            print(num)
            ssn = message.text.split('\n\n')[1].replace("`", "")
            
            print(ssn)
            if ssn.startswith("b'") and ssn.endswith("'"):
                ssn = ssn.replace("b'", "").replace("'", "")
            ssn = crypter.password_decrypt(ssn.encode(), 'KsP@542543').decode()
            all_ssns.append(ssn)

            client = TelegramClient(StringSession(ssn), api_id, api_hash)
            await client.start(password=pass_2fa,max_attempts=10)
            cPhn = await client.get_me()
            print(f"Logged in as : {cPhn.phone}")
            
            #await random_delay(3, 8)
            
            await safe_join_channel(client, username)

            try:
                entity = await fetch_entity(client, username)
                #history = await client(GetHistoryRequest(peer=entity, limit='10', offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
                                
                history = await client(GetHistoryRequest(
                    peer=entity,
                    offset_id=0,
                    offset_date=None,     # ✅ This was missing
                    add_offset=0,
                    limit=10,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))

                posts = [msg.id for msg in history.messages]
            except Exception as e:
                print(f"❌ Channel error: {e}")
                continue
            
            for post_id in posts:
                emoji = random.choice(REACTION_LIST)
                await react_to_post(client, username, post_id, emoji)
            
            print(f"  {str(len(all_ssns))} Sessions are Checked")
            
            await client.disconnect()
            #dialogs = client.get_dialogs()
            #for d in dialogs:
                #print("\t", d.title, ":", d.entity.id)

                    
            #kill_others(client)
            #f_nm_cng(client)
            #print(os.path.join(cwd, file))
            
    print(f"{str(len(all_ssns))} All Sessions are Checked successfully")
    exit()


if __name__ == "__main__":
    asyncio.run(main())

