import pymysql
import random

# MySQL의 DB에 연결하기 위해 connect()함수를 이용
conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'op330',
    db = 'compdb',
    charset = 'utf8'
)

# 연결한 DB와 상호작용하기 위해 cursor객체 생성
curs = conn.cursor()

# 가상 회원 정보를 삽입하기 위한 SQL 쿼리문을 작성하여 저장
sql = "insert into field (field_id,field_classification) values(%s, %s)"

curs.execute(sql,(1,'기획/아이디어'))
curs.execute(sql,(2,'광고/마케팅'))
curs.execute(sql,(3,'논문/리포트'))
curs.execute(sql,(4,'영상/UCC/사진'))
curs.execute(sql,(5,'디자인/캐릭터/웹툰'))
curs.execute(sql,(6,'웹/모바일/플래시'))
curs.execute(sql,(7,'게임/소프트웨어'))
curs.execute(sql,(8,'과학/공학'))
curs.execute(sql,(9,'문학/글/시나리오'))
curs.execute(sql,(10,'건축/건설/인테리어'))
curs.execute(sql,(11,'네이밍/슬로건'))
curs.execute(sql,(12,'예체능/미술/음악'))
curs.execute(sql,(13,'대외활동/서포터즈'))
curs.execute(sql,(14,'봉사활동'))
curs.execute(sql,(15,'취업/창업'))
curs.execute(sql,(16,'해외'))
curs.execute(sql,(17,'기타'))

conn.commit()
conn.close()
