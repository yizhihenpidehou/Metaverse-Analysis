import json
import math
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np



# 计算整体女性研究者比例
def female_percentage(lst):
    total=0
    female=0
    for i in range(0,len(lst)-1):
        json_str=json.loads(lst[i])
        gender_lst=json_str["gender"]
        for g in gender_lst:
            if g==0:
                female+=1
            total+=1
    return female/total

# 计算团队大小分布
def team_size_calculate(lst):
    team_size_dict=defaultdict(int)
    for i in range(1,7):
        team_size_dict[i]=0
    for i in range(0,len(lst)-1):
        json_str = json.loads(lst[i])
        team_size_dict[len(json_str["author"])]+=1
    return team_size_dict

# 计算 单性别 或 混合性别 的比例
def team_gender_diversity(gender_lst):
    gender_dict={1:0,0:0}
    for gender in gender_lst:
        gender_dict[gender]+=1
    if gender_dict[1] == len(gender_lst) or gender_dict[0] == len(gender_lst):
        return 0
    else:
        return 1

def team_size_mixed_gender(lst,norm=True):
    team_size_dict=defaultdict(int)
    mixed_total=0
    for i in range(0,len(lst)-1):
        json_str=json.loads(lst[i])
        gender_lst=json_str["gender"]
        mixed_flag=team_gender_diversity(gender_lst)
        if len(gender_lst)>=6 and mixed_flag:
            team_size_dict['6']+=1
            mixed_total+=1
        elif len(gender_lst)<6 and mixed_flag:
            team_size_dict[str(len(gender_lst))]+=1
            mixed_total += 1
    if norm:
        for k,v in team_size_dict.items():
            team_size_dict[k]=v/mixed_total

    return team_size_dict


# 用一个连续变量计算香农熵
def diversity_shanno_entroy(per):
    if per >0:
        gi=-per*math.log2(per)-(1-per)*math.log2(1-per)
    return gi


def group_bar_chart(team_size_mixed_everymonth_norm_dict_lst,figpath):
    labels = list(range(1,12,5))
    team_size_mixed_everymonth_norm_dict={}

    for j in range(2,7):
        team_size_mixed_everymonth_norm_dict[str(j)]=[]

    for d in team_size_mixed_everymonth_norm_dict_lst:
        for j in range(2,7):
            team_size_mixed_everymonth_norm_dict[str(j)].append(d[str(j)])



    x = np.arange(len(labels))  # the label locations
    width = 0.15  # the width of the bars

    fig, ax = plt.subplots()
    # rects1 = ax.bar(x - width / 2,team_size_mixed_everymonth_dict['1'], width, label='teamsize=1')
    ax.bar(x - width, team_size_mixed_everymonth_norm_dict['2'], width, label='teamsize=2')
    ax.bar(x ,team_size_mixed_everymonth_norm_dict['3'], width, label='teamsize=3')
    ax.bar(x+width, team_size_mixed_everymonth_norm_dict['4'], width, label='teamsize=4')
    ax.bar(x+width*2, team_size_mixed_everymonth_norm_dict['5'], width, label='teamsize=5')
    ax.bar(x + width*3 , team_size_mixed_everymonth_norm_dict['6'], width, label='teamsize>=6')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percentage of Mixed-Gender Teams')
    ax.set_xlabel('Month')
    ax.set_xticks(x, labels)
    ax.legend()

    fig.tight_layout()
    plt.savefig(figpath)
    plt.show()

def group_plot_chart(team_size_mixed_everymonth_dict_lst):
    team_size_mixed_everymonth_dict={}
    for i in range(2,7):
        team_size_mixed_everymonth_dict[str(i)]=[]

    for d in team_size_mixed_everymonth_dict_lst:
        for j in range(2,7):
            team_size_mixed_everymonth_dict[str(j)].append(d[str(j)])

    for k,v in team_size_mixed_everymonth_dict.items():
        if int(k) < 6:
            plt.plot(range(1,12),v,linewidth=3,label="team size="+k)
        else:
            plt.plot(range(1, 12), v, linewidth=3, label="team size>=" + k)
    plt.xlabel("Month")
    plt.ylabel("Percentage of Papers by Team Size")
    plt.legend()
    plt.savefig("Mixed_Team_Size_Change.png")
    plt.show()

