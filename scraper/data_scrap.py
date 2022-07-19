#jupyter notebook 환경에서 사용함
#모듈로 분리하지 않음

import requests
from bs4 import BeautifulSoup

import json
import os
import time

#colab
from google.colab import output
from fake_useragent import UserAgent

#Json 파일 관리
class JsonControl:
  #생성, 소멸자
  def __init__(self, f_name:str):
    self.path = f"/content/drive/MyDrive/dcData/{f_name}.json" #google colab 
    self.__data_json = self.__dataReturn(f_name)

  def __dataReturn(self, f_name):
    self.__checkfile()
    fs = open(self.path)
    res = json.load(fs)
    fs.close()
    return res

  #파일 존재 유무 확인 
  def __checkfile(self):
    if os.path.isfile(self.path): return
    fs = open(self.path, "w")
    fs.write("{}")
    fs.close()
  
  #private
  def __saveData(self):
    fs = open(self.path, "w")
    json.dump(self.__data_json, fs, ensure_ascii=False)
    fs.close()

  def addData(self, post_num:str, data:dict):
    self.__data_json[post_num] = data
    self.__saveData()

#스크래퍼
class Control:
  
  def __init__(self, gellName, gellType=None):
    #self.setEnv()

    self.JsonCon = JsonControl(f"{gellName}_{gellType}")
    #request Session
    self.session = requests.Session()
    self.ua = UserAgent() 
    self.session.headers.update({'User-Agent': self.ua.random})
    
    self.lambdaPageUrl = None

    if None == gellType:
      self.session.get(f"https://gall.dcinside.com/board/lists?id={gellName}")
      self.lambdaPageUrl = lambda x: f"https://gall.dcinside.com/board/view/?id={gellName}&no={x}"
      self.delurl = f"/derror/deleted/{gellName}/gallery"
    elif "m" == gellType:
      self.session.get(f"https://gall.dcinside.com/mgallery/board/lists?id={gellName}")
      self.lambdaPageUrl = lambda x: f"https://gall.dcinside.com/mgallery/board/view/?id={gellName}&no={x}"
      self.delurl = f"/derror/deleted/{gellName}/minor"
    elif "mini" == gellType:
      self.session.get(f"https://gall.dcinside.com/mini/board/lists/?id={gellName}")
      self.lambdaPageUrl = lambda x: f"https://gall.dcinside.com/mini/board/view/?id={gellName}&no={x}"
      self.delurl = f"/derror/deleted/{gellName}/mini"
    else:
      self.__del__() #호출 안될수도

    return

  def __del__(self):
    print("종료")

  #############
  def setEnv():
    pass

  def test(self):
    print(self.lambdaPageUrl(6357358))
  
  #public function
  def uaUpdate(self):
    self.session.headers.update({'User-Agent': self.ua.random})

  def getPost(self, url_number):
    page = self.session.get(self.lambdaPageUrl(url_number))
    bs = BeautifulSoup(page.text, "html.parser")

    if self.__checkDel(page.text):
      print(f"Delete Post: {page.url}")
      return
    post = self.__getContent(bs)

    self.JsonCon.addData(str(url_number), post)
    
    print(f"url:{page.url}")
    return


  #def setrange(start, end):
  #  pass

  def __checkDel(self, html):
    #print(html)
    "/derror/deleted/aoegame/minor"
    if f"<script type=\"text/javascript\">location.replace(\"{self.delurl}\");</script>" == html:
      return True
    else:
      return False

  #postting data
  def __getContent(self, bsData):
    bsContent = bsData.find('div', attrs={"class" : "view_content_wrap"})
    bsHeader = bsData.find("div", attrs= {"class" : "gallview_head"})

    #글 데이터
    title = bsData.find("span", attrs={"class" : "title_subject"}).text
    identi = bsData.find("div", attrs={"class" : "gall_writer"})["data-nick"]

    view = bsData.find("span", attrs={"class" : "gall_count"}).text
    recommend = bsData.find("span", attrs={"class" : "gall_reply_num"}).text
    datetime = bsData.find("span", attrs={"class" : "gall_date"}).text
    content = bsData.find("div", attrs={"class" : "write_div"}).text

    #platform = bsContent.find("span", attrs={"class" : "title_device"}).find("em", attrs={"class": "blind"}).text
    
    comment = bsData.find("span", attrs={"class" : "gall_comment"}).text #self.__getComent(bsData.find("div", attrs={"class" : "view_comment"})) #.find('div', attrs={"class" : "view_comment"}).

    return {"title":title, 
            "identi": identi, 
            "view" : view, 
            "recommend" : recommend, 
            "datetime": datetime,
            "content" : content,
            #"platform" : platform,
            "comment" : comment
            }

  # api 못 뜯음 -> 뜯는데 성공한다면 추가
  # def __getComent(self, bsData)->list:
  #   #print(bsData)
  #   return
  #   #답장 순회
  #   def getReply(bsReplyData) -> list:
  #     if None == bsReplyData : return None # 답장 영역이 없을 경우 None인지 확인 필요
  #     #답장에 대한 html data를 받는다
  #     replyList = []
  #     replyDict = (lambda i, d, c: {"identi": i, "datetime" : d, "content" : c})
  #     for i in range(0):
  #       #답장을 파싱하며 순회 진행 추가
  #       replyList += [replyDict(1, 3, 4)]
  #     return replyList
  #   #main
  #   #코멘트 영역을 찾아, 순회 진행 추가
  #   comentList = []
  #   coment =  (lambda i, d, c, r: {"identi": i, "datetime" : d, "content" : c, "reply": r})

  #   for bs_coment in range(0):
  #     #텍스트 부분 파싱해서 교체하게 만들기
  #     comentList += [coment(
  #         i="ㅇㅇ",
  #         d="2022. 07. 27",
  #         c="댓글내용",
  #         r=getReply(None) #답장 영역 파싱 None 부분 교체
  #     )]
  #   return comentList
    
#main

PAGE_URL = 21504069 #

post_range = 3002 #스크래핑 범위

start = PAGE_URL - post_range
end = PAGE_URL

loop = 0

g_name = "aoegame" #갤러리 명
g_type = "m" #갤러리 종류 

c = Control(gellName=g_name, gellType=g_type)

#감소하며 진행
while loop <= post_range:
  try:
    time.sleep(5)
    c.getPost(str(end - loop))
    loop += 1
    if loop % 10 == 0:
      output.clear()
      c.uaUpdate()
  except:
    c.uaUpdate()
