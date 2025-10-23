import pymysql as sql
from dotenv import load_dotenv
import pandas as pd
import os
from .. import database
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



def return_cur():
    connection = sql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    port=db_port,
    db=db_name)
    cursor = connection.cursor()

    return connection, cursor


def delete_all_data(connection, cursor, table_name):
    """_summary_
    table 안에 있는 모든 내용 삭제
    
    Args:
        connection (_type_): 커넥션
        cursor (_type_): 커서
        table_name (_type_): 지우려는 테이블 이름
    """
    import re

    if not isinstance(table_name, str):
        raise ValueError("table_name must be a string")

    # 안전 검증: 테이블명은 알파벳/숫자/언더스코어만 허용
    if not re.match(r'^[A-Za-z0-9_]+$', table_name):
        raise ValueError("unsafe table name; only letters, digits and underscore allowed")

    try:
        # TRUNCATE가 빠르고 자동으로 인덱스/자동증가값을 리셋하므로 기본 사용
        query = f"TRUNCATE TABLE `{table_name}`"
        cursor.execute(query)
        connection.commit()
    except Exception:
        # 문제가 생기면 롤백하고 예외 재발생
        try:
            connection.rollback()
        except Exception:
            pass
        raise

def insert_all_data(connection, cursor,  table_name, csv_path="charging_station.csv", chunksize=1000):
    """
    CSV(헤더 포함)를 읽어 charging_station 테이블에 삽입.
    컬럼 순서/이름은 CSV 헤더를 기준으로 하며, 빈값은 NULL로 처리.
    chunksize 단위로 나눠 executemany 로 수행하고 각 청크마다 커밋함.
    

    Args:
        connection (_type_): 커넥션
        cursor (_type_): 커서
        csv_path (str, optional): 파일 경로. Defaults to "charging_station.csv".
        chunksize (int, optional): 한 번에 넣는 데이터 수. Defaults to 1000.
    """
    try:
        for chunk in pd.read_csv(csv_path, chunksize=chunksize, dtype=str, keep_default_na=False):
            cols = list(chunk.columns)
            if not cols:
                continue
            col_names = ",".join([f"`{c}`" for c in cols])
            placeholders = ",".join(["%s"] * len(cols))
            query = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"

            rows = []
            for row in chunk.itertuples(index=False, name=None):
                cleaned = [None if (pd.isna(v) or v == "") else v for v in row]
                rows.append(tuple(cleaned))

            if rows:
                cursor.executemany(query, rows)
                connection.commit()
    except Exception as e:
        connection.rollback()
        print("삽입 중 오류:", e)
        raise

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir,"data", "charging_stations.csv")
    table_name = "charging_station"
    
    # 테이블 전체 데이터 삭제 필요 할 때 아래 주석 실행
    # delete_all_data(connection, cursor, table_name)
    connection, cursor = return_cur()

    try:
        insert_all_data(connection, cursor, table_name, csv_path=csv_path, chunksize=10000)
        print("삽입 완료")
    finally:
        cursor.close()
        connection.close()

