import random
import copy
import pulp as pulp
import matplotlib.pyplot as plt
import time


# 生成数据
def gene_data(data_size=100):
    data = [random.random() for i in range(data_size)]
    # 变为集合
    data = set(data)
    U = copy.deepcopy(data)
    F = []

    # 产生第一个20的集合
    init_S_size = 20
    # 在data中选出20个元素
    s = random.sample(data, init_S_size)
    s = set(s)
    F.append(s)
    union_s = copy.deepcopy(s)
    data = data.difference(s) #difference 差集

    # 产生大小随机的集合
    while len(data) > 0:
        if len(data) >= init_S_size:
            # 产生1到20的随机数n
            n = random.randint(1, init_S_size)
            # 产生1到n的随机数k
            k = random.randint(1, n)
            # 在原数据中取k个
            x = random.sample(data, k)
            # 在采样的点中取n-k个
            n_x = random.sample(union_s, n - k)
            s = set(x)
            F.append(set(x + n_x))
            # print(len(s))
            union_s = union_s.union(s)
            data = data.difference(s)
        else:
            s = copy.deepcopy(data)
            union_s = union_s.union(s)
            F.append(s)
            # 有点迷
            data = data.difference(s)

    F_y = len(U) - len(F)
    for i in range(F_y):
        n = random.randint(1, init_S_size)
        x = random.sample(U, n)
        s = set(x)
        F.append(s)

    return U, F


# 贪心集合覆盖
def greedy_covers(U,F):
    # U, F = gene_data(data_size)
    res = []
    union_C = []
    while len(U) > 0:

        s = None
        l = 0
        for f in F: # 找到并集大小最大的子集
            t = U & f  #并集
            if len(t) > l:
                l = len(t)
                s = t
        res.append(s)
        union_C.extend(s)
        U = U.difference(s)
    # print(res)
    print(len(res))  # 解的个数

    print(len(set(union_C)))
    return res


def solve_ilp(target, constraints):
    prob = pulp.LpProblem('LP1', pulp.LpMinimize)
    prob += target
    for cons in constraints:
        prob += cons
    status = prob.solve()
    if status != 1:
        # print 'status'
        # print status
        return None
    else:
        res = [None] * len(target)
        for v in prob.variables():
            s = v.name
            i = eval(s[1:])

            res[i] = v.varValue
        return res
        # return [v.varValue for v in prob.variables()]


# 通过线性规划进行求解
def LP(U,F):
    # u为数据,F为集合
    # U, F = gene_data(data_size)
    U = list(U)
    F = list(F)

    XS = []
    # xs设置
    for i in range(len(U)):
        u = U[i]
        xs = []
        for j in range(len(F)):
            s = F[j]
            if u in s:
                xs.append(1)
            else:
                xs.append(0)
        XS.append(xs)

    # 计算出元素出现的最大频率的倒数
    max_f = 1 / max([sum(item) for item in XS])
    print("元素出现的最大频率的倒数：",max_f)
    V_NUM = len(F)

    # 生成变量
    variables = [pulp.LpVariable('X%d' % i, lowBound=0, cat=pulp.LpContinuous) for i in range(V_NUM)]
    target = pulp.lpSum([variables[i] for i in range(V_NUM)])

    # 约束条件
    constraints = []
    for xs in XS:
        constraints.append(pulp.lpSum([xs[i] * variables[i] for i in range(V_NUM)]) >= 1.0)
    #   求解问题
    result = solve_ilp(target, constraints)
    print(result)

    # 检验每个条件都大于1
    # t = []
    # for xs in XS:
    #     t.append(sum([xs[i] * result[i] for i in range(V_NUM)]))
    # for i in range(len(t)):
    #     if t[i] < 1:
    #         print("i", i , t[i], '< 1')
    #         break

    # C 为问题的解
    # 用舍入法进行求解
    C = []
    union_C = []
    for i in range(len(result)):
        if result[i] >= max_f:
            C.append(F[i])
            union_C.extend(F[i])

    print(C)
    print(len(set(union_C)))


if __name__ == "__main__":
    # 4.1 实现基于贪心策略的近似算法
    # 4.2 实现一个基于线性规划的近似算法
    # 4.3 测试算法的性能 100,1000,5000
    # LP()
    # greedy_covers()
    nums = [100, 1000, 5000]
    time_record_greedy = []
    time_record_LP = []
    for num in nums:
        U,F = gene_data(num)
        time_greedy_start = time.time()
        greedy_covers(U,F)
        time_greedy_end = time.time()
        time_greedy = time_greedy_end - time_greedy_start

        time_LP_start = time.time()
        LP(U,F)
        time_LP_end = time.time()
        time_LP = time_LP_end - time_LP_start

        time_record_greedy.append(time_greedy)
        time_record_LP.append(time_LP)

    plt.plot(nums, time_record_greedy, c="red",label="greedy")
    plt.plot(nums, time_record_LP, c="yellow",label="LP")
    plt.legend(loc="upper left")
    plt.xlabel("data size")
    plt.ylabel("time")
    plt.show()
