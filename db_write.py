from ppomppu import *
from db_info import *
import pymysql.cursors # python과 mysql(mariadb) 연동

# Connect to the DB
connection = pymysql.connect(host=DB_host,
                            user=DB_user,
                            password=DB_password,
                            db=DB_db,
                            charset=DB_charset,
                            cursorclass=pymysql.cursors.DictCursor
                            )

try:
    cursor = connection.cursor()

    def init_db_setting(): # 해당 테이블이 없으면 만들어라! menudata, review, user
        if not (cursor.execute("SHOW TABLES LIKE %s", 'hotdeal_list')):
            cursor.execute("CREATE TABLE hotdeal_list(idx INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,site VARCHAR(50),id INT(10), date DATETIME, img_src VARCHAR(200), title VARCHAR(100), href VARCHAR(200), comment INT(10), category VARCHAR(50), good INT(10), bad INT(10), viewer INT(10), expire INT(2))")
        

    def update_idx():
        # id값 1부터 다시 세기.
        cursor.execute("ALTER TABLE hotdeal_list AUTO_INCREMENT=1")
        cursor.execute("SET @COUNT = 0")
        cursor.execute("UPDATE hotdeal_list SET idx = @COUNT:=@COUNT+1")

    # [site, id, date, img_src, title, href, comment, category, good, bad, viewer, expire]
    def update_hotdeal(arg):
        for i in range(len(arg)):
            site_id = (arg[i][0], arg[i][1])
            if (cursor.execute("SELECT * FROM hotdeal_list WHERE site=%s AND id=%s", site_id)): # 중복이면
                if arg[i][11] == 1: # is_expire
                    cursor.execute("UPDATE hotdeal_list SET expire = 1 WHERE site=%s AND id=%s", site_id)
                else:
                    continue
            else:
                cursor.execute("INSERT INTO hotdeal_list (site, id, date, img_src, title, href, comment, category, good, bad, viewer, expire) VALUES(%s, %s, %s ,%s ,%s, %s, %s, %s, %s, %s, %s, %s)", arg[i])
    
    # 실행부분
    init_db_setting() # 초기에 한 번만 실행함. 테이블을 생성.

    update_hotdeal(ppomppu_lists)

    update_idx() # idx 순서 업데이트

    # DB_hotdealList = cursor.execute("select * from hotdeal_list")
    # DB_hotdealList = cursor.fetchall()
    # result = []
    # for i in range(len(DB_hotdealList)):
    #     temp = DB_hotdealList[i]['title']
    #     result.append(temp)
    # print(result)
    
    
finally:
    connection.commit() # 실행한 문장들 적용
    cursor.close()
    connection.close()