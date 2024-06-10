from pymongo.mongo_client import MongoClient
import requests

uri = "mongodb+srv://realaaroha:realaaroha@cluster0.6jc4x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

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
        url=f"https://xtshort.com/api?api={api_key}&url={long_link}&format=text"
        headers = {
  "User-Agent": "Mozilla/5.0+(compatible; UptimeRobot/2.0; http://www.uptimerobot.com/)",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "Accept-Language": "en-US,en;q=0.8",
  "Connection": "close",
  "cache-control": "no-cache",
  "Referer": "https://hamro.onrender.com",
  "Accept-encoding": ""
        }

        response = requests.get(url, headers=headers)
        return response.text
    else:
        return "You haven't login Yet Please Login First"
