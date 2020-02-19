from crawl import *
import requests
from dcHeaders import *

if __name__ == "__main__":
    s = requests.Session()


    pGalUrl = "https://gall.dcinside.com/board/lists/?id=programming"
    b8GalUrl = "https://gall.dcinside.com/board/lists/?id=baseball_new8"
    pGal = Gallery(url=pGalUrl, session=s)
    b8Gal = Gallery(url=b8GalUrl, session=s)

    print(b8Gal.posts)
    print(b8Gal.postNums)
    sendData = []
    for postNum in b8Gal.postNums:
        post = b8Gal.posts[postNum]
        print("글번호: " + post.num)
        print("제목: " + post.title)
        print("댓글수: " + post.replyCnt)
        if post.ip == "":
            print("고닉: " + post.nick + "(" + post.uid + ")")
        else:
            print("유동: " + post.ip)
        print("날짜: " + post.date)
        print("조회수: " + post.count)
        print("추천: " + post.recommend)
        print("url: " + post.url)
        #read = Post(post.url)
        #print(read.content)
        #print(read.comments)
        print("")
        writer = ""

        if post.ip == "":
            writer += post.nick + "(" + post.uid + ")"
        else:
            writer += post.ip
        sendText = ""
        sendText += "글번호: %s\n" % post.num
        sendText += "제목: %s\n" % post.title
        sendText += "작성자: %s\n" % writer
        sendText += "날짜: %s\n" % post.date
        sendText += "조회수: %s\n" % post.count
        sendText += "추천: %s\n" % post.recommend 
        #sendText += "url: %s\n" % post.url 
        sendData.insert(0, sendText)
    commentData={"id":"programming","no":"1261736","cmt_id":"programming",
                 "cmt_no":"1261736", "e_s_n_o":"3eabc219ebdd65f53e",
                 "comment_page":"1","sort":"sort","prevCnt":"","board_type":""}
    #post = Post("https://gall.dcinside.com/board/view/?id=programming&no=1261729&page=1", s)
    #print(post.comments)
    for data in sendData:
        params = {"chat_id":"1020133801", "text":data }
        #params = {"chat_id": "217736082", "text":data }
        sended = s.get("https://api.telegram.org/bot1048341657:AAFSB6dGOLlZRcxwcaqeXNejDhYLs7T8HAA/sendMessage", params=params)
        print(sended.text)
        print(sended)


    #img = s.get("https://image.dcinside.com/download.php?no=24b0d769e1d32ca73fed83fa11d02831dd6ec24037e3c20ed8a76c8571d8aa31fd66163f30336a7e010a5fb648162982fd0705863e98d6f10ed0ea77519d7a3b493416c9f435&f_no=7cf3d72fe3", headers = Headers.imgDownHeaders)

    #print(img.content)
    #with open('picture_out.gif', 'wb') as f:
    #    f.write(img.content)

    #files = {'animation': open('picture_out.gif', 'rb')}
    #files = {'animation': img.content}
    data = {'chat_id' : "1020133801"}

    #sendImg = s.get("https://api.telegram.org/bot1048341657:AAFSB6dGOLlZRcxwcaqeXNejDhYLs7T8HAA/sendPhoto", params=params, headers={'Content-Type': 'multipart/form-data;'})
    #sendImg = s.post("https://api.telegram.org/bot1048341657:AAFSB6dGOLlZRcxwcaqeXNejDhYLs7T8HAA/sendAnimation", params=data, files=files)
    #print(sendImg.text)
