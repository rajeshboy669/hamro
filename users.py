from pymongo.mongo_client import MongoClient
import requests

uri = "mongodb+srv://realaaroha:realaaroha@cluster0.jxsimkw.mongodb.net/?retryWrites=true&w=majority"

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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json",
    
}

        response = requests.get(url, headers=headers)
        return response.text
    else:
        return "You haven't login Yet Please Login First"
