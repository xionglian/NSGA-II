#染色体到目标函数值的转换
#by xionglian 2019年3月14日

#返回element在list中下标
def indexOf(element,list):
    for i in range(0,len(list)):
        if list[i] == element:
            return i
    return -1
#延迟损失函数
def function_Dealy_Loss(delay,maxTolerateDelay,preference):
    return delay*preference if delay< maxTolerateDelay else maxTolerateDelay*preference+(delay-maxTolerateDelay)**preference
#延迟损失函数
def function_fair(delayQueue):
    max = delayQueue[0][0]
    for e in delayQueue:
        for ele in e:
            if(ele>max):
                max = ele
    return max
#能耗函数
def function_energy_consumption(taskQueue,duration,delayQueue):
    runTime =0
    sleepTime = 0
    for e in delayQueue:
        for ele in e:
            sleepTime += ele
    for i in taskQueue:
        runTime += duration[i-1]
    return sleepTime/(sleepTime+runTime)


preferences = [6,3,2]
maxTolerateDelays=[50,50,100]
cycle = [200,200,300]
duration = [40,50,80]
chromosome = [2,1,3,2,1,2,1,3,0,0,0,0,0,110,0,0]


# 1 根据染色体生成任务开始执行列表
# 1.1 分割染色体为任务排序队列和任务间隔队列
taskTypeNum = int(len(duration))
taskQueueNum = int(len(chromosome)/2)
taskQueue = chromosome[:taskQueueNum]
intervalQueue = chromosome[taskQueueNum:]

# 1.2 获取每一个任务开始执行列表
currentTime = 0;
#task[i]表示第i+1个任务的开始执行列表
taskStartTime=[[] for i in range(taskTypeNum)]#taskStartTime:[[50, 220, 420], [0, 170, 260], [90, 460]]
for i in range(taskQueueNum):
    taskType = taskQueue[i]
    taskStartTime[taskType-1].append(currentTime)
    currentTime += (duration[taskType-1] + intervalQueue[i])
print(u'taskStartTime:{}'.format(taskStartTime))

# 2 calculate delay loss
# 2.1 calculate Delay between  two scheduling for each task
#    (delay = actual interval - expect interval)
delayQueue = [[] for i in range(taskType)]#delayQueue:[[0, 0], [0, 0], [70]]
for i in range(taskType):
    for j in range(len(taskStartTime[i])-1):
        actualInterval = taskStartTime[i][j+1]-taskStartTime[i][j]
        delay = 0 if actualInterval - cycle[i]<0 else actualInterval - cycle[i]
        delayQueue[i].append(delay)
print(u'delayQueue:{}'.format(delayQueue))
# 2.2 According to the delay time,calculate delay loss
delayLoss = 0
for i in range(len(delayQueue)):
    for j in range(len(delayQueue[i])):
        delayLoss += function_Dealy_Loss(
            delayQueue[i][j],maxTolerateDelays[i],preferences[i])


# 3 计算公平性
fair = function_fair(delayQueue)

# 4 计算能耗
consu = function_energy_consumption(taskQueue,duration,delayQueue)

print(delayLoss)
print(fair)
print(consu)





