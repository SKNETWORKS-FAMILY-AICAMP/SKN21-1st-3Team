import pymysql as sql
from dotenv import load_dotenv
import os


# .env 환경 변수 load
load_dotenv()

# 환경 변수 설정
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD") or ""
db_name = os.environ.get("DB_NAME")
db_port = int(os.environ.get("DB_PORT") or 0)

# sql 서버 연동 모듈

connection = sql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    port=db_port,
    db=db_name,
)

cursor = connection.cursor()

def get_SD_NM():
    get_sql = "SELECT CTPRVN_NM FROM ctprvn_info"
    try:
        cursor.execute(get_sql)
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        # 간단한 오류 처리: 필요하면 로깅이나 예외 재발생으로 변경하세요.
        print(f"DB error in get_SD_NM: {e}")
        return []
def get_SGG_NM():
    pass

    
if __name__ == "__main__":
    print(get_SD_NM())
