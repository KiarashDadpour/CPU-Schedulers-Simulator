def find_min(Q: list, cbt: list):
    min_value = float("inf")
    index_value = -1
    for index in Q:
        if cbt[index] < min_value:
            min_value = cbt[index]
            index_value = index
    return index_value

def average(lst, p: int):
    return sum(lst) / p

def spn(p, at: list, cbt: list, cs: int):
    current_time = 0
    WT = [0] * p
    TT = [0] * p
    completed_count = 0
    completed = [False] * p

    while completed_count < p:
        Q = []
        for process in range(p):
            if at[process] <= current_time and completed[process] == False: # kodom omade
                Q.append(process)
        if not Q:
            current_time += 1
            continue
        shortest_process = find_min(Q, cbt)
        current_time += cbt[shortest_process] + cs
        TT[shortest_process] = current_time - at[shortest_process]
        WT[shortest_process] = TT[shortest_process] - cbt[shortest_process]
        completed[shortest_process] = True
        completed_count += 1

    return WT, TT


p = 5
at = [0, 2, 3, 4, 5]
cbt = [10, 8, 3, 7, 12]
cs = 0
a, b = spn(p, at, cbt, cs)
print("Waiting Times:", a)
print("Turnaround Times:", b)
wtbar = average(a, p)
ttbar = average(b, p)
print("Average of WT: ", wtbar)
print("Average of TT: ", ttbar)




