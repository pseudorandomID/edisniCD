import requests
import bs4
from urllib.parse import urlparse, parse_qs
import dcHeaders

class Image:
    def __init__(self, parsed_li):
        self.url = parsed_li.find('a')['href']
        self.name = parsed_li.text
        self.extension = parsed_li.text.split('.')[-1]

    def download(self):
        response = requests.get(self.url, headers=dcHeaders.Headers.imgDownHeaders)
        with open("images/" + self.name, 'wb') as imgFile:
            imgFile.write(response.content)
        del response 

    def toDict(self):
        dictImage = {}
        dictImage['name'] = self.name
        dictImage['url'] = self.url
        dictImage['extension'] = self.extension

        return dictImage
        

class Post:
    def __init__(self, url):
        session = requests.Session()
        parsed_url = urlparse(url)
        urlParams = parse_qs(parsed_url.query)
        raw = session.get(url, headers = dcHeaders.Headers.galHeaders)
        soup = bs4.BeautifulSoup(raw.text, 'html.parser')
        #commentData={"id":urlParams['id'],"no":urlParams['no'],"cmt_id":urlParams['id'],
        #             "cmt_no":urlParams['no'], "e_s_n_o":"3eabc219ebdd65f53e",
        #             "comment_page":"1","sort":"sort","prevCnt":"","board_type":""}
        #comments = session.post("https://gall.dcinside.com/board/comment/", data=commentData, headers=Headers.commentHeaders)
        #self.comments = comments.json()

        viewBox = soup.find("div", {"class":"writing_view_box"})
        imgList = soup.find("ul", {"class":"appending_file"})


        self.title = soup.find("span", {"class":"title_subject"}).text
        self.replyCnt = soup.find("span", {"class":"gall_comment"})
        self.url = url
        self.nick = soup.find("span", {"class":"nickname"})
        self.ip = soup.find("span", {"class":"ip"})
        self.date = soup.find("span", {"class":"gall_date"}).text
        self.count = soup.find("span", {"class":"gall_count"})
        self.recommend = soup.find("span", {"class":"gall_reply_num"})
        self.content = (lambda x : x.find("div", {"style":"overflow:hidden;"}).text if (x != None) else "")(viewBox)
        self.images = (lambda x : [Image(parsed_li) for parsed_li in x.findAll("li")] if (x != None) else [])(imgList)

def readPost(post):
    return Post(post.url)
        
class PostList:
    def __init__(self, galId, page='1'):
        class PostSummary:
            def __init__(self, tr):
                self.num = tr.find("td", {"class":"gall_num"}).text
                self.title = tr.find("td", {"class":"gall_tit"}).find("a").text
                #self.replyCnt = getReplyCnt(tr.find("span", {"class":"reply_num"}))
                self.url = "https://gall.dcinside.com" + tr.find("td", {"class":"gall_tit"}).find("a")["href"] 
                self.nick = tr.find("td", {"class":"gall_writer"})['data-nick']
                self.uid = tr.find("td", {"class":"gall_writer"})['data-uid']
                self.ip = tr.find("td", {"class":"gall_writer"})['data-ip']
                self.date = tr.find("td", {"class":"gall_date"})['title']
                self.count = tr.find("td", {"class":"gall_count"}).text
                self.recommend = int(tr.find("td", {"class":"gall_recommend"}).text)
                self.hasImg = (lambda x : True if (tr.find("em", {"class":"icon_pic"}) != None) else False)(tr)


        s = requests.Session()
        galUrl = "https://gall.dcinside.com/board/lists/?id=" + galId + "&page=" + page
        galResponse = s.get(galUrl, headers = dcHeaders.Headers.galHeaders)
        soup = bs4.BeautifulSoup(galResponse.text, 'html.parser')
        posts = soup.find_all("tr", {"class":"us-post"})
        
        #self.postNums = [(lambda x : x['data-no'])(post) for post in posts]
        #self.posts = {post['data-no'] : PostSummary(post) for post in posts}
        self.posts = {PostSummary(post) for post in posts}
