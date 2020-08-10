# Database 관련
import pymysql
class MysqlController:
    def __init__(self,host,port,id,password,db_name):
        self.conn = pymysql.connect(host=host,port=port,user=id,password=password,db=db_name,charset='utf8')
        self.curs = self.conn.cursor()

    def insert(self,poster,competition):
        # query : check duplication
        query_check_duplication = "SELECT COUNT(*) as cnt FROM Competition WHERE title = %s;"

        # query : poster
        query_select_poster_max_id = "SELECT IFNULL(MAX(poster_id)+1,1) FROM Poster p"
        query_insert_poster = "INSERT INTO Poster(poster_id,poster_jpg) VALUES( %s, %s)"
        # query : competition
        query_select_competition_max_id = "SELECT IFNULL(MAX(poster_id)+1,1) FROM Competition c"
        query_insert_competition = "INSERT INTO Competition(competition_id,title,host,support,period_start,period_end,total_money,first_place_money,homepage,poster_id)" \
                                   "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # query : target
        query_select_application_equal_id = "SELECT application_id FROM Application WHERE application_classification=%s"
        query_insert_target = "INSERT INTO Competition_application(competition_id,application_id)" \
                              "VALUES(%s,%s)"
        # query : field
        query_select_field_equal_id = "SELECT field_id FROM Field WHERE field_classification=%s"
        query_insert_field = "INSERT INTO Competition_field(competition_id,field_id)" \
                             "VALUES(%s,%s)"

        try:
            # check duplication
            self.curs.execute(query_check_duplication,competition['title'])
            duplicationCnt = self.curs.fetchone()
            if duplicationCnt[0] > 0 :
                return

            # insert poster
            self.curs.execute(query_select_poster_max_id)
            poster_max_id = self.curs.fetchone()

            poster_tuple = (poster_max_id,poster)
            self.curs.execute(query_insert_poster,poster_tuple)

            # insert competition
            self.curs.execute(query_select_competition_max_id)
            competition_max_id = self.curs.fetchone()

            competition_tuple = (competition_max_id,competition['title'],competition['host'],competition['support'],
                                 competition['period_start'],competition['period_end'],competition['total_money'],
                                 competition['first_place_money'],competition['homepage'],poster_max_id)
            self.curs.execute(query_insert_competition,competition_tuple)

            # insert target
            for x in competition['target']:
                if x=='':
                    self.conn.rollback()
                    return
                self.curs.execute(query_select_application_equal_id,x)
                application_id = self.curs.fetchone()
                target_tuple = (competition_max_id,application_id)
                self.curs.execute(query_insert_target,target_tuple)

            # insert field
            for x in competition['category']:
                self.curs.execute(query_select_field_equal_id,x)
                field_id = self.curs.fetchone()
                field_tuple = (competition_max_id,field_id)
                self.curs.execute(query_insert_field,field_tuple)

            self.conn.commit()

        except pymysql.Error as e:
            self.conn.rollback()
            print(competition['title'])
            print(str(e))
            
    def insertHostCodeId(self,title,cidx):
        try:
            query_find_competition_id = "SELECT competition_id FROM competition WHERE title=%s or title=%s;"
            query_insert_host_code_id = "INSERT INTO Competition_host(competition_id,host_code_id) VALUES(%s,%s);"
            
            # 공모전 명(title)과 일치하는 competition_id 찾기
            find_competition_id_tuple = (title,title+' ')
            self.curs.execute(query_find_competition_id,find_competition_id_tuple)
            finded_id = self.curs.fetchone()
            
            # Competition_host 테이블에 data 추가
            insert_host_tuple = (finded_id,cidx)
            self.curs.execute(query_insert_host_code_id,insert_host_tuple)
            self.conn.commit()
        except pymysql.Error as e:
            self.conn.rollback()
            print(str(e))
            
    def isTitleExisted(self,title):
        ret = False
        query_find_competition_same_title1 = "SELECT * FROM Competition WHERE title=%s"
        query_tuple1 = (title,)
        self.curs.execute(query_find_competition_same_title1,query_tuple1)
        result1 = self.curs.fetchone()
        if result1 is not None:
            ret = True
            
        query_find_competition_same_title2 = "SELECT * FROM Competition WHERE title=%s"
        query_tuple2 = (title+' ',)
        self.curs.execute(query_find_competition_same_title2,query_tuple2)
        result2 = self.curs.fetchone()
        if result2 is not None:
            ret = True
        
        return ret
# Selenium 관련 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def get_driver():
    driver = webdriver.Chrome(
        executable_path="/var/www/html/dbb/chromedriver.exe"
    )
    return driver

