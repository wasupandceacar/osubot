# 不知道想做什么的简陋osu群机器人 #

## 需要的环境 ##

- python3.5（qqbot库，请自行查看qqbot使用说明）
- mysql
- oppai-ng

**另外osu-api的key请最好自行申请一个**

## mysql设置 ##

1. 新建数据库osu
1. 新建表group_id，字段uid(int)，输入你群的所有osuid
1. 新建表group_bps，字段uid(int),username(varchar),bpname(varchar),bppp(int),mode(int)
1. 新建表group_id，字段uid(int),username(varchar),pp(float),mode(int)

## setting设置 ##

自行修改setting.py下的apikey,群组,数据库设置

----------

windows下请把osubot.py下的caculate_pp改为caculate_pp_win

----------

## 命令 ##

!rank [0123] 查看群内各模式菜鸡排名

!limit [0123] 查看群内各模式潜力表

!capp 查询单图pp

!roll 1-100随机roll点

!sleep [n] 让bot口球你n分钟

!refreshbp 手动刷新群内bp1，并报告bp1更新结果

!refreshpp 手动刷新群内pp，并报告pp更新结果

!su refreshbp 强制完全刷新bp1，不报告结果

!su refreshpp 强制完全刷新pp，不报告结果
