from db_connection import cursor


def get_station_list(
    region_code: str,
    sigungu_code: str,
    is_24hr: int | None,
    is_public: int | None,
):
    """
    전기차 목록 조회
    """
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
        print("query error", Exception.__str__)
        return []


def get_station_table_list(region_code, sigungu_code, is_24hr, is_public):
    """
    충전소 목록 테이블용 뷰를 위한 데이터 가공
    """
    rows = get_station_list(region_code, sigungu_code, is_24hr, is_public)

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
    region_code: str,
    sigungu_code: str,
    is_24hr: int | None,
    is_public: int | None,
):
    """
    충전소 목록 지도용 뷰를 위한 데이터 가공
    """
    rows = get_station_list(region_code, sigungu_code, is_24hr, is_public)
    result = [[row[-4], row[-3], row[1]] for row in rows]
    return result
