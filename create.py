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
sql = """create table members( 
member_id int(10) not null,
name varchar(30) not null,
identity varchar(100) not null,
password varchar(100) not null,
contact char(13),
address varchar(200),
participation_count varchar(50) not null,
job varchar(50) not null,
mind int(10) not null,
energy int(10) not null,
nature int(10) not null,
tactics int(10) not null,
ego int(10) not null,
gender char(1),
age int(10),
email varchar(200),
hope_role varchar(255),
usertype int(10),
latitude double(20,10) not null,
longitude double(20,10) not null,
primary key(member_id),
unique key uk_identity (identity)
);

create table poster( 
poster_id int(10) not null,
poster_jpg mediumblob not null,
primary key (poster_id)
);

create table competition( 
competition_id int(10) not null,
title varchar(100) not null,
host varchar(100) not null,
support varchar(255),
period_start date not null,
period_end date not null,
total_money varchar(50),
first_place_money varchar(50),
homepage varchar(255),
poster_id int(10),
primary key (competition_id),
foreign key (poster_id) references poster (poster_id) on delete cascade
);

create table organizer( 
host_code_id int(10) not null,
host_classification varchar(30) not null,
primary key (host_code_id)
);

create table competition_host( 
competition_id int(10),
host_code_id int(10),
primary key (competition_id, host_code_id),
foreign key (competition_id) references competition (competition_id) on delete cascade,
foreign key (host_code_id) references organizer (host_code_id) on delete cascade
);

create table field( 
field_id int(10) not null,
field_classification varchar(30) not null,
primary key (field_id)
);

create table member_interests( 
member_id int(10) not null,
field_id int(10) not null,
primary key (member_id, field_id),
foreign key (member_id) references members (member_id) on delete cascade,
foreign key (field_id) references field (field_id) on delete cascade
);

create table competition_field( 
competition_id int(10) not null,
field_id int(10) not null,
primary key (competition_id, field_id),
foreign key (competition_id) references competition (competition_id) on delete cascade,
foreign key (field_id) references field (field_id) on delete cascade
);

create table favorites( 
member_id int(10) not null, 
competition_id int(10) not null,
primary key (member_id, competition_id),
foreign key (member_id) references members (member_id) on delete cascade,
foreign key (competition_id) references competition (competition_id) on delete cascade
);

create table application( 
application_id int(10) not null,
application_classification varchar(30) not null,
primary key (application_id)
);

create table competition_application( 
competition_id int(10) not null,
application_id int(10) not null,
primary key (competition_id, application_id),
foreign key (competition_id) references competition (competition_id) on delete cascade,
foreign key (application_id) references application (application_id) on delete cascade
);

create table responsible_field(
re_field_id int(10) not null,
field_name varchar(50) not null,
primary key(re_field_id)
);

create table responsible(
member_id int(10) not null,
re_field_id int(10) not null,
primary key (member_id, re_field_id),
foreign key (member_id) references members (member_id) on delete cascade,
foreign key (re_field_id) references responsible_field (re_field_id) on delete cascade
);

create table virtual_profile_evaluate(
member_id int(10) not null,
evaluate1 int(10),
evaluate2 int(10),
evaluate3 int(10),
evaluate4 int(10),
evaluate5 int(10),
primary key(member_id),
foreign key(member_id) references members (member_id) on delete cascade
);

create table recommend(
recommend_id int(10) not null,
competition_id int(10),
team_leader_id int(10),
team_member1_id int(10),
team_member2_id int(10),
team_member3_id int(10),
team_member4_id int(10),
primary key(recommend_id),
foreign key(competition_id) references competition (competition_id),
foreign key(team_leader_id) references members (member_id) on delete cascade,
foreign key(team_member1_id) references members (member_id) on delete cascade,
foreign key(team_member2_id) references members (member_id) on delete cascade,
foreign key(team_member3_id) references members (member_id) on delete cascade,
foreign key(team_member4_id) references members (member_id) on delete cascade
);

create table request(
request_id int(10) not null,
recommend_id int(10),
competition_id int(10),
send_member_id int(10),
receive_member_id int(10),
state char(1),
primary key(request_id),
foreign key(recommend_id) references recommend (recommend_id) on delete cascade,
foreign key(competition_id) references competition (competition_id) on delete cascade,
foreign key(send_member_id) references members (member_id) on delete cascade,
foreign key(receive_member_id) references members (member_id) on delete cascade
);

create table usertouser_interaction(
send_member_id int(10) not null,
receive_member_id int(10) not null,
rate int(10),
distance double(20,10),
primary key(send_member_id, receive_member_id),
foreign key(send_member_id) references members (member_id) on delete cascade,
foreign key(receive_member_id) references members (member_id) on delete cascade
);

insert into field (field_id,field_classification) values(1,'기획/아이디어');
insert into field (field_id,field_classification) values(2,'광고/마케팅');
insert into field (field_id,field_classification) values(3,'논문/리포트');
insert into field (field_id,field_classification) values(4,'영상/UCC/사진');
insert into field (field_id,field_classification) values(5,'디자인/캐릭터/웹툰');
insert into field (field_id,field_classification) values(6,'웹/모바일/플래시');
insert into field (field_id,field_classification) values(7,'게임/소프트웨어');
insert into field (field_id,field_classification) values(8,'과학/공학');
insert into field (field_id,field_classification) values(9,'문학/글/시나리오');
insert into field (field_id,field_classification) values(10,'건축/건설/인테리어');
insert into field (field_id,field_classification) values(11,'네이밍/슬로건');
insert into field (field_id,field_classification) values(12,'예체능/미술/음악');
insert into field (field_id,field_classification) values(13,'대외활동/서포터즈');
insert into field (field_id,field_classification) values(14,'봉사활동');
insert into field (field_id,field_classification) values(15,'취업/창업');
insert into field (field_id,field_classification) values(16,'해외');
insert into field (field_id,field_classification) values(17,'기타');

insert into application (application_id,application_classification) values(1,'제한없음');
insert into application (application_id,application_classification) values(2,'일반인');
insert into application (application_id,application_classification) values(3,'대학생');
insert into application (application_id,application_classification) values(4,'청소년');
insert into application (application_id,application_classification) values(5,'어린이');
insert into application (application_id,application_classification) values(6,'기타');

insert into organizer (host_code_id,host_classification) values(6,'정부/공공기관');
insert into organizer (host_code_id,host_classification) values(7,'공기업');
insert into organizer (host_code_id,host_classification) values(33,'대기업');
insert into organizer (host_code_id,host_classification) values(34,'신문/방송/언론');
insert into organizer (host_code_id,host_classification) values(35,'외국계기업');
insert into organizer (host_code_id,host_classification) values(36,'중견/중소/벤처기업');
insert into organizer (host_code_id,host_classification) values(37,'비영리/협회/재단');
insert into organizer (host_code_id,host_classification) values(38,'해외');
insert into organizer (host_code_id,host_classification) values(39,'기타');

insert into responsible_field (re_field_id, field_name) values (1,"건축");
insert into responsible_field (re_field_id, field_name) values (2,"기계");
insert into responsible_field (re_field_id, field_name) values (3,"소재*재료");
insert into responsible_field (re_field_id, field_name) values (4,"전기*전자");
insert into responsible_field (re_field_id, field_name) values (5,"컴퓨터*통신");
insert into responsible_field (re_field_id, field_name) values (6,"일반교육");
insert into responsible_field (re_field_id, field_name) values (7,"특수교육");
insert into responsible_field (re_field_id, field_name) values (8,"경영*경제");
insert into responsible_field (re_field_id, field_name) values (9,"법률");
insert into responsible_field (re_field_id, field_name) values (10,"사회*복지");
insert into responsible_field (re_field_id, field_name) values (11,"언론*방송");
insert into responsible_field (re_field_id, field_name) values (12,"정치*외교");
insert into responsible_field (re_field_id, field_name) values (13,"디자인");
insert into responsible_field (re_field_id, field_name) values (14,"무용");
insert into responsible_field (re_field_id, field_name) values (15,"연극*영화");
insert into responsible_field (re_field_id, field_name) values (16,"미술");
insert into responsible_field (re_field_id, field_name) values (17,"음악");
insert into responsible_field (re_field_id, field_name) values (18,"영상*사진");
insert into responsible_field (re_field_id, field_name) values (19,"의약");
insert into responsible_field (re_field_id, field_name) values (20,"언어*문학");
insert into responsible_field (re_field_id, field_name) values (21,"인문학");
insert into responsible_field (re_field_id, field_name) values (22,"수학");
insert into responsible_field (re_field_id, field_name) values (23,"물리");
insert into responsible_field (re_field_id, field_name) values (24,"화학");
insert into responsible_field (re_field_id, field_name) values (25,"생물");
insert into responsible_field (re_field_id, field_name) values (26,"지구과학");"""

curs.execute(sql)

             
conn.commit()
conn.close()