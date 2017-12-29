import requests
import json
import threading
import traceback
from db_collections import get_group_uids
from settings import *

s = requests.Session()

limit_dic={}

limit_range=[[0,70],[70,90],[90,100]]
limit_des=['前途无量',"潜力平平","老年玩家"]

def get_limit(mod):
    limit_dic.clear()
    threads = [threading.Thread(target=get_one_limit, args=(uid, mod)) for uid in get_group_uids()]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    sort_dic = sorted(limit_dic.items(), key=lambda d: d[1][2], reverse=False)
    limit_str=''
    index=0
    first_flag=True
    for i in range(len(sort_dic)):
        person=sort_dic[i]
        while not limit_range[index][0]<=person[1][2]<limit_range[index][1]:
            index+=1
            first_flag=True
        if first_flag:
            limit_str+=limit_des[index]+"\n--------------------------\n\n"
            first_flag=False
        limit_str+=person[0]+" pp比: "+str(person[1][2])+"%\n"
        limit_str+="总pp: "+str(person[1][0])+"pp\n"
        limit_str+="bp1 pp: " + str(person[1][1]) + "pp\n\n"
    return limit_str

def get_one_limit(uid, mod):
    try:
        ppurl = "https://osu.ppy.sh/api/get_user_best?k=" + OSU_API_KEY + "&u=" + str(uid) + "&m=" + str(
            mod) + "&limit=1"
        data = s.get(ppurl).content
        ddata = data.decode('utf-8')
        jdata = json.loads(ddata)
        top_pp = float('-1' if len(jdata)==0 else jdata[0]['pp'])
        ppurl = "https://osu.ppy.sh/api/get_user?k=" + OSU_API_KEY + "&u=" + str(uid) + "&m=" + str(mod)
        data = s.get(ppurl).content
        ddata = data.decode('utf-8')
        jdata = json.loads(ddata)
        total_pp = float('-1' if jdata[0]['pp_raw'] == None else jdata[0]['pp_raw'])
        if (total_pp != -1.0 and total_pp != 0.0) and (top_pp != -1.0 and top_pp != 0.0):
            limit_dic[jdata[0]['username']] = [total_pp, top_pp, round(5 * total_pp / top_pp, 2)]
    except:
        traceback.print_exc()
        get_one_limit(uid, mod)

if __name__=="__main__":
    print(get_limit(0))