# Program Name: NSGA-II.py
# Description: This is a python implementation of Prof. Kalyanmoy Deb's popular NSGA-II algorithm
# Author: Haris Ali Khan 
# Supervisor: Prof. Manoj Kumar Tiwari

# Importing required modules
import math
import random
import matplotlib.pyplot as plt


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
        currentTime += intervalQueue[i]
        taskStartTime[taskType - 1].append(currentTime)
        currentTime += duration[taskType - 1]
    print(chromosome,'的taskStartTime',taskStartTime)
    # 2 calculate delay loss
    # 2.1 calculate Delay between  two scheduling for each task
    #    (delay = actual interval - expect interval)
    delayQueue = [[] for i in range(len(cycle))]  # delayQueue:[[0, 0], [0, 0], [70]]
    for i in range(len(cycle)):
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
    totalLoopNum = sum(loopNums)

    for i in range(size):
        temp = [0 for i in range(len(cycle))]
        while (sum(temp) < totalLoopNum):
            index = random.randint(0, len(cycle) - 1)
            if (temp[index] < loopNums[index]):
                temp[index] += 1
                chromosomes[i].append(index+1)
    for i in range(size):
        j = 0
        while (j < totalLoopNum):
            interval = random.randint(0, int(cycle[chromosomes[i][j]-1]))
            chromosomes[i].append(interval)
            j += 1

    return chromosomes


#####################################################################################

# First function to optimize
# 目标函数1
def function1(x):
    value = -x ** 2
    return value


# Second function to optimize
# 目标函数2
def function2(x):
    value = -(x - 2) ** 2
    return value


# Function to find index of list
# 确定a在list中下标（todo:折半查找优化）
def index_of(a, list):
    for i in range(0, len(list)):
        if list[i] == a:
            return i
    return -1


def sort_by_values(list1, values):
    """" 
      根据某一个目标函数，对同一等级个体排序
    :param list1 非支配排序后的同一等级的个体下标列表
    :param values 某一个目标函数的值
    :return  排序后的下标列表
    """
    sorted_list = []
    while (len(sorted_list) != len(list1)):
        if index_of(min(values), values) in list1:
            sorted_list.append(index_of(min(values), values))
        values[index_of(min(values), values)] = math.inf
    return sorted_list


