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


api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'

mClient = TelegramClient('me', api_id, api_hash)
mClient.start(phone='+8801778855999',password="khALid@542543",max_attempts=10)

inp = input("id: ")
print(mClient.get_entity(inp))