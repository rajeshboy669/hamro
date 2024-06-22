import telegram.ext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import re
from pymongo.mongo_client import MongoClient
import requests
import string
import random
def end_gen(length):
    letters = string.ascii_lowercase+string.digits+string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str



uri = "mongodb+srv://aaroha:aaroha@cluster0.xfupmjy.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client['TeleUsers']
collection = db['TeleAuth']
# user login

def is_auth(uname):
    query = {"_id": uname}
    result = collection.find_one(query)
    return result

def login(uname, api_key):
    d_check=is_auth(uname)
    if d_check == None:
        document = {'_id': uname,'api_key': api_key}
        collection.insert_one(document)
        return True
    else:
        return False
    
def logout(uname):
    query={'_id': uname}
    result = collection.find_one(query)
    if result != None:
        collection.delete_one(query)
        return True
    else:
        return False

# link generator 
def link_gen(uname, long_link):
    if is_auth(uname) != None:
        query={"_id":uname}
        res=collection.find_one(query)
        api_key=res['api_key']
        url=f"https://ez4short.xyz/api?api={api_key}&url={long_link}&format=text"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        return response.text
    else:
        return "You haven't login Yet Please Login First"


def start(update,context):
    keyboard = [
                [InlineKeyboardButton("Sign Up", url="https://ez4short.xyz/auth/signup")],
                
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_reply_text = '''😋This bot will help you to Short Links from your ez4short.xyz Account.

If you don't have an active ez4short.xyz Account then Please register your account here ez4short.xyz/auth/signup
 
2️⃣How to Short Links? 
👉 After Logging in , Send any link which you want to Short. 
👉 You will get your Shortned Link immediately.

3️⃣How to Short Bulk links at a time? 
👉Send All the links which you want to short in below format 👇
https://loutube.co
https://google.com
https://ez4short.xyz
👉 Boom 💥 ! You will get all link shorten.

⚡️Still Have Doubts?
⚡️Want to Report Any Bug?
😌Send Here @EZ4short_support'''
    update.message.reply_text(message_reply_text, reply_markup=reply_markup)

def api_Login(update, context):
    user_rsp=update.message.text.split(" ")
    user = update.message.from_user
    username = user.username
    if len(user_rsp)==1:
        update.message.reply_text("Please send login api in format of /login 12590xxxxxxxx")
    elif len(user_rsp)==2:
        ser_rsp=login(username, user_rsp[1])
        if ser_rsp == True:
            update.message.reply_text(f"Welcome {username}, Now You Can Short Your Links")
        elif ser_rsp == False:
            update.message.reply_text("You are already logged in.")
        else:
            update.message.reply_text("Something Went Wrong")
    else:
        update.message.reply_text("Please send api in format /login 12590xxxxxxxx")

def help(update,context):
    keyboard = [
                [InlineKeyboardButton("Get Help", url="https://ez4short.xyz/member/forms/support")],
                
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_reply_text = 'Click on button to get help'
    update.message.reply_text(message_reply_text, reply_markup=reply_markup)

def feature(update, context):
    update.message.reply_text("""💠 Features Of ez4short.xyz bot 💠

❤️ It's AN AI Based User Friendly Bot ❤️

➡️ Use Can Short Bulk Links Into Your ez4short.xyz Account With This Bot""")

# Define a function to handle incoming messages
def handle_message(update, context):
    message = update.message
    r_message=message.text
    user = update.message.from_user
    username = user.username
    if message.photo:
        # Get the latest photo and its caption
        photo_file_id = message.photo[-1].file_id
        caption = message.caption
        links = re.findall(r'(https?://\S+)', caption)
        filtered_list = [link for link in links if "t.me" not in link]
        short_link=[]
        L=0
        for link in filtered_list:
            short_link.append(link_gen(username, link))
            caption = caption.replace(link, f"{short_link[L]}")
            L=L+1
        context.bot.send_photo(chat_id=message.chat_id, photo=photo_file_id, caption=caption)
    elif message.text:
        if "https//" in message.text or "http" in message.text:
            caption = message.text
            links = re.findall(r'(https?://\S+)', caption)
            filtered_list = [link for link in links if "t.me" not in link]
            short_link=[]
            L=0
            for link in filtered_list:
                short_link.append(link_gen(username, link))
                caption = caption.replace(link, f"{short_link[L]} ")
                L=L+1
            update.message.reply_text(caption)
        else:
            update.message.reply_text("Please Send me any link or Forward Whole Post")
    else:
        update.message.reply_text("Please Send me any link or Forward Whole Post")

def get_api(update,context):
    keyboard = [
                [InlineKeyboardButton("Get Token", url="ez4short.xyz/member/tools/api")],
                
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_reply_text = """• First Visit ez4short.xyz/member/tools/api
• Copy the API TOKEN and come back to Bot.
• Input  /token and Paste The token Copied from ez4short.xyz/member/tools/api
• Now bot will successfully connected to your  ez4short.xyz account."""
    update.message.reply_text(message_reply_text, reply_markup=reply_markup)

def api_Logout(update, context):
    user = update.message.from_user
    username = user.username
    resp=logout(username)
    if resp == True:
        update.message.reply_text("You are Logged Out SuccessFully")
    elif resp == False:
        update.message.reply_text("You Haven't Login Yet Please Login First")
    else:
        update.message.reply_text("Something Went Wrong")
# Set up the bot and its message handler
def main():
    bot = telegram.Bot("7064912106:AAH95CbvWSR77N5KdXNXN-d4wUs2gt1Ln8c")
    updater = telegram.ext.Updater(bot.token, use_context=True)
    disp = updater.dispatcher
    disp.add_handler(telegram.ext.CommandHandler('start',start))
    disp.add_handler(telegram.ext.CommandHandler('help',help))
    disp.add_handler(telegram.ext.CommandHandler('login',api_Login))
    disp.add_handler(telegram.ext.CommandHandler('get_api',get_api))
    disp.add_handler(telegram.ext.CommandHandler('logout',api_Logout))
    disp.add_handler(telegram.ext.CommandHandler('features',feature))
    disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.all, handle_message))
    updater.start_polling()

if __name__ == "__main__":
    main()
