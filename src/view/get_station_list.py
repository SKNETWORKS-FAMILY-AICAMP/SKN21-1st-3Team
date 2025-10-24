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

        if is_24hr:
            query += f'and is_24hr="{is_24hr}"'
        if is_public:
            query += f'and is_public="{is_public}"'

        cursor.execute(query)
        result = cursor.fetchall()

        if result == None:
            return []

        return list(result)
    except Exception:
        print(Exception)
