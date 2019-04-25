import random
import math
import matplotlib.pyplot as plt
import time
import sys
sys.setrecursionlimit(2000000)


# 产生坐标0-10的随机点n个
def generate_point_set(n):
    point_set = []
    i =0
    while i < n:
        point = [random.randint(0, 100), random.randint(0, 100)]
        if point not in point_set:
            i += 1
            point_set.append(point)
    return point_set


def g(A, B, P):
    """
    判断点PA 矢量 在 AB矢量 的顺时针方向还是还是逆时针方向，
    若在逆时针方向则返回1，同向返回0，顺时针方向返回 -1
    :param A:
    :param B:
    :param P:
    :return:
    """
    # 使用PxQ = XpYp - XqYp,若大于0则表示Q在P的逆时针方向
    result = (B[0]-A[0])*(P[1]-A[1])-(B[1]-A[1])*(P[0]-A[0])
    if result < 0:
        return -1
    elif result == 0:
        return 0
    else:
        return 1


def is_in_triangle(Pi, Pj, Pk, P):
    """
    判断点P 是否在其他三个点组成的三角形中，是的话返回true
    :param Pi:
    :param Pj:
    :param Pk:
    :param P:
    :return:
    """
    if g(Pi,Pj,Pk) == 0:
        return 0
    if g(Pi,Pj,P)*g(Pi,Pj,Pk) >= 0 and  g(Pj,Pk,P)*g(Pj,Pk,Pi) >=0 and g(Pk,Pi,P)*g(Pk,Pi,Pj) >= 0:
        return 1
    return 0


def brute_force(Q):
    Q = list(Q)
    # p_0是横坐标最小的点，一定是凸包上的点
    flag = [1 for i in range(len(Q))]
    output = []
    if len(Q) == 3:
        # 以逆时针方式输出凸包的点
        if g(Q[0],Q[1],Q[2]) > 0:
            output = Q
        else:
            output.append(Q[2])
            output.append(Q[1])
            output.append(Q[0])
        return output

    for i in range(len(Q)-3):
        for j in range(i+1,len(Q)-2):
            for k in range(j+1,len(Q)-1):
                for l in range(k+1,len(Q)):
                    if is_in_triangle(Q[i],Q[j],Q[k],Q[l]):
                        flag[l] = 0
                    if is_in_triangle(Q[j],Q[k],Q[l],Q[i]):
                        flag[i] = 0
                    if is_in_triangle(Q[k],Q[l],Q[i],Q[j]):
                        flag[j] = 0
                    if is_in_triangle(Q[l],Q[i],Q[j],Q[k]):
                        flag[k] = 0
    print(flag)
    sub_Q = []
    for i in range(len(Q)):
        if flag[i]:
            sub_Q.append(Q[i])
    # 找到sub_Q x 坐标最大点B和最小点A
    A = sub_Q[0]
    B = sub_Q[0]
    for point in sub_Q:
        if point[0] < A[0]:
            A = point
        if point[0] > B[0]:
            B = point

    # 按照点在AB直线的上方还是下方将 sub_Q 分为up，down两部分
    Qup = []
    Qdown = []
    for point in sub_Q:
        if g(A,B,point) > 0:
            Qup.append(point)
        if g(A,B,point) < 0:
            Qdown.append(point)

    # 将Qup按照横坐标递减排序，将Qdown按照横坐标递增排序
    Qup = sorted(Qup,key=lambda x:x[0],reverse=True)
    Qdown = sorted(Qdown,key=lambda x:x[0],reverse=False)

    #  从A按照x坐标递增输出Qdown,从B开始按照x坐标依次递减输出Qup
    output = []
    output.append(A)
    output.extend(Qdown)
    output.append(B)
    output.extend(Qup)
    return output


def preProcess(point_polar):
    """
    当多个点的极角相同时，保留距离原点最远的点
    :param point_polar:
    :return:
    """
    # sorted_polar = sorted(point_polar,key=lambda x:x[2])
    # remove_Duplicates = []
    # i = 0
    # while i < len(sorted_polar):
    #     temp_max = sorted_polar[i]
    #     j = i + 1
    #     while j < len(sorted_polar) and sorted_polar[i][2] == sorted_polar[j][2]:
    #         if sorted_polar[j][3] >temp_max[3]:
    #             temp_max = sorted_polar[j]
    #     remove_Duplicates.append(temp_max)
    remove_Duplicates_dict = {}
    for i in range(len(point_polar)):
        if remove_Duplicates_dict.get(point_polar[i][2]) == None:
            remove_Duplicates_dict[point_polar[i][2]] = point_polar[i]
        elif remove_Duplicates_dict[point_polar[i][2]][3] < point_polar[i][3]:
            remove_Duplicates_dict[point_polar[i][2]] = point_polar[i]
    remove_Duplicates = list(remove_Duplicates_dict.values())
    remove_Duplicates = sorted(remove_Duplicates, key=lambda x: x[2])
    return remove_Duplicates


