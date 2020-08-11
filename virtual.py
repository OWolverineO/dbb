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
sql = """insert into members(member_id, name, identity, password, participation_count,
    mind, energy, nature, tactics, ego, age, usertype, latitude, longitude, job)
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

# range(N) N명의 가상회원 정보를 DB에 삽입
for i in range(10):
    
    # 회원번호
    member_id = i+1
    
    # 이름
    name = "virtual_"+str(i+1)
    
    # 아이디
    identity = "virtual_"+str(i+1)
    
    # 비밀번호
    password = str(i+1)
    
    # 공모전 참가횟수 '0회','1~2회','3~4회','5회 이상' 중 하나를 랜덤으로 저장
    pc = ['0회','1~2회','3~4회','5회 이상']
    participation_count = pc[random.randint(0,3)]
    
    # 성격점수들 0 ~ 100 사이의 랜덤 값을 저장
    mind = random.randint(0,100)
    energy = random.randint(0,100)
    nature = random.randint(0,100)
    tactics = random.randint(0,100)
    ego = random.randint(0,100)
    
    # 유저 타입 1 ~ 2187 사이의 랜덤 값을 저장
    usertype = random.randint(1,2187)
    
    # 위도 대한민국의 위도 범위인 33 ~ 38 사이의 랜덤 값을 저장
    latitude = random.uniform(33,38)
    
    # 경도 대한민국의 경도 범위인 124 ~ 132 사이의 랜덤 값을 저장
    longitude = random.uniform(124,132)

    # 직업 '일반인','대학생','청소년','어린이','기타' 중 하나를 랜덤으로 저장
    joblist = ['일반인','대학생','청소년','어린이','기타']
    jobindex = random.randint(0,4)
    job = joblist[jobindex]

    # 나이 직업에 따라서 결정될 나이의 값이 다름
    age = 0
    # 일반인
    if jobindex == 0:
        ind = random.randint(0,100)
        if ind <= 25:
            age = random.randint(7,19)
        elif ind > 25 and ind <= 75:
            age = random.randint(20,40)
        else:
            age = random.randint(41,60)
    # 대학생
    elif jobindex == 1:
        ind = random.randint(0,100)
        if ind <= 90:
            age = random.randint(20,26)
        elif ind > 90 and ind <= 98:
            age = random.randint(27,30)
        else:
            age = random.randint(31,40)
    # 청소년
    elif jobindex == 2:
        age = random.randint(14,19)
    # 어린이
    elif jobindex == 3:
        age = random.randint(7,13)
    # 기타
    else:
        age = random.randint(7,60)
        
    # 결정된 가상 회원의 속성 값들을 DB에 삽입
    curs.execute(sql,(member_id, name, identity, password, participation_count,
                      mind, energy, nature, tactics, ego, age, usertype, latitude, longitude, job))

conn.commit()
conn.close()