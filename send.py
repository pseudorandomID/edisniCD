import requests
import pymongo
import argparse
import sys, time

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', help='Bot Token')
    parser.add_argument('--chatid', help='chat_id')
    errMsg = "--token, --chatid"
    args = parser.parse_args()
    return (lambda x: x if (x.token is not None and x.chatid is not None) 
            else sys.exit(errMsg))(args)

if __name__=="__main__":
    args = parseArgs()
    botToken, chat_id = args.token, args.chatid

    dbClient = pymongo.MongoClient("mongodb://localhost:27017/")
    dcDB = dbClient["dc"]
    postsCollection = dcDB["posts"]

    baseUrl = "https://api.telegram.org/" + botToken

    while True:
        postsUndone = postsCollection.find({"done":False})
        for post in postsUndone:
            data = {'chat_id' : chat_id}
            for image in post['images']:
                if image['extension'] == "gif":
                    files = {'animation': open('images/' + image['name'], 'rb')}
                    sendGif = requests.post(baseUrl + "/sendAnimation", params=data, files=files)
                else:
                    files = {'document': open('images/' + image['name'], 'rb')}
                    sendImg = requests.post(baseUrl + "/sendDocument", params=data, files=files)
            
            text = ""
            text += post['galName'] + "\n"
            text += post['title'] + "\n"
            text += post['date'] + "\n"
            text += post['content']
            data['text'] = text
            sendMessage = requests.get(baseUrl + "/sendMessage", params=data)

            postsCollection.update_one({"num":post['num']}, {"$set":{"done":True}})

        print("Sleeping...")
        time.sleep(5)
