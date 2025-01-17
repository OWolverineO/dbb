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
sql = "insert into application (application_id,application_classification) values(%s, %s)"

curs.execute(sql,(1,'제한없음'))
curs.execute(sql,(2,'일반인'))
curs.execute(sql,(3,'대학생'))
curs.execute(sql,(4,'청소년'))
curs.execute(sql,(5,'어린이'))
curs.execute(sql,(6,'기타'))

sql = "insert into organizer (host_code_id,host_classification) values(%s, %s)"

curs.execute(sql,(6,'정부/공공기관'))
curs.execute(sql,(7,'공기업'))
curs.execute(sql,(33,'대기업'))
curs.execute(sql,(34,'신문/방송/언론'))
curs.execute(sql,(35,'외국계기업'))
curs.execute(sql,(36,'중견/중소/벤처기업'))
curs.execute(sql,(37,'비영리/협회/재단'))
curs.execute(sql,(38,'해외'))
curs.execute(sql,(39,'기타'))

sql = "insert into responsible_field (re_field_id, field_name) values(%s, %s)"

curs.execute(sql,(1,"건축"))
curs.execute(sql,(2,"기계"))
curs.execute(sql,(3,"소재*재료"))
curs.execute(sql,(4,"전기*전자"))
curs.execute(sql,(5,"컴퓨터*통신"))
curs.execute(sql,(6,"일반교육"))
curs.execute(sql,(7,"특수교육"))
curs.execute(sql,(8,"경영*경제"))
curs.execute(sql,(9,"법률"))
curs.execute(sql,(10,"사회*복지"))
curs.execute(sql,(11,"언론*방송"))
curs.execute(sql,(12,"정치*외교"))
curs.execute(sql,(13,"디자인"))
curs.execute(sql,(14,"무용"))
curs.execute(sql,(15,"연극*영화"))
curs.execute(sql,(16,"미술"))
curs.execute(sql,(17,"음악"))
curs.execute(sql,(18,"영상*사진"))
curs.execute(sql,(19,"의약"))
curs.execute(sql,(20,"언어*문학"))
curs.execute(sql,(21,"인문학"))
curs.execute(sql,(22,"수학"))
curs.execute(sql,(23,"물리"))
curs.execute(sql,(24,"화학"))
curs.execute(sql,(25,"생물"))
curs.execute(sql,(26,"지구과학"))

conn.commit()
conn.close()
