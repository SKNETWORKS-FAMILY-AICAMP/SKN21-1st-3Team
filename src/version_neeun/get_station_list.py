# src/queries -> src 프로젝트 root 변경
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.database import cursor


def get_station_list(
    region_code: int,
    sigungu_code: int,
    is_24hr,
    is_public,
):
    try:
        query = f"""
            SELECT * 
            FROM elecar_parking.charging_station 
            WHERE CTPRVN_CD="{region_code}" and SGG_CD="{sigungu_code}"
        """

        if is_24hr != None:
            query += f" and is_24h={is_24hr}"
        if is_public != None:
            query += f" and is_public={is_public}"

        cursor.execute(query)
        rows = cursor.fetchall()

        return rows
    except Exception:
        print(Exception)


def get_station_table_list(region_code, sigungu_code, is_24hr, is_public):
    rows = get_station_list(region_code, sigungu_code, is_24hr, is_public)
    if rows == None:
        return []

    result = {
        "ID": [],
        "이름": [],
        "주소(지번)": [],
        "주소(도로명)": [],
    }

    for row in rows:
        result["ID"].append(row[0])
        result["이름"].append(row[1])
        result["주소(지번)"].append(row[9])
        result["주소(도로명)"].append(row[10])

    return result


def get_station_map_list(
    region_code: int,
    sigungu_code: int,
    is_24hr,
    is_public,
):
    try:
        rows = get_station_list(region_code, sigungu_code, is_24hr, is_public)

        if rows == None:
            return []

        result = [[row[-4], row[-3], row[1]] for row in rows]

        return result
    except Exception:
        print(Exception)
