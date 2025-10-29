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


"""
    sql 서버 연동 모듈
"""

connection = sql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    port=db_port,
    db=db_name,
)

cursor = connection.cursor()
