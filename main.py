import pandas as pd
import math

# initiate parameters
LOWER_BOUND = 4
UPPER_BOUND = 10

# load sheet file
df = pd.read_excel("面試時間調查.xlsx", usecols=["你ㄉ大名！", "你可以ㄉ面試時間！"])
names = df["你ㄉ大名！"].tolist()
times = df["你可以ㄉ面試時間！"].tolist()

# change data to 
# interval dict: {['time': number]}
# data: [[avaliable times], [], ...]
# people: ['name1', 'name2', ...]

intervals = []
namelen = len(names)

# if intervals has been initialized this can be delete
for i in range(namelen):
    # check for nan cell
    if names[i] and names[i] == names[i]:  
        for t in times[i].split(', '):
            if t not in intervals:
                intervals.append(t)
intervals.sort()
interval_dict = dict()
for idx, t in enumerate(intervals):
    interval_dict[t] = idx

data = []
people = []
for i in range(namelen):
    if names[i] and names[i] == names[i]:  
        people.append(names[i])
        data.append(sorted(list(map(lambda t: interval_dict[t], times[i].split(', '))), reverse=True))  

# print(data)
# proccess 
cnts = [0]*len(intervals)
alloc = [-1]*len(people)

def make_order(list):
    def order(elem):
        if cnts[elem] < LOWER_BOUND:
            return cnts[elem]
        else:
            return -cnts[elem]
    sorted_list = sorted(list, key=order, reverse=True)
    return sorted_list

def find(p_idx):
    # print(p_idx)
    if p_idx >= len(data):
        return True
    order = make_order(data[p_idx])
    for o in order:
        if cnts[o] >= UPPER_BOUND:
            continue
        cnts[o] += 1
        alloc[p_idx] = o
        if find(p_idx+1):
            return True
        cnts[o] -= 1
        alloc[p_idx] = -1
    return False

# output result
if find(0):
    for idx, p in enumerate(people):
        print(p+':'+intervals[alloc[idx]])
    print('-'*100)
    for id, i in enumerate(intervals):
        t = ''
        for idx in range(len(people)):
            if alloc[idx] == id:
                t += people[idx]+' '
        print(i+':'+t)
else:
    print('Match Fails')