# Function to carry out NSGA-II's fast non dominated sort
# 快速非支配排序
def fast_non_dominated_sort(values1, values2, values3):
    S = [[] for i in range(0, len(values1))]
    front = [[]]
    n = [0 for i in range(0, len(values1))]
    rank = [0 for i in range(0, len(values1))]

    for p in range(0, len(values1)):
        S[p] = []
        n[p] = 0
        for q in range(0, len(values1)):
            # if (values1[p] > values1[q] and values2[p] > values2[q]) or (
            #         values1[p] >= values1[q] and values2[p] > values2[q]) or (
            #         values1[p] > values1[q] and values2[p] >= values2[q]):
            if (values1[p] > values1[q] and values2[p] > values2[q] and values3[p] > values3[q] ):
                if q not in S[p]:
                    S[p].append(q)
            # elif (values1[q] > values1[p] and values2[q] > values2[p]) or (
            #         values1[q] >= values1[p] and values2[q] > values2[p]) or (
            #         values1[q] > values1[p] and values2[q] >= values2[p]):
            elif (values1[q] > values1[p] and values2[q] > values2[p] and values3[q] > values3[p]):
                n[p] = n[p] + 1
        if n[p] == 0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)

    i = 0
    while (front[i] != []):
        Q = []
        for p in front[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                if (n[q] == 0):
                    rank[q] = i + 1
                    if q not in Q:
                        Q.append(q)
        i = i + 1
        front.append(Q)

    del front[len(front) - 1]
    return front


# Function to calculate crowding distance
def crowding_distance(values1, values2,values3, front):
    """
    根据多目标，获得某一层非支配排序的距离
    :param values1: 目标函数1的值
    :param values2: 目标函数2的值
    :param values3: 目标函数3的值
    :param front:  非支配排序后的某一层个体列表
    :return: 该层个体距列表
    """
    distance = [0 for i in range(0, len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    sorted3 = sort_by_values(front, values3[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    for k in range(1, len(front) - 1):
        if(max(values1) - min(values1) != 0):
            distance[k] = distance[k] + (values1[sorted1[k + 1]] - values2[sorted1[k - 1]]) / (max(values1) - min(values1))
    for k in range(1, len(front) - 1):
        if (max(values2) - min(values2) != 0):
            distance[k] = distance[k] + (values1[sorted2[k + 1]] - values2[sorted2[k - 1]]) / (max(values2) - min(values2))
    for k in range(1, len(front) - 1):
        if (max(values3) - min(values3) != 0):
            distance[k] = distance[k] + (values1[sorted3[k + 1]] - values2[sorted3[k - 1]]) / (max(values3) - min(values3))
    return distance


# Function to carry out the crossover
def crossover(a, b):
    print('开始交叉a=',a,'b=',b)
    r = random.randint(0,len(a)/2)
    print('交叉r值',r)
    result = []
    copy_b = b.copy()[:int(len(b)/2)]

    for i in range(r):
        result.append(a[i])
        copy_b.remove(a[i])
    print('去掉a中交叉用到的基金，b为',copy_b)
    for i in range(r,int(len(a)/2)):
        result.append(copy_b[i-r])
    for i in range(int(len(a)/2),int(len(a)/2)+r):
        result.append(a[i])
    for i in range(int(len(a)/2)+r,len(a)):
        result.append(b[i])
    print('交叉结果',result)
    return mutation(result)

# Function to carry out the mutation operator
def mutation(solution):
    print(solution,'开始变异')
    mutation_prob = random.random()
    if mutation_prob < 0.8:
        #任务队列突变
        mutation_position_1_1 = random.randint(0,len(solution)/2-1)
        mutation_position_1_2 = random.randint(0, len(solution) / 2-1 )
        print('交换点',mutation_position_1_1,mutation_position_1_2)
        temp = solution[mutation_position_1_1]
        solution[mutation_position_1_1] = solution[mutation_position_1_2]
        solution[mutation_position_1_2] = temp

        temp = solution[int(len(solution)/2)+mutation_position_1_1]
        solution[int(len(solution)/2)+mutation_position_1_1] = solution[int(len(solution)/2)+mutation_position_1_2]
        solution[int(len(solution) / 2) + mutation_position_1_2] = temp


        mutation_position_2 = random.randint(0,len(solution)/2-1)
        mutation_value1 = random.randint(1,len(cycle))
        mutation_value2 = random.randint(0,math.fabs(maxTolerateDelays[solution[mutation_position_2]-1]-solution[mutation_position_2]))
        solution[int(len(solution)/2+mutation_position_2)] = mutation_value2
    print('变异结果',solution)
    return solution


# main函数开始
pop_size = 50
max_gen = 900
preferences = [6, 3, 2]
maxTolerateDelays = [50, 50, 100]
cycle = [200, 200, 300]
duration = [40, 50, 80]

chromosomes = initChromosome(cycle, pop_size)
print('1len(chromosomes)',len(chromosomes))
print('种群为',chromosomes)
# Initialization
min_x = -55
max_x = 55
gen_no = 0
while (gen_no < max_gen):
    # 计算目标函数值
    function1_values = []
    function2_values = []
    function3_values = []
    for chromosome in chromosomes:
        print(chromosome)
        taskQueue, delayQueue = chromosome2delayQueueAndTaskQueue(chromosome)
        print('taskQueue: ',taskQueue)
        print('delayQueue: ',delayQueue)
        # 1 计算延迟损失
        function1_values.append(delayQueue2delayLoss(delayQueue))
        # 2 计算公平性
        function2_values.append(function_fair(delayQueue))
        # 3 计算能耗
        function3_values.append(function_energy_consumption(taskQueue, duration, delayQueue))
    # 快速非支配排序，生成排序列表（列表每一项是相同Rank个体组成的列表）
    non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:], function2_values[:],
                                                            function3_values[:])
    print(non_dominated_sorted_solution)
    print("The best front for Generation number ", gen_no, " is")
    for valuez in non_dominated_sorted_solution[0]:
        print((chromosomes[valuez]), end=" ")
    print("\n")
    print('2len(chromosomes)', len(chromosomes))
    # 对每一层计算拥挤度
    crowding_distance_values = []
    for i in range(0, len(non_dominated_sorted_solution)):  #
        crowding_distance_values.append(
            crowding_distance(function1_values[:], function2_values[:],function3_values[:], non_dominated_sorted_solution[i][:]))
    print('2.5len(chromosomes)', len(chromosomes))
    chromosomes2 = chromosomes[:]
    # 随机生成后代（todo:优化选择机制）
    while (len(chromosomes2) != 2 * pop_size):
        a1 = random.randint(0, pop_size - 1)
        b1 = random.randint(0, pop_size - 1)
        print('3len(chromosomes)', len(chromosomes))
        print(len(chromosomes),a1,b1)
        chromosomes2.append(crossover(chromosomes[a1], chromosomes[b1]))
    # 对两代种群计算目标值
    function1_values2 = []
    function2_values2=[]
    function3_values2 = []
    for chromosome in chromosomes2:
        taskQueue, delayQueue = chromosome2delayQueueAndTaskQueue(chromosome)
        print('染色体',chromosome)
        print('任务队列',taskQueue)
        print('延迟队列', delayQueue)
        # 1 计算延迟损失
        function1_values2.append(delayQueue2delayLoss(delayQueue))
        # 2 计算公平性
        function2_values2.append(function_fair(delayQueue))
        # 3 计算能耗
        function3_values2.append(function_energy_consumption(taskQueue, duration, delayQueue))

    # 根据目标值，求得非支配层次列表
    non_dominated_sorted_solution2 = fast_non_dominated_sort(function1_values2[:], function2_values2[:], function3_values2[:])
    crowding_distance_values2 = []
    for i in range(0, len(non_dominated_sorted_solution2)):  # 计算父代和子代的拥挤度
        crowding_distance_values2.append(
            crowding_distance(function1_values2[:], function2_values2[:], function3_values2[:],non_dominated_sorted_solution2[i][:]))
    print('4len(chromosomes)', len(chromosomes))
    # 重新选取新的种群
    new_solution = []
    for i in range(0, len(non_dominated_sorted_solution2)):
        non_dominated_sorted_solution2_1 = [#获取第i层的个体下标列表？？觉得没必要 range(0,len(non_dominated_sorted_solution2[i]))
            index_of(non_dominated_sorted_solution2[i][j], non_dominated_sorted_solution2[i]) for j in
            range(0, len(non_dominated_sorted_solution2[i]))]
        front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])#根据目标函数2对个体排序（结果是个体下标列表）
        front = [non_dominated_sorted_solution2[i][front22[j]] for j in#根据下标列表获取个体
                 range(0, len(non_dominated_sorted_solution2[i]))]
        front.reverse()
        for value in front:
            new_solution.append(value)
            if (len(new_solution) == pop_size):
                break
        if (len(new_solution) == pop_size):
            print('2len(new_solution)', len(new_solution))
            #chromosomes = [chromosomes2[i] for i in new_solution]
            break
        print('len(new_solution)',len(new_solution))
        print('5len(chromosomes)', len(chromosomes))
        chromosomes = [chromosomes2[i] for i in new_solution]
        print('6len(chromosomes)', len(chromosomes))
    gen_no = gen_no + 1

# Lets plot the final front now
function1 = [i * -1 for i in function1_values]
function2 = [j * -1 for j in function2_values]
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.scatter(function1, function2)
plt.show()
