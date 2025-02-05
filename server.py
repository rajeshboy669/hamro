import os
import asyncio
import logging
import requests
import re
import string
import random
from flask import Flask, request
from pymongo import MongoClient
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Load Bot Token and MongoDB URI from Environment Variables
TOKEN = os.getenv("BOT_TOKEN", "7754090875:AAFvORs24VyZojKEqoNoX4nD6kfYZOlzbW8")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://aaroha:aaroha@<hostname>/?ssl=true&replicaSet=atlas-dut4lu-shard-0&authSource=admin&retryWrites=true&w=majority")

# Setup Flask App
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['TeleUsers']
collection = db['TeleAuth']

def is_auth(uname):
    return collection.find_one({"_id": uname})

def login(uname, api_key):
    if is_auth(uname) is None:
        collection.insert_one({'_id': uname, 'api_key': api_key})
        return True
    return False

def logout(uname):
    result = collection.find_one({"_id": uname})
    if result:
        collection.delete_one({"_id": uname})
        return True
    return False

def link_gen(uname, long_link):
    user_data = is_auth(uname)
    if user_data:
        api_key = user_data['api_key']
        url = f"https://ez4short.xyz/api?api={api_key}&url={long_link}&format=text"
        response = requests.get(url)
        return response.text
    return "You haven't logged in yet. Please login first."

async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Sign Up", url="https://ez4short.xyz/auth/signup")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = "😋 This bot helps you shorten links using your ez4short.xyz account. Register here: https://ez4short.xyz/auth/signup"
    await update.message.reply_text(message, reply_markup=reply_markup)

async def api_login(update: Update, context: CallbackContext):
    user_rsp = update.message.text.split(" ")
    username = update.message.from_user.username
    if len(user_rsp) == 2:
        if login(username, user_rsp[1]):
            await update.message.reply_text(f"Welcome {username}, you can now shorten links!")
        else:
            await update.message.reply_text("You are already logged in.")
    else:
        await update.message.reply_text("Use format: /login YOUR_API_KEY")

async def api_logout(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    if logout(username):
        await update.message.reply_text("Successfully logged out.")
    else:
        await update.message.reply_text("You haven't logged in yet.")

async def handle_message(update: Update, context: CallbackContext):
    message = update.message.text
    username = update.message.from_user.username
    links = re.findall(r'(https?://\S+)', message)
    short_links = [link_gen(username, link) for link in links]
    if short_links:
        await update.message.reply_text("\n".join(short_links))
    else:
        await update.message.reply_text("Send a valid link to shorten.")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("login", api_login))
app.add_handler(CommandHandler("logout", api_logout))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json()
    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
