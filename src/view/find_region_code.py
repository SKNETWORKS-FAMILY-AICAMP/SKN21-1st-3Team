# src/queries -> src 프로젝트 root 변경
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.database import cursor


def find_region_code(region_code: int):
    query = f"SELECT * FROM charging_station WHERE CTPRVN_CD = {region_code}"
    result = cursor.execute(query)
    print(result)


def find_sido_code(sido_code: int):
    query = f"SELECT * FROM charging_station WHERE CTPRVN_CD = {sido_code}"
    result = cursor.execute(query)
    print(result)
