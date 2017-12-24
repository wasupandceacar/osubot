import pymysql
import traceback

def get_group_uids():
    re=[]
    try:
        db = pymysql.connect("138.68.57.30", "root", "1248163264128", "osu")
        cursor = db.cursor()
        sql = "SELECT * FROM group_id"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            re.append(row[0])
        db.close()
        return re
    except:
        traceback.print_exc()

if __name__ == "__main__":
    print(get_group_uids())