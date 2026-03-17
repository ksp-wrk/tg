# telegram_viewer_bot.py

# telegram_viewer_bot_final.py

import os
import sys
import subprocess
import importlib.util
import asyncio
import json
import random
import re
from datetime import datetime, timedelta

# Auto install required packages
REQUIRED = ['telethon', 'python-telegram-bot[job-queue]', 'pysocks', 'nest_asyncio']
for pkg in REQUIRED:
    pip_name = pkg
    if '[' in pkg:
        pip_name = pkg.split('[')[0]
    if importlib.util.find_spec(pip_name.replace('-', '_')) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import SendReactionRequest, GetHistoryRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import ReactionEmoji
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import crypter
import nest_asyncio
nest_asyncio.apply()

# ========== CONFIG ==========
API_ID = 16017675
API_HASH = '898e9db01786302c9f95f67c23d9fecb'
BOT_TOKEN = '7753879828:AAHcGFNikwY6clhpXJx345rgTlP6z9AvMUA' # master

SESSIONS_FILE = 'sessions.txt'
PROXY_FILE = 'proxies.json'
APPROVAL_FILE = 'approvals.json'
VIEWED_FILE = 'viewed.json'
SESSION_CACHE = 'session_cache.json'

GROUP_ID = 2576914746  # Session storage group
MANDATORY_GROUPS = [2415019283]
MANDATORY_CHANNELS = [2282561371]
ADMIN_IDS = [7032729089]

POST_EXPIRY_DAYS = 5
SESSION_PROXY_LIMIT = 5
REACTION_LIST = ['❤️', '🔥', '😍', '😢', '👍']
# ============================

def load_json(file, default):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump(default, f)
    with open(file, 'r') as f:
        return json.load(f)

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)

def load_proxies():
    if not os.path.exists(PROXY_FILE):
        return []
    try:
        data = load_json(PROXY_FILE, [])
        return data if isinstance(data, list) and data else []
    except:
        return []

def assign_proxies(sessions, proxies):
    assignment = {}
    if not proxies:
        for sess in sessions:
            assignment[sess] = None
        return assignment

    usage = {}
    for sess in sessions:
        valid = [p for p in proxies if usage.get(p['addr'], 0) < SESSION_PROXY_LIMIT]
        proxy = random.choice(valid) if valid else None
        if proxy:
            usage[proxy['addr']] = usage.get(proxy['addr'], 0) + 1
        assignment[sess] = proxy
    return assignment

def load_sessions():
    cache = load_json(SESSION_CACHE, {})
    client = TelegramClient('me', API_ID, API_HASH)
    client.connect()
    messages = client.iter_messages(GROUP_ID, limit=None)
    new_sessions = []

    for msg in messages:
        matches = re.findall(r'`([^`]+)`', msg.text or '')
        if len(matches) >= 2:
            phone, encrypted = matches[0], matches[1]
            if phone not in cache:
                try:
                    decrypted = crypter.password_decrypt(encrypted.encode(), 'KsP@542543').decode()
                    cache[phone] = msg.id
                    new_sessions.append(decrypted)
                except Exception as e:
                    print(f"❌ Decryption failed for {phone}: {e}")

    save_json(SESSION_CACHE, cache)

    if new_sessions:
        with open(SESSIONS_FILE, 'a') as f:
            for s in new_sessions:
                f.write(s + '\n')

    return [line.strip() for line in open(SESSIONS_FILE) if line.strip()]

async def fetch_entity(client, username):
    try:
        return await client.get_entity(username)
    except UserNotParticipantError:
        return await client(JoinChannelRequest(username))
    except Exception as e:
        if "private" in str(e).lower():
            raise ValueError("❌ Cannot use private channels.")
        raise

async def react_to_post(session, channel, msg_id, emoji, proxy=None):
    try:
        client = TelegramClient(StringSession(session), API_ID, API_HASH, proxy=proxy)
        await client.start()
        entity = await fetch_entity(client, channel)
        await client.get_messages(entity, ids=msg_id)
        await client(SendReactionRequest(
            peer=entity,
            msg_id=msg_id,
            reaction=[ReactionEmoji(emoticon=emoji)],
            big=True
        ))
        await client.disconnect()
        return True
    except Exception as e:
        print(f"❌ {e}")
        return False

async def hourly_viewer(context: ContextTypes.DEFAULT_TYPE):
    sessions = load_sessions()
    proxies = load_proxies()
    approvals = load_json(APPROVAL_FILE, {})
    viewed = load_json(VIEWED_FILE, {})
    assignments = assign_proxies(sessions, proxies)
    now = datetime.now().timestamp()
    for key, val in approvals.items():
        if not val['approved']:
            continue
        username, count = val['username'], val['count']
        try:
            temp = TelegramClient(StringSession(sessions[0]), API_ID, API_HASH)
            await temp.start()
            entity = await fetch_entity(temp, username)
            history = await temp(GetHistoryRequest(peer=entity, limit=count, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
            posts = [msg.id for msg in history.messages]
            await temp.disconnect()
        except Exception as e:
            print(f"❌ Channel error: {e}")
            continue
        for i, session in enumerate(sessions):
            sid = f"sess_{i}"
            if sid not in viewed: viewed[sid] = []
            for post_id in posts:
                if any(v[0] == post_id for v in viewed[sid]):
                    continue
                emoji = random.choice(REACTION_LIST)
                if await react_to_post(session, username, post_id, emoji, assignments.get(session)):
                    viewed[sid].append([post_id, now])
    cutoff = (datetime.now() - timedelta(days=POST_EXPIRY_DAYS)).timestamp()
    for k in viewed:
        viewed[k] = [v for v in viewed[k] if v[1] > cutoff]
    save_json(VIEWED_FILE, viewed)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    for g in MANDATORY_CHANNELS + MANDATORY_GROUPS:
        try:
            m = await context.bot.get_chat_member(g, user)
            if m.status not in ['member', 'creator', 'administrator']:
                await update.message.reply_text("🚫 Join required groups/channels first.")
                return
        except:
            await update.message.reply_text("🚫 Cannot verify group/channel access.")
            return
    await update.message.reply_text("✅ Viewer bot ready!")

async def submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /submit <channel> <count>")
        return
    username = context.args[0].replace('@', '')
    count = int(context.args[1]) if len(context.args) > 1 else 5
    key = f"{username}_{update.effective_user.id}"
    approvals = load_json(APPROVAL_FILE, {})
    try:
        test = TelegramClient(StringSession(), API_ID, API_HASH)
        await test.connect()
        await fetch_entity(test, username)
        await test.disconnect()
    except Exception as e:
        await update.message.reply_text(str(e))
        return
    approvals[key] = {"username": username, "count": count, "approved": update.effective_user.id in ADMIN_IDS}
    save_json(APPROVAL_FILE, approvals)
    await update.message.reply_text("✅ Submitted for approval." if update.effective_user.id not in ADMIN_IDS else "✅ Auto-approved.")

load_sessions()
"""
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("submit", submit))
    app.job_queue.run_repeating(hourly_viewer, interval=3600, first=10)
    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
"""