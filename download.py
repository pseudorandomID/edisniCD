from dcinside import *
import pymongo
import time
import sys
import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--g', help='Gallery ID')
    parser.add_argument('--r', help='Recommends', type=int, default=3)
    errMsg = "Please specify Gallery ID with --g option"
    args = parser.parse_args()
    return (lambda x: x if x.g else sys.exit(errMsg))(args)

if __name__ == "__main__":
    args = parseArgs()
    galId, minRecommends = args.g, args.r

    dbClient = pymongo.MongoClient("mongodb://localhost:27017/")
    dcDB = dbClient["dc"]
    postsCollection = dcDB["posts"]

    while True:
        time.sleep(3)
        try:
            gal = Gallery(galId)
            postList = gal.posts

            for post in postList:
                if (
                    post.hasImg 
                    and post.recommends >= minRecommends
                    and postsCollection.find_one({'num':post.num}) == None
                   ):

                    postDetail = readPost(post)

                    for image in postDetail.images:
                        print("Downloading %s" %(image.name))
                        image.download()
                        print("complete!\n")

                    document = postDetail.toDict()
                    document['done'] = False
                    postsCollection.insert_one(document)

            print("Sleeping...")

        except KeyboardInterrupt:
            sys.exit()

        except Exception as e:
            print(e.__doc__)
            print(e)
