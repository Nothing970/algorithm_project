import random
import time
import sys
sys.setrecursionlimit(2000000)


def QuickSort(A, p, r):
    if p < r:
        q = Rand_Partition(A, p, r)
        QuickSort(A, p, q-1)
        QuickSort(A, q+1, r)


def Rand_Partition(A, p, r):
    # randint 同时包含上下界
    i = random.randint(p, r)
    A[r], A[i] = A[i], A[r]
    x = A[r]
    i = p-1
    for j in range(p,r):
        if A[j] <= x:
            i = i+1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[r] = A[r], A[i+1]
    return i+1


if __name__ == "__main__":
    # （1）输入为1000000个随机32位整数，记录算法的运行表现
    input_1 = [random.randint(0, int(10E32)-1) for i in range(1000000)]
    time_start_1 = time.time()
    QuickSort(input_1, 0, len(input_1)-1)
    time_end_1 = time.time()
    print("(1)time cost:", time_end_1-time_start_1)

    # （2）输入为1000000个1，记录算法的运行表现
    # input_2 = [1 for i in range(1000000)]
    # time_start_2 = time.time()
    # QuickSort(input_2, 0, len(input_2)-1)
    # time_end_2 = time.time()
    # print("(2)time cost:", time_end_2-time_start_2)

    # （3）输入规模为10000，先向数组中添加x%比例的1，再向数组中加入随机32位整数直到填满数组，
    # 分别令x = 50，60，70，80，90，100
    for percent in [50,60,70,80,90,100]:
        input_3 = [1 for i in range(100*percent)] + \
                  [random.randint(0, int(10E32) - 1) for i in range(100*(100-percent))]
        time_start_3 = time.time()
        QuickSort(input_3, 0, len(input_3)-1)
        time_end_3 = time.time()
        print("(3)time cost(percent:%d):"%percent,time_end_3-time_start_3)

    # （4）分别令输入规模为1000，5000，重复第（3）步实验
    for amount in [1000,5000]:
        for percent in [50, 60, 70, 80, 90, 100]:
            input_4 = [1 for i in range(int(amount/100) * percent)] + \
                      [random.randint(0, int(10E32) - 1) for i in range(int(amount/100) * (100 - percent))]
            time_start_4 = time.time()
            QuickSort(input_4, 0, len(input_4)-1)
            time_end_4 = time.time()
            print("(4)time cost(amount:%d percent:%d):" % (amount, percent), time_end_4 - time_start_4)

    # （5）（选做）调用自带的快速排序算法
    input_1 = [random.randint(0, int(10E32) - 1) for i in range(1000000)]
    time_start_1 = time.time()
    input_1.sort()
    time_end_1 = time.time()
    print("(1)time cost:", time_end_1 - time_start_1)

    input_2 = [1 for i in range(1000000)]
    time_start_2 = time.time()
    input_2.sort()
    time_end_2 = time.time()
    print("(2)time cost:", time_end_2 - time_start_2)

    for percent in [50,60,70,80,90,100]:
        input_3 = [1 for i in range(100*percent)] + \
                  [random.randint(0, int(10E32) - 1) for i in range(100*(100-percent))]
        time_start_3 = time.time()
        input_3.sort()
        time_end_3 = time.time()
        print("(3)time cost(percent:%d\):"%percent,time_end_3-time_start_3)

    for amount in [1000,5000]:
        for percent in [50, 60, 70, 80, 90, 100]:
            input_4 = [1 for i in range(int(amount/100) * percent)] + \
                      [random.randint(0, int(10E32) - 1) for i in range(int(amount/100) * (100 - percent))]
            time_start_4 = time.time()
            input_4.sort()
            time_end_4 = time.time()
            print("(4)time cost(amount:%d percent:%d\):" % (amount, percent), time_end_4 - time_start_4)



