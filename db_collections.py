import pymysql
import traceback
import requests
import re
import json
from settings import *

s = requests.Session()

bp_dic=[{},{},{},{}]

pp_dic=[{},{},{},{}]

mod=['std', 'taiko', 'ctb', 'mania']

def get_group_uids():
    re=[]
    try:
        db = pymysql.connect(DB_IP, DB_USER, DB_PSWD, "osu")
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

def get_one_bp(uid):
    try:
        name = get_username(uid)
        for i in range(4):
            userurl = 'https://osu.ppy.sh/pages/include/profile-leader.php?u=' + str(uid) + '&m=' + str(i)
            data = s.get(userurl).content
            info = data.decode('utf-8')
            pplist = re.compile('<b>(.*?)pp</b>')
            pps = re.findall(pplist, info)
            if len(pps) == 0:
                pp = '0'
                map = ''
            else:
                pp = pps[0]
                maplist = re.compile('href="/b/.*?>(.*?)<div class="c">', re.S)
                map = re.findall(maplist, info)[0]
                map = map[:-8]
                map = map.replace('</a>', '')
                map = map.replace('</b>', '')
                map = map.replace('&#039;', '\'')
                map = map.replace('&amp;', '&')
                map = map.replace('&quot;', '"')
            bp_dic[i][uid] = [name, pp, map]
    except:
        traceback.print_exc()
        get_one_bp(uid)


def get_username(uid):
    userurl = 'https://osu.ppy.sh/u/' + str(uid)
    data = s.get(userurl).content
    user = data.decode('utf-8')
    userlist = re.compile('<title>(.*?)\'s profile', re.S)
    try:
        return re.findall(userlist, user)[0]
    except:
        print(str(uid)+" crashed")
        return get_username(uid)

def refresh_group_bps():
    for uid in get_group_uids():
        get_one_bp(uid)
    try:
        db = pymysql.connect(DB_IP, DB_USER, DB_PSWD, "osu")
        cursor = db.cursor()
        sql = 'INSERT INTO group_bps (uid, username, bpname, bppp, mode) VALUES (%s, %s, %s ,%s, %s) on duplicate key update username=values(username), bpname=values(bpname), bppp=values(bppp)'
        list=[]
        for i in range(len(bp_dic)):
            dic=bp_dic[i]
            for (k, v) in dic.items():
                 list.append((k, v[0], v[2], int(v[1]), i))
        cursor.executemany(sql, list)
        db.commit()
        db.close()
    except:
        traceback.print_exc()

def get_group_bps():
    re_bp_dic = [{}, {}, {}, {}]
    try:
        db = pymysql.connect(DB_IP, DB_USER, DB_PSWD, "osu")
        cursor = db.cursor()
        sql = "SELECT * FROM group_bps"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            re_bp_dic[int(row[4])][int(row[0])]=[row[1], str(row[3]), row[2]]
        db.close()
        return re_bp_dic
    except:
        traceback.print_exc()

def diff_group_bps():
    for uid in get_group_uids():
        get_one_bp(uid)
    old_bp_dic=get_group_bps()
    re=[]
    for i in range(len(bp_dic)):
        dic=bp_dic[i]
        old_dic=old_bp_dic[i]
        for (k, v) in dic.items():
            if old_dic[k]!=v:
                try:
                    re.append("("+mod[i]+") "+v[0]+" 刷新了bp1\n"+v[2]+" "+v[1]+"pp")
                    db = pymysql.connect(DB_IP, DB_USER, DB_PSWD, "osu")
                    cursor = db.cursor()
                    sql = """UPDATE group_bps SET username="%s", bpname="%s", bppp="%d" where uid="%d" and mode="%d" """ % (v[0], v[2], int(v[1]), k, i)
                    cursor.execute(sql)
                    db.commit()
                    db.close()
                except:
                    traceback.print_exc()
    return re

def get_one_pp(uid):
    try:
        name = get_username(uid)
        for i in range(4):
            ppurl = "https://osu.ppy.sh/api/get_user?k="+OSU_API_KEY+"&u=" + str(
                uid) + "&m=" + str(i)
            data = s.get(ppurl).content
            ddata = data.decode('utf-8')
            jdata = json.loads(ddata)
            pp_dic[i][uid] = [name, '-1' if jdata[0]['pp_raw'] == None else jdata[0]['pp_raw']]
    except:
        traceback.print_exc()
        get_one_pp(uid)

def refresh_group_pps():
    for uid in get_group_uids():
        get_one_pp(uid)
    try:
        db = pymysql.connect(DB_IP, DB_USER, DB_PSWD, "osu")
        cursor = db.cursor()
        sql = 'INSERT INTO group_pps (uid, username, pp, mode) VALUES (%s, %s, %s ,%s) on duplicate key update username=values(username), pp=values(pp)'
        list=[]
        for i in range(len(bp_dic)):
            dic=pp_dic[i]
            for (k, v) in dic.items():
                 list.append((k, v[0], float(v[1]), i))
        cursor.executemany(sql, list)
        db.commit()
        db.close()
    except:
        traceback.print_exc()

def get_group_pps():
    re_pp_dic = [{}, {}, {}, {}]
    try:
        db = pymysql.connect(DB_IP, DB_USER, DB_PSWD, "osu")
        cursor = db.cursor()
        sql = "SELECT * FROM group_pps"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            re_pp_dic[int(row[3])][int(row[0])]=[row[1], str(row[2])]
        db.close()
        return re_pp_dic
    except:
        traceback.print_exc()

def diff_group_pps():
    for uid in get_group_uids():
        get_one_pp(uid)
    old_pp_dic=get_group_pps()
    re=[]
    for i in range(len(pp_dic)):
        dic=pp_dic[i]
        old_dic=old_pp_dic[i]
        for (k, v) in dic.items():
            if old_dic[k]!=v:
                delta=float(v[1])-float(old_dic[k][1])
                if delta>1.0:
                    re.append("(" + mod[i] + ") " + v[0] + " +" + str(round(delta, 2)) + "pp\nfrom " + str(old_dic[k][1]) + "pp to " + str(v[1]) + "pp")
                try:
                    db = pymysql.connect(DB_IP, DB_USER, DB_PSWD, "osu")
                    cursor = db.cursor()
                    sql = """UPDATE group_pps SET username="%s", pp="%s" where uid="%d" and mode="%d" """ % (v[0], v[1], k, i)
                    cursor.execute(sql)
                    db.commit()
                    db.close()
                except:
                    traceback.print_exc()
    return re

if __name__ == "__main__":
    print(diff_group_pps())