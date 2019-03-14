# NSGA-II
NSGA is a popular non-domination based genetic algorithm for multi-objective optimization. 
It is a very effective algorithm but has been generally criticized for its computational complexity, lack of elitism and for choosing the optimal parameter value for sharing parameter σshare. 
A modified version, NSGA II  was developed, which has a better sorting algorithm , incorporates elitism and no sharing parameter needs to be chosen a priori. 
This is a python implementation of NSGA-II algorithm
A所有目标都优于B时，就说A支配了B，否则A和B就是一个非支配的关系，Rank值越小的解越好。
种群中所有不被任何其他解支配的解构成了非支配前沿(Pareto最优解)
为了保证解的多样性，我们往往希望同一Rank层中的解能够相互分开，所以设置了 拥挤度 这个概念，
认为 解之间距离开的解比解之间距离小的解更好 拥挤距离排序用于保持解的多样性。 每个个体的拥挤距离是通过计算与其相邻的两个个体在每个子目标函数上的距离差之和来求取


# rcpsp是一种资源受限项目调度问题
本文是解决物联网中资源受限的MCU中的驱动调度问题

