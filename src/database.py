import pymysql as sql

"""
    sql 서버 연동 모듈
"""

connection = sql.connect(
    host="192.168.0.37",
    user="project1",
    password="1111",
    port=3306,
    db="elecar_parking",
)

cursor = connection.cursor()
