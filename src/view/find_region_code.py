# src/queries -> src 프로젝트 root 변경
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.database import cursor


def find_region_code(region_code: str):
    try:
        query = f'SELECT CTPRVN_CD FROM elecar_parking.ctprvn_info WHERE CTPRVN_NM="{region_code}"'
        cursor.execute(query)
        result = cursor.fetchone()

        if result == None:
            raise Exception("there is not this code")

        print(result[0])
        return result[0]
    except Exception:
        print("error", Exception)


def find_sigungu_code(sigungu_code: str):
    try:
        query = (
            f'SELECT SGG_CD FROM elecar_parking.sgg_info WHERE SGG_NM="{sigungu_code}"'
        )
        cursor.execute(query)
        result = cursor.fetchone()

        if result == None:
            raise Exception("there is not this code")

        # Iterate through the results and print them
        for row in result:
            print(row)
        print(result[0])
        return result[0]
    except Exception:
        print("error", Exception)
