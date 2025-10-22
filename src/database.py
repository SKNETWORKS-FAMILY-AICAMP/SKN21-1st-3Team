import pymysql as sql

"""
    sql 서버 연동 모듈
"""

connection = sql.connect(
    host="", user="", password="", port=3306, db="your_database_name"
)

cursor = connection.cursor()