def move_page(driver,url):
    driver.get(url)

def click_xpath_link(driver,xpath):
    check = False
    try:
        driver.find_element_by_xpath(xpath).click()
        check = True
    except NoSuchElementException:
        pass
    finally:
        return check

# Crawl 관련 함수
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as TE
import time
# from PIL import Image

def crawl(url):
    data = requests.get(url)
    print(data, url)
    return data.content

def loadTitle(driver,soup):
    # 공모전명
    # tit = (soup.select_one('div.tit-area > h6.tit')).text
    title = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div[1]/h6').text
    return title

def loadInfo(driver,soup):
    # 분야, 응모대상, 주최/주관, 후원/협찬, 접수기간, 총 상금, 1등 상금, 홈페이지, 첨부파일
    WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li'))
    )
    # '//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li[1]'
    # #container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li:nth-child(1)
#     info_list = soup.select('#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li')
#     if info_list==[]:
#         info_list = soup.select('#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li')
#         print("one more!!")
    
    info_list = driver.find_elements_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li')
#     for i in range(0,len(info_list)):
#         tmp  = info_list[i].text
#         info_list[i] = tmp
#     print(info_list)
    return info_list

def loadPoster(driver,base_url):
    # 포스터 이미지
    try:
        # 5초동안 poster가 로드됐는지 확인
        WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/img'))
        )
    except TE:
        # 5초동안 poster가 로드 안 된 경우는 poster가 없는 경우 (5초내로 보통 로드가 다 되기 때문)
        # 빈 white 이미지를 반환
        with open('blank.png','rb') as file:
            binaryData = file.read()
        return binaryData
    try:
        # 정상적인 포스터 크롤링 과정
        poster_tag = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/img')
        poster_src = poster_tag.get_attribute('src')
        poster_jpg = requests.get(poster_src).content
    except requests.exceptions.ConnectionError as e:
        print('Connection Error!')
        print(str(e))
    return poster_jpg

def getDevidedPeriodList(period):
    index = period.find('D')
    period = period[:index].strip()
    period_list = period.split(' ~ ')
    return period_list

def get_text_excluding_children(driver, element): 

         return driver.execute_script(""" return jQuery(arguments[0]).contents().filter(function() { 
                     return this.nodeType == Node.TEXT_NODE; }).text();
                     """, element)
    
def parsing(driver,title,info_list):
    dictD = {}
    column = ['title','category','target','host','support','period','total_money','first_place_money','homepage','file']
    index = 0
    dictD[column[index]] = title
    for info in info_list:
        index = index + 1
#         span = info.select_one('span')
#         span.extract()
        if info==info_list[len(info_list)-1]:
            break
        elif info==info_list[len(info_list)-3]:
            info = info.find_element_by_tag_name('a').text
        else:    
            info = get_text_excluding_children(driver,info)
#         div_sns = info.select_one('div.cd-sns')
#         if div_sns != None :
#             break
        dictD[column[index]] = info.strip()#info.text.strip()
    return dictD

# Main
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as TE

competition_column = ['title','category','target','host','support','period','total_money','first_place_money','homepage','file']

driver = get_driver()
sql_controller = MysqlController('localhost',3306,'root','op330','compdb')

# 주최사 구분없이 전체 공모전 Crawling ==========================================================================================
main_page_url="https://www.wevity.com"
for i in range(2335,2300,-1): # range(n,m,-1) : 페이지 n부터 m+1까지를 1씩 감소하며 이동, 0319maxPage = 2337
    for j in range(2,17): # 게시글 15개
        move_page(driver,main_page_url+"?c=find&s=1&gp="+str(i)) # url 입력 후 enter 치는 행동과 같음
        try:
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH,"//*[@id='container']/div[2]/div[1]/div[2]/div[3]/div/ul/li["+str(j)+"]/div[1]/a"))
            )
        except TE :
            # 해당 페이지에 더이상 공모전이 없는 경우, 바로 다음페이지 탐색
            break
        check = click_xpath_link(driver,"//*[@id='container']/div[2]/div[1]/div[2]/div[3]/div/ul/li["+str(j)+"]/div[1]/a")
        if check == True:
            # 페이지 소스 parsing할 수 있는 형태로 가져오기
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/div[2]/div[1]/div[2]/div/div[1]/h6'))
            )
            pageString = driver.page_source
            soup = BeautifulSoup(pageString,'html.parser')

            # ---------------------------------------------------------------------------------------
            # 포스터
            poster = loadPoster(driver,main_page_url)
            # 공모전명
            title = loadTitle(driver,soup)
            
            # 분야, 응모대상, 주최/주관, 후원/협찬, 접수기간, 총 상금, 1등 상금, 홈페이지, 첨부파일
            info_list = loadInfo(driver,soup)
            
            # 한 공모전에 대한 내용을 사전형태로 저장
            competition = parsing(driver,title,info_list)
            print(competition)
            # '분야'의 중복속성 제거를 위한 작업
            competition['category'] = competition['category'].split(', ')
            # '대상'의 중복속성 제거를 위한 작업
            competition['target'] = competition['target'].split(', ')
            # '접수기간'을 '접수시작', '접수마감'으로 분리하는 작업
            period_list = getDevidedPeriodList(competition['period'])
            competition['period_start'] = period_list[0]
            competition['period_end'] = period_list[1]
            del competition['period']

            sql_controller.insert(poster,competition)
            print(str(i)+":"+str(j))

