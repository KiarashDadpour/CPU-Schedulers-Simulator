def average(lst, p:int):
    time = 0
    for i in lst:
        time += i
    return time / p

def fcfs(p, at: list, cbt: list, cs: int) :
    current_time = 0
    WT = []
    TT = []
    for process in range(p):
        start_time = max(current_time,at[process])
        end_time = start_time + cbt[process]
        wt = start_time - at[process]
        tt = end_time - at[process]
        WT.append(wt)
        TT.append(tt)
        current_time = end_time + cs
    return WT, TT

p = 5
at = [0, 2, 3, 4, 5]
cbt = [10, 8, 3, 7, 12]
cs = 1
a,b = fcfs(p, at, cbt, cs)
print(a)
wtbar = average(a, p)
ttbar = average(b, p)
print("Average of WT: " ,wtbar)
print("Average of TT: ", ttbar)




