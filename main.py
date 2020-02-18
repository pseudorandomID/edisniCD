from crawl import *
import requests

if __name__ == "__main__":
    s = requests.Session()


    pGalUrl = "https://gall.dcinside.com/board/lists/?id=programming"
    pGal = Gallery(url=pGalUrl, session=s)

    for postNum in pGal.postNums:
        post = pGal.posts[postNum]
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
        read = Post(post.url)
        print(read.content)
        print(read.comments)
        print("")

    commentData={"id":"programming","no":"1261736","cmt_id":"programming",
                 "cmt_no":"1261736", "e_s_n_o":"3eabc219ebdd65f53e",
                 "comment_page":"1","sort":"sort","prevCnt":"","board_type":""}
    #post = Post("https://gall.dcinside.com/board/view/?id=programming&no=1261729&page=1", s)
    #print(post.comments)