def draw_part_team_size_mixed():
    baseurl = '/Users/yizhihenpidehou/Desktop/fdu/Metaverse-Analysis/'

    team_size_mixed_everymonth_norm_dict_lst=[]
    team_size_shannon_everymonth_dict_lst=[]

    for i in range(1,12,5):
        targeturl = baseurl
        dirurl = baseurl
        if i < 10:
            targeturl += "2022-0" + str(i) + "/fourpublisher_arxiv_withsource_updatedauthor2022-0" + str(
                i) + "_withgender.json"
            dirurl += "2022-0" + str(i) + '/'
        else:
            targeturl += "2022-" + str(i) + "/fourpublisher_arxiv_withsource_updatedauthor2022-" + str(
                i) + "_withgender.json"
            dirurl += "2022-" + str(i) + '/'

        request_file = open(targeturl, 'r')
        request_file_str = request_file.read()
        request_file_lst = request_file_str.split("---------------------------------\n")

        # 计算平均shanno
        team_size_dict={}
        total_team_count=0
        for i in range(2,7):
            team_size_dict[str(i)]=[]
        for i in range(0,len(request_file_lst)-1):
            json_str=json.loads(request_file_lst[i])
            gender_lst=json_str["gender"]
            team_size=len(gender_lst)
            female=0
            for gender in gender_lst:
                if gender == 0:
                    female+=1
            if len(gender_lst)> female > 0 :
                total_team_count+=1
                female_percentage=female*1.0/team_size
                gender_diversity=diversity_shanno_entroy(female_percentage)
                if team_size <6:
                    team_size_dict[str(team_size)].append(gender_diversity)
                else:
                    team_size_dict['6'].append(gender_diversity)

        # 统计平均shanno entory
        for k,v in team_size_dict.items():
            team_size_dict[k]=sum(v)*1.0/total_team_count
        print("team_size_dict:",team_size_dict)
        team_size_shannon_everymonth_dict_lst.append(team_size_dict)

        # team size 与 mixed gender的比例
        team_size_mixed_gender_dict_norm = team_size_mixed_gender(request_file_lst,norm=True)

        team_size_mixed_everymonth_norm_dict_lst.append(team_size_mixed_gender_dict_norm)

    # 绘制性别每个月平均比例
    group_bar_chart(team_size_mixed_everymonth_norm_dict_lst,figpath="team_size_mixed.png")
    # 绘制性别平均香农熵变化
    group_bar_chart(team_size_shannon_everymonth_dict_lst,figpath="team_size_shannon.png")

def draw_all_month():
    mixed_gender_percentage_lst = []
    female_research_percentage_lst = []
    team_size_mixed_everymonth_dict_lst=[]

    baseurl = '/Users/yizhihenpidehou/Desktop/fdu/Metaverse-Analysis/'
    for i in range(1, 12):

        targeturl = baseurl
        dirurl = baseurl
        if i < 10:
            targeturl += "2022-0" + str(i) + "/fourpublisher_arxiv_withsource_updatedauthor2022-0" + str(
                i) + "_withgender.json"
            dirurl += "2022-0" + str(i) + '/'
        else:
            targeturl += "2022-" + str(i) + "/fourpublisher_arxiv_withsource_updatedauthor2022-" + str(
                i) + "_withgender.json"
            dirurl += "2022-" + str(i) + '/'

        request_file = open(targeturl, 'r')
        request_file_str = request_file.read()
        request_file_lst = request_file_str.split("---------------------------------\n")
        # 计算女性研究者的比例
        female_research_percentage = female_percentage(request_file_lst)
        female_research_percentage_lst.append(female_research_percentage)

        # mix gender team 的比例
        total_mix=0
        for i in range(0,len(request_file_lst)-1):
            json_str=json.loads(request_file_lst[i])
            gender_lst=json_str["gender"]
            res=team_gender_diversity(gender_lst)
            total_mix+=res
        mixed_gender_percentage=total_mix/(len(request_file_lst)-1)
        mixed_gender_percentage_lst.append(mixed_gender_percentage)

        # team size 与 mixed gender的比例
        team_size_mixed_gender_dict = team_size_mixed_gender(request_file_lst, norm=True)
        team_size_mixed_everymonth_dict_lst.append(team_size_mixed_gender_dict)

    # 绘制混合性别团队的比例
    plt.plot(range(1,12),mixed_gender_percentage_lst,color="black",linewidth=3)
    plt.xlabel("month(1-11)")
    plt.ylabel("Percentage of Mixed-Gender Teams")
    plt.ylim(0,1)
    plt.savefig("Mixed-Gender-Percentage.png")
    plt.show()
    # 女性研究者的比例变化
    plt.plot(range(1, 12), female_research_percentage_lst, color="black", linewidth=3)
    plt.xlabel("month(1-11)")
    plt.ylabel("Percentage of Female Researchers")
    plt.ylim(0, 1)
    plt.savefig("Female-Researchers-Percentage.png")
    plt.show()
    # 各种team size 比例的变化
    group_plot_chart(team_size_mixed_everymonth_dict_lst)




def gender_diversity_pipleline():

    draw_all_month()
    draw_part_team_size_mixed()