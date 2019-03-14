# 染色体到目标函数值的转换
# by xionglian 2019年3月14日

import math
import random


# 求a与b最小公倍数
def lcm(a, b):
    return int(a * b / math.gcd(a, b))


#
def lcmList(list):
    if (len(list) < 1):
        return -1
    if (len(list) == 1):
        return list[0]
    result = list[0]
    for i in range(len(list) - 1):
        result = lcm(result, list[i + 1])
    return result


# 返回element在list中下标
def indexOf(element, list):
    for i in range(0, len(list)):
        if list[i] == element:
            return i
    return -1


# 单个任务的延迟损失函数
def function_Dealy_Loss(delay, maxTolerateDelay, preference):
    return delay * preference if delay < maxTolerateDelay else maxTolerateDelay * preference + (
                                                                                               delay - maxTolerateDelay) ** preference


# 计算染色体全部损失（染色体包含多个任务）
def delayQueue2delayLoss(delayQueue):
    # 2.2 According to the delay time,calculate delay loss
    delayLoss = 0
    for i in range(len(delayQueue)):
        for j in range(len(delayQueue[i])):
            delayLoss += function_Dealy_Loss(
                delayQueue[i][j], maxTolerateDelays[i], preferences[i])
    return delayLoss


# 公平函数
def function_fair(delayQueue):
    max = delayQueue[0][0]
    for e in delayQueue:
        for ele in e:
            if (ele > max):
                max = ele
    return max


# 能耗函数
def function_energy_consumption(taskQueue, duration, delayQueue):
    runTime = 0
    sleepTime = 0
    for e in delayQueue:
        for ele in e:
            sleepTime += ele
    for i in taskQueue:
        runTime += duration[i - 1]
    return sleepTime / (sleepTime + runTime)


def chromosome2delayQueueAndTaskQueue(chromosome):
    # 1 根据染色体生成任务开始执行列表
    # 1.1 分割染色体为任务排序队列和任务间隔队列
    print(chromosome)
    taskTypeNum = int(len(duration))
    taskQueueNum = int(len(chromosome) / 2)
    taskQueue = chromosome[:taskQueueNum]
    intervalQueue = chromosome[taskQueueNum:]

    # 1.2 获取每一个任务开始执行列表
    currentTime = 0;
    # task[i]表示第i+1个任务的开始执行列表
    taskStartTime = [[] for i in range(taskTypeNum)]  # taskStartTime:[[50, 220, 420], [0, 170, 260], [90, 460]]
    for i in range(taskQueueNum):
        taskType = taskQueue[i]
        currentTime +=  intervalQueue[i]
        taskStartTime[taskType - 1].append(currentTime)
        currentTime += duration[taskType - 1]

    print(u'taskStartTime:{}'.format(taskStartTime))
    # 2 calculate delay loss
    # 2.1 calculate Delay between  two scheduling for each task
    #    (delay = actual interval - expect interval)
    delayQueue = [[] for i in range(taskType)]  # delayQueue:[[0, 0], [0, 0], [70]]
    for i in range(taskType):
        for j in range(len(taskStartTime[i]) - 1):
            actualInterval = taskStartTime[i][j + 1] - taskStartTime[i][j]
            delay = 0 if actualInterval - cycle[i] < 0 else actualInterval - cycle[i]
            delayQueue[i].append(delay)
    return taskQueue, delayQueue


def initChromosome(cycle, size):
    expectBigLoopTime = lcmList(cycle)
    chromosomes = [[] for i in range(size)]
    if (-1 == expectBigLoopTime):
        return []
    loopNums = []
    for e in cycle:
        loopNums.append(int(expectBigLoopTime / e))
    print(loopNums)
    totalLoopNum = sum(loopNums)

    for i in range(size):
        temp = [0 for i in range(len(cycle))]
        while(sum(temp)<totalLoopNum):
            index = random.randint(0, len(cycle) - 1)
            if(temp[index]<loopNums[index]):
                temp[index] += 1
                chromosomes[i].append(index)
    for i in range(size):
        j = 0
        while(j < totalLoopNum):
            interval = random.randint(0,int(cycle[chromosomes[i][j]]))
            chromosomes[i].append(interval)
            j += 1

    return chromosomes

preferences = [6, 3, 2]
maxTolerateDelays = [50, 50, 100]
cycle = [200, 200, 300]
duration = [40, 50, 80]



chromosomes = initChromosome(cycle,1000)
taskQueue, delayQueue = chromosome2delayQueueAndTaskQueue(chromosomes[0])

#taskQueue:  [1, 2, 1, 2, 3, 1, 2, 3]
#delayQueue:  [[40, 194], [89, 76], [0]]
taskQueue, delayQueue = chromosome2delayQueueAndTaskQueue([2, 2, 2, 1, 3, 1, 1, 3, 35, 24, 35, 9, 24, 14, 28, 22] )
print(taskQueue)
print(delayQueue)
# 3 计算延迟损失
delayLoss = delayQueue2delayLoss(delayQueue)
# 3 计算公平性
fair = function_fair(delayQueue)

# 4 计算能耗
consu = function_energy_consumption(taskQueue, duration, delayQueue)

print(delayLoss)
print(fair)
print(consu)