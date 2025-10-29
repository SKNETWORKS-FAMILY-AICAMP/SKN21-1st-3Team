from db_connection import cursor


def find_region_code(region_code: str) -> str:
    """
    지역구 이름으로 DB에 저장된 지역코드 가져오기
    Args:
        region_code (str): 대전,
    Return (str):
        '30'
    """
    try:
        query = f'SELECT CTPRVN_CD FROM elecar_parking.ctprvn_info WHERE CTPRVN_NM="{region_code}"'
        cursor.execute(query)
        result = cursor.fetchone()

        if result == None:
            raise Exception("invaild region_code")

        return result[0]
    except Exception:
        print("error", Exception.__str__)
        return ""


def find_sigungu_code(sigungu_code: str) -> str:
    """
    시/군/구 이름으로 시/군/구 지역 코드 가져오기
    Args:
        sigungu_code (str): '유성구'
    Return (str):
        '30200'
    """
    try:
        query = (
            f'SELECT SGG_CD FROM elecar_parking.sgg_info WHERE SGG_NM="{sigungu_code}"'
        )
        cursor.execute(query)
        result = cursor.fetchone()

        if result == None:
            raise Exception("invaild sigungu_code")

        return result[0]
    except Exception:
        print("error", Exception.__str__)
        return ""