def GrahamScan(Q,preprocess=True):
    n = len(Q)
    if n <= 2:
        return Q
    if n == 3:
        output = []
        # 以逆时针方式输出凸包的点
        if g(Q[0],Q[1],Q[2]) > 0:
            output = Q
        else:
            output.append(Q[2])
            output.append(Q[1])
            output.append(Q[0])
        return output
    P = []
    if preprocess:
        Q = sorted(Q, key=lambda x: x[1], reverse=False)
        point_polar = []
        for i in range(1, n):
            polar = math.atan2(Q[i][1] - Q[0][1], Q[i][0] - Q[0][0])
            polar = polar / math.pi * 180
            length = math.sqrt((Q[i][1] - Q[0][1]) * (Q[i][1] - Q[0][1]) + (Q[i][0] - Q[0][0]) * (Q[i][0] - Q[0][0]))
            point_polar.append([Q[i][0], Q[i][1], polar, length])
            # 预处理：找到Q中y坐标最小的点P0,以水平为极轴求得每个点极角
            result = preProcess(point_polar)
        P.append(Q[0])
        for i in range(len(result)):
            P.append([result[i][0], result[i][1]])
    else:
        P=Q

    m = len(P)

    if m < 2:
        return
    stack = []
    stack.append(P[0])
    stack.append(P[1])
    stack.append(P[2])
    for i in range(3,m):
        while is_in_triangle(P[0],P[i],stack[-2],stack[-1]):
            stack.pop()
        stack.append(P[i])
    return stack

# def PartSort()
# def find_mid_x(Q,start,end):
#     left = start
#     right = end
#     key = Q[end]
#     while left < right:
#         while left < right and Q[left][0] <= key[0]:
#             left +=1
#         while left < right and Q[right][0] >= key[0]:
#             right -=1
#         if left < right:


def merge_two_ordered_polar_point(nums1,nums2):
    i = 0
    j = 0
    result = []
    while i < len(nums1) and j < len(nums2):
        if nums1[i][2] <= nums2[j][2]:
            result.append(nums1[i])
            i += 1
        else:
            result.append(nums2[j])
            j += 1
    if i < len(nums1):
        result.extend(nums1[i:])
    if j < len(nums2):
        result.extend(nums2[j:])
    return result


def ConvexHull(Q):
    n = len(Q)
    if n <= 2:
        return Q
    if n == 3:
        output = []
        # 以逆时针方式输出凸包的点
        if g(Q[0],Q[1],Q[2]) > 0:
            output = Q
        else:
            output.append(Q[2])
            output.append(Q[1])
            output.append(Q[0])
        return output
    # x中位数
    mid_x = sum([point[0] for point in Q]) / n
    Ql = []
    Qr=[]
    for point in Q:
        if point[0] <= mid_x:
            Ql.append(point)
        else:
            Qr.append(point)
    Pl = ConvexHull(Ql)
    Pr = ConvexHull(Qr)
    # 如果左侧的最低点不是全局最低点，则有可能出错，eg：Q = [[1,50],[10,70],[10,49],[51,2],[51,70]]
    # 所以这种情况进行左右互换
    # global_low_y = Pl[0][1]
    # for point in Pl:
    #     if global_low_y > point[1]:
    #         global_low_y = point[1]
    # for point in Pr:
    #     if global_low_y >point[1]:
    #         Pr, Pl = Pl, Pr
    left = []
    right_1 = []
    right_2 = []
    # Pl 内部点p
    p = [sum(point[0] for point in Pl)/len(Pl),sum(point[1] for point in Pl)/len(Pl)]
    # pl_i 为左侧最低点
    pl_i = Pl[0]
    pl_i_index = 0
    for i in range(len(Pl)):
        if Pl[i][1]< pl_i[1]:
            pl_i = Pl[i]
            pl_i_index = i
    num = 0
    while num < len(Pl):
        # 待计算计算角与x轴水平方向夹角
        polar1 = math.atan2(Pl[(pl_i_index+num) % len(Pl)][1] - p[1], Pl[(pl_i_index+num) % len(Pl)][0] - p[0])
        polar1 = polar1 / math.pi * 180
        # pl_i与与x轴水平方向夹角
        polar2 = math.atan2(pl_i[1] - p[1], pl_i[0] - p[0])
        polar2 = polar2 / math.pi * 180
        polar = (polar1 - polar2) % 360
        left.append([Pl[(pl_i_index+num) % len(Pl)][0],Pl[(pl_i_index+num) % len(Pl)][1],polar])
        num += 1
    pr_high = Pr[0]
    pr_high_index = 0
    pr_low = Pr[0]
    pr_low_index = 0
    for i in range(len(Pr)):
        if Pr[i][1] > pr_high[1]:
            pr_high = Pr[i]
            pr_high_index = i
        if Pr[i][1] < pr_low[1]:
            pr_low = Pr[i]
            pr_low_index = i
    num = 0
    num_right_1 = (len(Pr)+pr_high_index-pr_low_index + 1) % len(Pr)
    if num_right_1 ==0:
        num_right_1 = len(Pr)
    while num < num_right_1:
        polar1 = math.atan2(Pr[(pr_low_index + num) % len(Pr)][1] - p[1], Pr[(pr_low_index + num) % len(Pr)][0] - p[0])
        polar1 = polar1 / math.pi * 180
        polar2 = math.atan2(pl_i[1] - p[1], pl_i[0] - p[0])
        polar2 = polar2 / math.pi * 180
        polar = (polar1 - polar2) % 360
        right_1.append([Pr[(pr_low_index + num) % len(Pr)][0], Pr[(pr_low_index + num) % len(Pr)][1], polar])
        num += 1
    num = 0
    num_right_2 = (len(Pr) - num_right_1) % len(Pr)
    while num < num_right_2:
        polar1 = math.atan2(Pr[(pr_low_index + len(Pr) - 1 - num) % len(Pr)][1] - p[1], Pr[(pr_low_index + len(Pr) - 1 - num) % len(Pr)][0] - p[0])
        polar1 = polar1 / math.pi * 180
        polar2 = math.atan2(pl_i[1] - p[1], pl_i[0] - p[0])
        polar2 = polar2 / math.pi * 180
        polar = (polar2 - polar1) % 360
        right_2.append([Pr[(pr_low_index + len(Pr) - 1 - num) % len(Pr)][0], Pr[(pr_low_index + len(Pr) - 1 - num) % len(Pr)][1], polar])
        num += 1

    merged_point = merge_two_ordered_polar_point(merge_two_ordered_polar_point(left,right_1),right_2)
    merged_point = [x[:-1] for x in merged_point]
    return GrahamScan(merged_point,preprocess=False)