# N. 창 종료
driver.close()

# DB에 있는 공모전의 주최사(host_code_id) update ===================================================================================
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as TE
import time
from selenium.common.exceptions import NoSuchElementException

host_idx = [6,7,33,34,35,36,37,38,39]
driver = get_driver()
for i in host_idx: # 주최사별
    for j in range(2338,2330,-1): # 페이지 이동 
        move_page(driver,main_page_url+"?c=find&s=1&gub=3&cidx="+str(i)+"&gp="+str(j))
        for k in range(2,17): # 게시글 15개
            try:
                try:
                    WebDriverWait(driver,10).until(
                        EC.presence_of_element_located((By.XPATH,"//*[@id='container']/div[2]/div[1]/div[2]/div[3]/div/ul/li["+str(k)+"]/div[1]/a"))
                    )
                except TE :
                    # 해당 페이지에 더이상 공모전이 없는 경우, 바로 다음페이지 탐색
                    break
                string = driver.find_element_by_xpath("//*[@id='container']/div[2]/div[1]/div[2]/div[3]/div/ul/li["+str(k)+"]/div[1]/a").text
                string = string.split(' ')
                string_len = len(string)
                title_extracted = ''
                span_cnt = len(driver.find_elements_by_xpath("//*[@id='container']/div[2]/div[1]/div[2]/div[3]/div/ul/li["+str(k)+"]/div[1]/a/span"))
                for x in range(0,string_len-span_cnt):
                    if x != string_len-span_cnt-1:
                        title_extracted = title_extracted + string[x] + ' '
                    else:
                        title_extracted = title_extracted + string[x]

                if sql_controller.isTitleExisted(title_extracted) == True:
                    sql_controller.insertHostCodeId(title_extracted,i)
                else :
                    WebDriverWait(driver,10).until(
                        EC.presence_of_element_located((By.XPATH,"//*[@id='container']/div[2]/div[1]/div[2]/div[3]/div/ul/li["+str(k)+"]/div[1]/a"))
                    )   
                    click_xpath_link(driver,"//*[@id='container']/div[2]/div[1]/div[2]/div[3]/div/ul/li["+str(k)+"]/div[1]/a")
                    WebDriverWait(driver,10).until(
                        EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/div[2]/div[1]/div[2]/div/div[1]/h6'))
                    )
                    # 페이지 소스 parsing할 수 있는 형태로 가져오기
                    pageString = driver.page_source
                    soup = BeautifulSoup(pageString,'html.parser')

                    # ---------------------------------------------------------------------------------------
                    # 포스터
                    poster = loadPoster(driver,main_page_url)
                    # 공모전명
                    title = loadTitle(driver,soup)
                    # 분야, 응모대상, 주최/주관, 후원/협찬, 접수기간, 총 상금, 1등 상금, 홈페이지, 첨부파일
                    info_list = loadInfo(driver,soup)
                    # 한 공모전에 대한 내용을 사전형태로 저장
                    competition = parsing(driver,title,info_list)

                    # '분야'의 중복속성 제거를 위한 작업
                    competition['category'] = competition['category'].split(', ')
                    # '대상'의 중복속성 제거를 위한 작업
                    competition['target'] = competition['target'].split(', ')
                    # '접수기간'을 '접수시작', '접수마감'으로 분리하는 작업
                    period_list = getDevidedPeriodList(competition['period'])
                    competition['period_start'] = period_list[0]
                    competition['period_end'] = period_list[1]
                    del competition['period']

                    sql_controller.insert(poster,competition)
                    sql_controller.insertHostCodeId(competition['title'],i)

                    move_page(driver,main_page_url+"?c=find&s=1&gub=3&cidx="+str(i)+"&gp="+str(j))
            except NoSuchElementException:
                pass

# N. 창 종료
driver.close()

