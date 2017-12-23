import subprocess

def caculate_pp_win(mid, argstr):
    command=r"(New-Object System.Net.WebClient).DownloadString('https://osu.ppy.sh/osu/"+str(mid)+"') | oppai -"
    if argstr!=None:
        command+=argstr
    args=[r"powershell",command]
    p=subprocess.Popen(args, stdout=subprocess.PIPE)
    dt=p.stdout.read()
    return dt.decode('utf-8')

def caculate_pp(mid, argstr):
    command=r"curl https://osu.ppy.sh/osu/"+str(mid)+" | oppai -"
    if argstr!=None:
        command+=argstr
    args=[command]
    p=subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
    dt=p.stdout.read()
    return dt.decode('utf-8')

if __name__=="__main__":
    print(caculate_pp(994495, ' +hdhrnc 78.58% 239x'))