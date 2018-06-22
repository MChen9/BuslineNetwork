import pickle
import pandas as pd
import math
import numpy as np



'''Geometric Manhattan Distance'''
def GeoManhattanDistance(start, end):
    slon, slat = start[0], start[1]
    elon, elat = end[0], end[1]
    avglat = (slat + elat)/2
    return (math.cos(math.radians(avglat))) * 6367000.0 * (abs(elon - slon)) * math.pi/180 \
           + 6367000.0 * abs(elat - slat) * math.pi/180



'''all bus stops along with bus lines '''
with open('pickle_example.pickle','rb') as r:
    c=pickle.load(r)

BusStop = {}
for ele in c:
    try:
        key = ele['buslines'][0]['name'].encode("utf8").decode('utf8')
        value = [[float(y) for y in x['location'].split(',')] for x in ele['buslines'][0]['busstops']]
        BusStop[key] = value
    except:
        pass


'''test one line'''
'''
# calculate distance between two nodes along a bus line
DistList = []
for i in range(len(BusStop['大亚湾317路A线(惠阳海关--惠阳海关)'])- int(1)):
    start = BusStop['大亚湾317路A线(惠阳海关--惠阳海关)'][i]
    end = BusStop['大亚湾317路A线(惠阳海关--惠阳海关)'][i + int(1)]
    dist = GeoManhattanDistance(start, end)
    DistList.append(dist)

# end node of 30 min by bus
y = 0
x = 0
while y <= 4980:
    y = y + DistList[x]
    x = x + 1

print(x) # end node
'''


'''test one stop'''
'''
# find other bus line pass the stop
BusLineHub = []
BusLineInt = BusStop['大亚湾317路A线(惠阳海关--惠阳海关)'][0]
for Key, Value in BusStop.items():
    if BusLineInt in Value:
        BusLineHub.append(Key)
    else:
        pass


# find the index of the stop in this bus line
n = 0
for i in BusStop[BusLineHub[1]]:
    if i == BusLineInt:
        break
    else:
        n = n + 1


# if it is the last stop, then make no sense
if n == len(BusStop[BusLineHub[1]]) - 1:
    print('This is the last stop of' + BusLineHub[1])
else:
    DistList = []
    for i in range(n, len(BusStop[BusLineHub[1]]) - int(1)):
        start = BusStop[BusLineHub[1]][i]
        end = BusStop[BusLineHub[1]][i + int(1)]
        dist = GeoManhattanDistance(start, end)
        DistList.append(dist)




# end node of 30 min by bus
y = 0
x = 0
while y <= 4980:
    try:
        y = y + DistList[x]
        x = x + 1
    except ValueError:
        pass

print(BusStop[BusLineHub[1]][x]) # end node coordinates
'''

'''test one line traverse all stops'''
# branches of every stop along with a bus line
def LineBranch(buslinename):
    BusLineHub = {}
    for coord in BusStop[buslinename]:
        BusLineHub2 = []
        for key, value in BusStop.items():
            if coord in value:
                BusLineHub2.append(key)
            else:
                pass
        key = tuple(coord) # list cannot be key, use tuple()
        value = BusLineHub2
        BusLineHub[key] = value
    return BusLineHub
# stop location(coordinates) and return bus line names as a dict






# find the index of the stop(intersection node) of corresponding bus line
def StopIndex(BusLineHub):
    stopindex = {}
    for coord, namelist in BusLineHub.items():
        stopindex1 = {}
        for name in namelist:
            n = 0
            for i in BusStop[name]:
                if tuple(i) == coord:
                    break
                else:
                    n = n + 1
            key = name
            value = n
            stopindex1[key] = value
        Key = coord
        Value = stopindex1
        stopindex[Key] = Value
    return stopindex





# if it is the last stop, then make no sense
'''calculate distance between nodes by sequence from branch nodes'''
def SequenceDistance(stopindex):
    DistList = {}
    for coord, indexdict in stopindex.items():
        DistList1 = {}
        for busstop, n in indexdict.items():
            if n == len(BusStop[busstop]) - 1:
                print('This is the last stop of' + busstop)
            else:
                DistList2 = []
                for i in range(n, len(BusStop[busstop]) - int(1)):
                    start = BusStop[busstop][i]
                    end = BusStop[busstop][i + int(1)]
                    dist = GeoManhattanDistance(start, end)
                    DistList2.append(dist)
            key = busstop
            value = DistList2
            DistList1[key] = value
        Key = coord
        Value = DistList1
        DistList[Key] = Value
    return DistList


a = LineBranch('大亚湾317路A线(惠阳海关--惠阳海关)')
b = StopIndex(a)
c = SequenceDistance(b)


# end node of 30 min by bus
'''find which node is the end node of 30min drive'''
DisList = c
EndNodeIndex = {}
i = 0
for coord, distlist in DisList.items(): #branches of every stop of '大亚湾317路A线(惠阳海关--惠阳海关)'
    if i == 0:
        EndNodeIndex1 = {}
        for busline, distance in distlist.items(): # '大亚湾':[..],  ' ':[..]
            y = 0  # change initial distance
            x = 0  # from stop i
            while y <= 4980:
                y = y + distance[x]
                x = x + 1
            key = busline
            value = x
            EndNodeIndex1[key] = value
        i += 1
    else:
        EndNodeIndex2 = {}
        for busline, distance in distlist.items(): # '大亚湾':[..],  ' ':[..]
            y = 0  # change initial distance
            x = 0  # from stop i
            while y <= 4980:
                y = y + distance[x]
                x = x + 1
            key = busline
            value = x
            EndNodeIndex1[key] = value
    Key = coord
    Value = EndNodeIndex1
    EndNodeIndex[Key] = Value



'''
    EndNode = []
    for coord, busline in EndNodeIndex.items():
        EndNode1 = []
        for key, value in busline:
            EndNode1.append(BusStop[key][value[0]])
        EndNode.append(EndNode1)
'''







pass