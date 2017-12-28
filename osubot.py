from group_rank import *
from caculate_pp import *
from db_collections import *
import random
from qqbot import qqbotsched

help_message="!rank [0123] 查看群内各模式菜鸡排名\n" \
             "!capp 查询单图pp\n" \
             "!roll 1-100随机roll点\n" \
             "!sleep [n] 让bot口球你n分钟\n" \
             "!refreshbp 手动刷新群内bp1，并报告bp1更新结果\n" \
             "!refreshpp 手动刷新群内pp，并报告pp更新结果\n" \
             "!su refreshbp 强制完全刷新bp1，不报告结果\n" \
             "!su refreshpp 强制完全刷新pp，不报告结果"

@qqbotsched(minute='*/10')
def check_bp_task(bot):
    re = diff_group_bps()
    if len(re) == 0:
        print("无bp1更新")
    else:
        for r in re:
            gl = bot.List('group', '200064826')
            if gl is not None:
                for group in gl:
                    bot.SendTo(group, r)
    re = diff_group_pps()
    if len(re) == 0:
        print("无pp大更新")
    else:
        for r in re:
            gl = bot.List('group', '200064826')
            if gl is not None:
                for group in gl:
                    bot.SendTo(group, r)

def onStartupComplete(bot):
    refresh_group_bps()
    refresh_group_pps()
    print("初始强制刷新完成")

def onQQMessage(bot, contact, member, content):
    if contact.ctype=='group' and (contact.qq=='203341856' or contact.qq=='200064826'):
        if not bot.isMe(contact, member):
            if content.startswith('!'):
                command = content[1:]
                if command.startswith("rank"):
                    mod = int(content[6:])
                    bot.SendTo(contact, get_rank(mod))
                elif command.startswith("capp"):
                    args = content[6:].split()
                    le = len(args)
                    if le == 0:
                        bot.SendTo(contact, "至少输入一个参数")
                    else:
                        mid = args[0]
                        if le >= 2:
                            argstr = ''
                            for i in range(1, le):
                                arg = args[i]
                                argstr += ' ' + arg
                        else:
                            argstr = None
                        bot.SendTo(contact, caculate_pp(mid, argstr))
                elif command.startswith("roll"):
                    bot.SendTo(contact, member.name + " 掷出 " + str(random.randint(1, 100)) + " 点")
                elif command.startswith("help"):
                    bot.SendTo(contact, help_message)
                elif command.startswith("sleep"):
                    min = int(content[7:])
                    gl = bot.List('group', contact.name)
                    if gl:
                        group = gl[0]
                        membs = bot.List(group, member.name)
                        if membs:
                            bot.GroupShut(group, membs, min * 60)
                elif command.startswith("refreshbp"):
                    re = diff_group_bps()
                    if len(re) == 0:
                        bot.SendTo(contact, "无任何bp1更新")
                    else:
                        for r in re:
                            bot.SendTo(contact, r)
                elif command.startswith("refreshpp"):
                    re = diff_group_pps()
                    if len(re) == 0:
                        bot.SendTo(contact, "无任何pp大更新")
                    else:
                        for r in re:
                            bot.SendTo(contact, r)
                elif command.startswith("su"):
                    if member.qq == '237515611':
                        subcommand = content[4:]
                        if subcommand.startswith("refreshbp"):
                            refresh_group_bps()
                            bot.SendTo(contact, "强制刷新bp完成")
                        elif subcommand.startswith("refreshpp"):
                            refresh_group_pps()
                            bot.SendTo(contact, "强制刷新pp完成")
                    else:
                        bot.SendTo(contact, "你不是权限狗，不能使用该命令")

