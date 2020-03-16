from dcinside import *
import pymongo

if __name__ == "__main__":
    dbClient = pymongo.MongoClient("mongodb://localhost:27017/")
    dcDB = dbClient["dc"]
    postsCollection = dcDB["posts"]

    galId= "baseball_new8"
    #pGal = Gallery(url=pGalUrl, session=s)
    postList = PostList(galId).posts

    for post in postList:
        if post.hasImg and post.recommend >= 1:
            postDetail = readPost(post)

            for image in postDetail.images:
                image.download()


            insertData = {}
            insertData['title'] = postDetail.title
            insertData['date'] = postDetail.date
            insertData['content'] = postDetail.content
            insertData['images'] = [image.name for image in postDetail.images]
            insertData['done'] = False
            print(insertData)
            print("dd")
            postsCollection.insert_one(insertData)
