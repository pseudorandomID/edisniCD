import requests
import bs4
from urllib.parse import urlparse, parse_qs

class Headers:
    dcHeaders = {"Host": "nstatic.dcinside.com",
                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0",
                 "Accept": "text/css,*/*;q=0.1",
                 "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
                 "Accept-Encoding": "gzip, deflate, br",
                 "Connection": "keep-alive"
                }

    commentHeaders = {"Host": "gall.dcinside.com",
                      "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0",
                      "Accept": "application/json, text/javascript, */*; q=0.01",
                      "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
                      "Accept-Encoding": "gzip, deflate, br",
                      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                      "X-Requested-With": "XMLHttpRequest"
                     }
class Post:
    def __init__(self, url, session = None):
        if session == None:
            session = requests.Session()

        parsed_url = urlparse(url)
        urlParams = parse_qs(parsed_url.query)
        raw = session.get(url, headers = Headers.dcHeaders)
        soup = bs4.BeautifulSoup(raw.text, 'html.parser')
        viewBox = soup.find("div", {"class":"writing_view_box"})
        content = viewBox.find("div", {"style":"overflow:hidden;"}).text
        commentData={"id":urlParams['id'],"no":urlParams['no'],"cmt_id":urlParams['id'],
                     "cmt_no":urlParams['no'], "e_s_n_o":"3eabc219ebdd65f53e",
                     "comment_page":"1","sort":"sort","prevCnt":"","board_type":""}
        comments = session.post("https://gall.dcinside.com/board/comment/", data=commentData, headers=Headers.commentHeaders)

        self.title = soup.find("span", {"class":"title_subject"})
        self.replyCnt = soup.find("span", {"class":"gall_comment"})
        self.url = url
        self.nick = soup.find("span", {"class":"nickname"})
        self.ip = soup.find("span", {"class":"ip"})
        self.date = soup.find("span", {"class":"gall_date"})
        self.count = soup.find("span", {"class":"gall_count"})
        self.recommend = soup.find("span", {"class":"gall_reply_num"})
        self.content = content
        self.comments = comments.json()
        
class Gallery:
    def __init__(self, url, session = None):
        class PostInfo:
            def __init__(self, tr):
                self.num = tr.find("td", {"class":"gall_num"}).text
                self.title = tr.find("td", {"class":"gall_tit"}).find("a").text
                self.replyCnt = getReplyCnt(tr.find("span", {"class":"reply_num"}))
                self.url = "https://gall.dcinside.com" + tr.find("td", {"class":"gall_tit"}).find("a")["href"] 
                self.nick = tr.find("td", {"class":"gall_writer"})['data-nick']
                self.uid = tr.find("td", {"class":"gall_writer"})['data-uid']
                self.ip = tr.find("td", {"class":"gall_writer"})['data-ip']
                self.date = tr.find("td", {"class":"gall_date"})['title']
                self.count = tr.find("td", {"class":"gall_count"}).text
                self.recommend = tr.find("td", {"class":"gall_recommend"}).text

        def getReplyCnt(e):
            if e == None:
                return ""
            return e.text

        if session == None:
            session = requests.Session()

        gal = session.get(url, headers = Headers.dcHeaders)
        soup = bs4.BeautifulSoup(gal.text, 'html.parser')
        trs = soup.find_all("tr", {"class":"us-post"})
        
        self.postNums = [(lambda x : x['data-no'])(tr) for tr in trs]
        self.posts = {tr.find("td", {"class":"gall_num"}).text : PostInfo(tr) for tr in trs}
