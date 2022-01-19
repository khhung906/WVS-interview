import pandas as pd
import math

# preprocess
# load sheet file
df = pd.read_excel("2021 面試時間調查（社員版）(回覆).xlsx", 
    usecols=[
        "你ㄉ大名！", 
        "10/22（五）19:00-21:30", 
        "10/22（五）｜部分時段可以", 
        "10/23（六）9:35-12:25 & 13:30-16:55", 
        "10/23（六）上午都可",
        "10/23（六）下午都可",
        "10/23（六）部分時間可｜上午",
        "10/23（六）部分時間可｜下午",
        "10/24（日）9:00-12:25 & 13:30-16:55",
        "10/24（日）上午都可",
        "10/24（日）下午都可",
        "10/24（日）部分時間可｜上午",
        "10/24（日）部分時間可｜下午"
    ]
)

names = df["你ㄉ大名！"].tolist()
Fri_all = df["10/22（五）19:00-21:30"].tolist()
Fri_p = df["10/22（五）｜部分時段可以"].tolist()
Sat_all = df["10/23（六）9:35-12:25 & 13:30-16:55"].tolist()
Sat_m = df["10/23（六）上午都可"].tolist()
Sat_a = df["10/23（六）下午都可"].tolist()
Sat_p_m = df["10/23（六）部分時間可｜上午"].tolist()
Sat_p_a = df["10/23（六）部分時間可｜下午"].tolist()
Sun_all = df["10/24（日）9:00-12:25 & 13:30-16:55"].tolist()
Sun_m = df["10/24（日）上午都可"].tolist()
Sun_a = df["10/24（日）下午都可"].tolist()
Sun_p_m = df["10/24（日）部分時間可｜上午"].tolist()
Sun_p_a = df["10/24（日）部分時間可｜下午"].tolist()

# total avaliable time: 27
ava_time = {
    'all': 27,
    'start': 0,
    'fri': 4,
    'sat_m': 9,
    'sat_a': 15,
    'sun_m': 21,
    'sun_a': 27,
}

fri = {
    '19:00-19:30': 0,
    '19:40~20:10': 1,
    '20:20~20:50': 2,
    '21:00~21:30': 3
}

sat = {
    '9:35~10:05': 4,
    '10:10~10:40': 5,
    '10:45~11:15': 6,
    '11:20~11:50': 7,
    '11:55~12:25': 8,
    '13:30~14:00': 9,
    '14:05~14:35': 10,
    '14:40~15:10': 11,
    '15:15~15:45': 12,
    '15:50~16:20': 13,
    '16:25~16:55': 14 
}

sun = {
    '9:00~9:30': 15,
    '9:35-10:05': 16,
    '10:10~10:40': 17,
    '10:45~11:15': 18,
    '11:20~11:50': 19,
    '11:55~12:25': 20,
    '13:30~14:00': 21,
    '14:05~14:35': 22,
    '14:40~15:10': 23,
    '15:15~15:45': 24,
    '15:50~16:20': 25,
    '16:25~16:55': 26,
}

p_cnt = len(names)
data = []
new_ppl = {}

