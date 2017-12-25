import pymysql
import traceback
import requests
import re
import threading

s = requests.Session()

bp_dic=[{},{},{},{}]

mod=['std', 'taiko', 'ctb', 'mania']

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

def get_one_bp(uid):
    name = get_username(uid)
    for i in range(4):
        userurl = 'https://osu.ppy.sh/pages/include/profile-leader.php?u=' + str(uid) + '&m='+str(i)
        data = s.get(userurl).content
        info = data.decode('utf-8')
        pplist = re.compile('<b>(.*?)pp</b>')
        pps = re.findall(pplist, info)
        if len(pps)==0:
            pp='0'
            map=''
        else:
            pp=pps[0]
            maplist = re.compile('href="/b/.*?>(.*?)<div class="c">', re.S)
            map = re.findall(maplist, info)[0]
            map = map[:-8]
            map = map.replace('</a>', '')
            map = map.replace('</b>', '')
            map = map.replace('&#039;', '\'')
            map = map.replace('&amp;', '&')
            map = map.replace('&quot;', '"')
        bp_dic[i][uid]=[name, pp, map]

def get_username(uid):
    userurl = 'https://osu.ppy.sh/u/' + str(uid)
    data = s.get(userurl).content
    user = data.decode('utf-8')
    userlist = re.compile('<title>(.*?)\'s profile', re.S)
    return re.findall(userlist, user)[0]

def refresh_group_bp():
    threads = [threading.Thread(target=get_one_bp, args=(uid, )) for uid in get_group_uids()]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    try:
        db = pymysql.connect("138.68.57.30", "root", "1248163264128", "osu")
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
        db = pymysql.connect("138.68.57.30", "root", "1248163264128", "osu")
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
    threads = [threading.Thread(target=get_one_bp, args=(uid, )) for uid in get_group_uids()]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    old_bp_dic=get_group_bps()
    re=[]
    for i in range(len(bp_dic)):
        dic=bp_dic[i]
        old_dic=old_bp_dic[i]
        for (k, v) in dic.items():
            if old_dic[k]!=v:
                try:
                    re.append("("+mod[i]+") "+v[0]+" 刷新了bp1\n"+v[2]+" "+v[1]+"pp")
                    db = pymysql.connect("138.68.57.30", "root", "1248163264128", "osu")
                    cursor = db.cursor()
                    sql = "UPDATE group_bps SET username='%s', bpname='%s', bppp='%d' where uid='%d' and mode='%d'" % (v[0], v[2], int(v[1]), k, i)
                    cursor.execute(sql)
                    db.commit()
                    db.close()
                except:
                    traceback.print_exc()
    return re

if __name__ == "__main__":
   print(diff_group_bps())