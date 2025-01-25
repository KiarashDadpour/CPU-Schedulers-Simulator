from collections import deque
import matplotlib.pyplot as plt

def average(lst):
    return sum(lst) / len(lst)

def fcfs(p, at: list, cbt: list, cs=1):
    current_time = 0
    WT = [0] * p
    TT = [0] * p
    timeline = []

    ready_queue = deque(range(p))

    while ready_queue:
        process = ready_queue.popleft()

        if current_time < at[process]:
            current_time = at[process]
        start_time = current_time
        end_time = start_time + cbt[process]
        wt = start_time - at[process]
        tt = end_time - at[process]

        WT[process] = wt
        TT[process] = tt

        timeline.append((process + 1, start_time, end_time))

        current_time = end_time + cs
    RT = WT
    return WT, TT, RT,  timeline

def plot_gantt_fcfs(timeline, cs):
    fig, ax = plt.subplots(figsize=(10, 6))
    half_cs = cs / 2

    for i, process in enumerate(timeline):
        index, start, end = process
        y_pos = index * 1.47
        ax.broken_barh([(start, end - start)], (y_pos - 0.4, 0.8), facecolors='tab:blue')
        if cs > 0 and i < len(timeline) - 1:
            cs_start = end
            ax.broken_barh([(cs_start, half_cs)], (y_pos - 0.4, 0.8), facecolors='tab:red', alpha=0.5)
        if cs > 0 and i < len(timeline) - 1:
            next_start = timeline[i + 1][1]
            cs_start_next = next_start - half_cs
            ax.broken_barh([(cs_start_next, half_cs)], ((timeline[i + 1][0] * 1.47) - 0.4, 0.8), facecolors='tab:orange', alpha=0.5)
    if cs > 0:
        last_process_end = timeline[-1][2]
        ax.broken_barh([(last_process_end, half_cs)], (y_pos - 0.4, 0.8), facecolors='tab:green', alpha=0.5)

    ax.set_ylim(0, len(timeline))
    ax.set_xlim(0, max(t[2] for t in timeline) + cs)
    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_yticks([t[0] * 1.59 for t in timeline])
    ax.set_yticklabels([f"P{t[0]}" for t in timeline])
    ax.grid(True)
    max_time = max(t[2] for t in timeline) + cs
    ax.set_xticks(range(0, max_time + 1, 2))
    plt.title("FCFS")
    plt.show()

p = 5
at = [0, 2, 3, 4, 5]
cbt = [9, 8, 3, 7, 10]
cs = 1
quantum = 5

a, b, c, timeline = fcfs(p, at, cbt, cs)
print("WT:", a)
print("TT:", b)
print("RT: ", c)
wtbar = average(a)
ttbar = average(b)
rtbar = average(c) 
print("Average of WT: ", wtbar)
print("Average of TT: ", ttbar)
print("Average of RT: ", rtbar)

plot_gantt_fcfs(timeline, cs)
