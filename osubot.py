from group_rank import *
from caculate_pp import *
import random

help_message="!rank [0123] 查看群内各模式菜鸡排名\n" \
             "!capp 查询单图pp\n" \
             "!roll 1-100随机roll点\n" \
             "!sleep [n] 让bot口球你n秒"

def onQQMessage(bot, contact, member, content):
    if contact.ctype=='group' and (contact.qq=='203341856' or contact.qq=='200064826'):
        if content.startswith('!'):
            command=content[1:]
            if command.startswith("rank"):
                mod=int(content[6:])
                bot.SendTo(contact, get_rank(mod))
            elif command.startswith("capp"):
                args=content[6:].split()
                le=len(args)
                if le==0:
                    bot.SendTo(contact, "至少输入一个参数")
                else:
                    mid=args[0]
                    if le>=2:
                        argstr=''
                        for i in range(1, le):
                            arg=args[i]
                            argstr+=' '+arg
                    else:
                        argstr=None
                    bot.SendTo(contact, caculate_pp(mid, argstr))
            elif command.startswith("roll"):
                bot.SendTo(contact, member.name+" 掷出 "+str(random.randint(1, 100))+" 点")
            elif command.startswith("help"):
                bot.SendTo(contact, help_message)
            elif command.startswith("sleep"):
                second = int(content[7:])
                gl = bot.List('group', contact.name)
                if gl:
                    group = gl[0]
                    membs = bot.List(group, member.name)
                    if membs:
                        bot.GroupShut(group, membs, second)

