import pymysql as sql
from dotenv import load_dotenv
import pandas as pd
import os
# .env 환경 변수 load
load_dotenv()

# 환경 변수 설정
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD") or ""
db_name = os.environ.get("DB_NAME")
db_port = int(os.environ.get("DB_PORT") or 0)

# read CSV (assumes file is next to this script or provide full path)
csv_path = os.path.join(os.path.dirname(__file__), "charging_stations.csv")
df = pd.read_csv(csv_path, dtype=str).rename(columns=lambda c: c.strip())

if not {"OBJT_ID", "X", "Y"}.issubset(df.columns):
    raise ValueError("CSV must contain OBJT_ID, X and Y columns")

conn = sql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    db=db_name,
    port=db_port,
    charset="utf8mb4",
    cursorclass=sql.cursors.DictCursor,
)
try:
    with conn.cursor() as cur:
        sql_update = "UPDATE charging_station SET longitude=%s, latitude=%s WHERE OBJT_ID=%s"
        updated_count = 0
        for _, row in df.iterrows():
            obj_id = row["OBJT_ID"]
            try:
                lon = float(row["X"])
                lat = float(row["Y"])
            except Exception:
                # skip rows with invalid coordinates
                continue
            cur.execute(sql_update, (lon, lat, obj_id))
            if cur.rowcount and cur.rowcount > 0:
                updated_count += cur.rowcount
        conn.commit()
    print(f"Rows updated: {updated_count}")
finally:
    conn.close()