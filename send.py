import requests
import pymongo



if __name__=="__main__":
    dbClient = pymongo.MongoClient("mongodb://localhost:27017/")
    dcDB = dbClient["dc"]
    postsCollection = dcDB["posts"]

    apiBaseUrl = "https://api.telegram.org/"
    botToken = "bot1048341657:AAFSB6dGOLlZRcxwcaqeXNejDhYLs7T8HAA"

    undones = postsCollection.find({"done":False})
    for undone in undones:
        #files = {'animation': img.content}
        data = {'chat_id' : "1020133801"}
        for image in undone['images']:
            if image['extension'] == "gif":
                files = {'animation': open('images/' + image['name'], 'rb')}
                sendGif = requests.post(apiBaseUrl + botToken + "/sendAnimation", params=data, files=files)
            else:
                files = {'photo': open('images/' + image['name'], 'rb')}
                sendImg = requests.post(apiBaseUrl + botToken + "/sendPhoto", params=data, files=files)

        postsCollection.update_one(undone, "$set":{"done":True})



        #sendImg = s.post("https://api.telegram.org/bot1048341657:AAFSB6dGOLlZRcxwcaqeXNejDhYLs7T8HAA/sendPhoto", params=params, headers={'Content-Type': 'multipart/form-data;'})
        #print(sendImg.text)
