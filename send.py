import requests
import pymongo



if __name__=="__main__":
    dbClient = pymongo.MongoClient("mongodb://localhost:27017/")
    dcDB = dbClient["dc"]
    postsCollection = dcDB["posts"]

    undones = postsCollection.find({"done":False})
    print(undones)
    for undone in undones:
        print(undone)
        #files = {'animation': img.content}
        data = {'chat_id' : "1020133801"}
        for image in undone['images']:
            print(image)
            files = {'photo': open('images/' + image, 'rb')}
            sendImg = requests.post("https://api.telegram.org/bot1048341657:AAFSB6dGOLlZRcxwcaqeXNejDhYLs7T8HAA/sendPhoto", params=data, files=files)
            print(sendImg)


        #sendImg = s.post("https://api.telegram.org/bot1048341657:AAFSB6dGOLlZRcxwcaqeXNejDhYLs7T8HAA/sendPhoto", params=params, headers={'Content-Type': 'multipart/form-data;'})
        #print(sendImg.text)