for i in range(p_cnt):
    new_ppl = {}
    new_ppl['name'] = names[i].split()[0]
    new_ppl['time_table'] = []

    # Friday
    if Fri_all[i] == "所有時段都可以":
        for j in range(ava_time['start'], ava_time['fri']): 
            new_ppl['time_table'].append(j)
    elif Fri_all[i] == "部分時段可以（下一頁填寫詳細時間）":
        if Fri_p[i] != '都不行...':
            times = Fri_p[i].split(', ')
            for t in times:
                new_ppl['time_table'].append(fri[t])
    
    # Saturday
    if Sat_all[i] == "全天都可以":
        for j in range(ava_time['fri'], ava_time['sat_a']): 
            new_ppl['time_table'].append(j)

    elif Sat_all[i] == "上午時段都可以（下一頁填寫下午可面試時間）":
        for j in range(ava_time['fri'], ava_time['sat_m']): 
            new_ppl['time_table'].append(j)
        if Sat_m[i] != '都不行...':
            times = Sat_m[i].split(', ')
            for t in times:
                new_ppl['time_table'].append(sat[t])

    elif Sat_all[i] == "下午時段都可以（下一頁填寫上午可面試時間）":
        for j in range(ava_time['sat_a'], ava_time['sat_m']): 
            new_ppl['time_table'].append(j)
        if Sat_a[i] != '都不行...':
            times = Sat_a[i].split(', ')
            for t in times:
                new_ppl['time_table'].append(sat[t])

    elif Sat_all[i] == "只有幾個時段可以（下一頁填寫詳細時間）":
        if Sat_p_m[i] != '都不行...':
            times = Sat_p_m[i].split(', ')
            for t in times:
                new_ppl['time_table'].append(sat[t])

        if Sat_p_a[i] != '都不行...':
            times = Sat_p_a[i].split(', ')
            for t in times:
                new_ppl['time_table'].append(sat[t])

    #Sunday
    if Sun_all[i] == "全天都可以":
        for j in range(ava_time['sat_a'], ava_time['sun_a']): 
            new_ppl['time_table'].append(j)

    elif Sun_all[i] == "上午時段都可以（下一頁填寫下午可面試時間）":
        for j in range(ava_time['sat_a'], ava_time['sun_m']): 
            new_ppl['time_table'].append(j)
        if Sun_m[i] != '都不行...':
            times = Sun_m[i].split(', ')
            for t in times:
                new_ppl['time_table'].append(sun[t])

    elif Sun_all[i] == "下午時段都可以（下一頁填寫上午可面試時間）":
        for j in range(ava_time['sun_m'], ava_time['sun_a']): 
            new_ppl['time_table'].append(j)
        if Sun_a[i] != '都不行...':
            times = Sun_a[i].split(', ')
            for t in times:
                new_ppl['time_table'].append(sun[t])

    elif Sun_all[i] == "只有幾個時段可以（下一頁填寫詳細時間）":
        if Sun_p_m[i] != '都不行...':
            times = Sun_p_m[i].split(', ')
            for t in times:
                new_ppl['time_table'].append(sun[t])

        if Sun_p_a[i] != '都不行...':
            times = Sun_p_a[i].split(', ')
            for t in times:
                new_ppl['time_table'].append(sun[t])

    data.append(new_ppl)

# cnt_times = [0]*ava_time['all']
# for i in range(p_cnt):
#     for j in range(ava_time['all']):
#         if data[i]['time_table'][j]: cnt_times[j]+=1

for i in range(p_cnt):
    cnt = 0
    data[i]['spare_time'] = len(data[i]['time_table'])
    if data[i]['time_table']: data[i]['first_time'] = data[i]['time_table'][0]
    else :data[i]['first_time'] = -1

# sort with time table -> most time -> least time (early time -> late time)
def sort_time(elem):
    return elem['spare_time']*100+elem['first_time']

data.sort(key=sort_time)

f = open('data.txt', 'w')
for i in range(len(data)):
    line = ''
    # line += ' '*(20-len(data[i]['name']))
    for j in range(ava_time['all']):
        line += ' '
        if j in data[i]['time_table']: line += 'o'
        else: line += 'x'
    line += ' '*5+data[i]['name']
    line += '\n'
    f.write(line)

result = open('result.txt', 'w')
k = 0
while data[k]['spare_time'] == 0:
    result.write(data[k]['name']+' no free time\n')
    data.pop(0)

UPPER_BOUND = 3

cnts = [0]*ava_time['all']
alloc = {i:[] for i in range(ava_time['all'])}
def solve(p_idx):
    if p_idx >= len(data):
        return True
    for o in data[p_idx]['time_table']:
        if cnts[o] >= UPPER_BOUND:
            continue
        cnts[o] += 1
        alloc[o].append(data[p_idx]['name'])
        if solve(p_idx+1):
            return True
        cnts[o] -= 1
        alloc[o].remove(data[p_idx]['name'])
    return False

# output result
times = ['Friday '+t for t in fri.keys()] + ['Saturday '+t for t in sat.keys()] + ['Sunday '+t for t in sun.keys()]

if solve(0):
    for i in range(ava_time['all']):
        line = times[i] + ' '*3
        for p in alloc[i]:
            line += ' '+p
        line += '\n'
        result.write(line)
else:
    print('Match Fails')