if __name__ == "__main__":
    # 4.1实现基于枚举方法的凸包求解算法
    # 4.2实现基于Graham-Scan的凸包求解算法
    # 4.3 实现基于分治思想的凸包求解算法
    # 4.4 长为100正方形，点数大小分别为1000，2000，3000 的数据集合，记录时间，绘制性能曲线

    # Q = generate_point_set(50)
    # # Q = [[98, 10], [30, 20], [9, 38], [15, 33], [57, 61], [67, 72], [39, 42], [71, 1], [59, 66], [88, 60], [88, 35], [52, 17], [70, 100], [54, 8], [82, 40], [36, 45], [46, 82], [19, 69], [47, 13], [96, 46], [47, 32], [28, 53], [30, 60], [12, 47], [75, 75], [32, 1], [82, 1], [84, 29], [2, 61], [78, 19], [50, 31], [29, 33], [94, 55], [34, 77], [84, 87], [13, 48], [54, 2], [42, 99], [5, 43], [60, 86]]
    # # Q = [[9, 38], [15, 33], [19, 69], [28, 53], [12, 47], [2, 61], [13, 48], [5, 43]]
    # # Q = [[9, 38], [12, 47], [2, 61], [5, 43]]
    # # Q =[[9, 10], [80, 40], [94, 80], [48, 72], [61, 91], [18, 81], [87, 16], [94, 34], [60, 23], [77, 28], [0, 16], [62, 91], [32, 3], [46, 7], [56, 40], [26, 14], [92, 27], [57, 63], [52, 70], [8, 76], [68, 24], [89, 82], [5, 90], [19, 71], [64, 99], [54, 57], [42, 34], [0, 27], [91, 5], [28, 41], [47, 21], [81, 29], [76, 6], [84, 15], [19, 67], [67, 98], [64, 59], [88, 15], [7, 0], [11, 64]]
    # # Q = [[1,50],[10,70],[10,49],[51,2],[51,70]]
    # print(Q)
    # Q = list(Q)
    # # P = brute_force(Q)
    # # print(Q)
    # # P = GrahamScan(Q)
    # # print(Q)
    # P = ConvexHull(Q)
    # # print(P)
    #
    # # 展示最终效果
    # for point in Q:
    #     # scatter() 画散点
    #     plt.scatter(point[0],point[1],marker='o',c='y')
    # (x,y) = zip(*P+[P[0]])
    # plt.plot(x,y)
    # plt.show()

    point_nums = [100,200,300]
    time_records = []
    for point_num in point_nums:
        Q = generate_point_set(point_num)
        time_brute_start = time.time()
        P = brute_force(Q)
        time_brute_end = time.time()
        time_brute = time_brute_end - time_brute_start

        time_scan_start = time.time()
        P = GrahamScan(Q)
        time_scan_end = time.time()
        time_scan = time_scan_end - time_scan_start

        time_convex_start = time.time()
        P = ConvexHull(Q)
        time_convex_end = time.time()
        time_convex = time_convex_end - time_convex_start

        time_records.append([time_brute, time_scan, time_convex])

    plt.plot(point_nums, time_records[0], c="red")
    plt.plot(point_nums, time_records[1], c="yellow")
    plt.plot(point_nums, time_records[2], c="blue")
    plt.show()





