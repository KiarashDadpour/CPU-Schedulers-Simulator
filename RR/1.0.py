def average(lst, p: int):
    time = 0
    for i in lst:
        time += i
    return time / p


def round_robin(p, at: list, cbt: list, cs: int, quantum: int):
    current_time = 0
    cbt1 = cbt[:]
    WT = [0] * p
    TT = [0] * p
    completed = [False] * p

    all_completed = False
    while not all_completed:
        all_completed = True
        for process in range(p):
            if at[process] <= current_time and cbt[process] > 0: # kodom lahze ki omade
                all_completed = False
                if cbt[process] > quantum:
                    current_time += quantum
                    cbt[process] -= quantum
                else:
                    current_time += cbt[process]
                    cbt[process] = 0
                    completed[process] = True
                    TT[process] = current_time - at[process]
                    WT[process] = TT[process] - cbt1[process]

                current_time += cs

    return WT, TT


p = 5
at = [0, 2, 3, 4, 5]
cbt = [10, 8, 3, 7, 12]
cs = 0
quantum = 5
a, b = round_robin(p, at, cbt, cs, quantum)
print(a)
wtbar = average(a, p)
ttbar = average(b, p)
print("Average of WT: ", wtbar)
print("Average of TT: ", ttbar)
