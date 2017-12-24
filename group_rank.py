import requests
import json
import threading
from db_collections import get_group_uids

s = requests.Session()

rank_dic={}

def get_rank(mod):
    threads = [threading.Thread(target=get_one_rank, args=(uid, mod)) for uid in get_group_uids()]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    sort_dic=sorted(rank_dic.items(), key=lambda d:d[1],reverse=True)
    rankstr=''
    for i in range(len(sort_dic)):
        person=sort_dic[i]
        rankstr+="#"+str(i+1)+" "+person[0]+"\n"
        rankstr+=str(person[1])+"pp\n\n"
    print(rankstr)
    return rankstr

def get_one_rank(uid, mod):
    ppurl = "https://osu.ppy.sh/api/get_user?k=cff10afa31a4a9cd85aa7bc433c20c862562ed51&u=" + str(uid) + "&m="+str(mod)
    data = s.get(ppurl).content
    ddata = data.decode('utf-8')
    jdata = json.loads(ddata)
    rank_dic[jdata[0]['username']] = float('-1' if jdata[0]['pp_raw']==None else jdata[0]['pp_raw'])

if __name__=="__main__":
    get_rank(0)