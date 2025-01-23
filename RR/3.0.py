import matplotlib.pyplot as plt
from collections import deque

def average(lst):
    return sum(lst) / len(lst)

def round_robin(p, at, cbt, cs, quantum):
    cbt1 = cbt.copy()
    at1 = at.copy()

    WT = [0] * p 
    TT = [0] * p  
    RT = [float('inf')] * p  
    timeline = []

    current_time = 0
    ready_queue = deque()
    completed_processes = 0
    first_run = [True] * p  

    for i in range(p):
        if at1[i] <= current_time and cbt[i] > 0:
            if i not in ready_queue:
                ready_queue.append(i)

    while completed_processes < p:
        if not ready_queue:
            current_time += 1
            continue

        current_process = ready_queue.popleft()

        if first_run[current_process]:
            RT[current_process] = current_time - at1[current_process]
            first_run[current_process] = False

        start_time = current_time
        running_time = min(quantum, cbt[current_process])

        current_time += running_time
        cbt[current_process] -= running_time

        timeline.append((current_process + 1, start_time, current_time))

        current_time += cs
        if cbt[current_process] <= 0:
            completed_processes += 1
            TT[current_process] = current_time - at1[current_process]
            WT[current_process] = TT[current_process] - cbt1[current_process]
        else:
            for i in range(p):
                if at1[i] <= current_time and  cbt[i] > 0 and  i not in ready_queue and i != current_process:
                    ready_queue.append(i)

            ready_queue.append(current_process)

    return WT, TT, RT, timeline


def plot_gantt_rr(timeline, cs):
    fig, ax = plt.subplots(figsize=(10, 6))
    half_cs = cs / 2  # Compute half of CS time

    for i, process in enumerate(timeline):
        index, start, end = process
        y_pos = index * 1.5
        ax.broken_barh([(start, end - start)], (y_pos - 0.4, 0.8), facecolors='tab:blue')
        if cs > 0 and i < len(timeline) - 1:
            cs_start = end
            ax.broken_barh([(cs_start, half_cs)], (y_pos - 0.4, 0.8), facecolors='tab:red', alpha=0.5)
        if cs > 0 and i < len(timeline) - 1:
            next_start = timeline[i + 1][1]
            cs_start_next = next_start - half_cs
            ax.broken_barh([(cs_start_next, half_cs)], ((timeline[i + 1][0] * 1.5) - 0.4, 0.8), facecolors='tab:orange', alpha=0.5)
    if cs > 0:
        last_process_end = timeline[-1][2]
        ax.broken_barh([(last_process_end, half_cs)], (y_pos - 0.4, 0.8), facecolors='tab:green', alpha=0.5)

    ax.set_ylim(0, len(timeline))
    ax.set_xlim(0, max(t[2] for t in timeline) + cs)
    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_yticks([t[0] * 1.5 for t in timeline])
    ax.set_yticklabels([f"P{t[0]}" for t in timeline])
    ax.grid(True)
    max_time = max(t[2] for t in timeline) + cs
    ax.set_xticks(range(0, max_time + 1, 2))
    plt.title("Round Robin")
    plt.show()

p = 5
at = [0, 2, 3, 4, 5]
cbt = [9, 8, 3, 7, 10]
cs = 1
quantum = 5

a, b, c, timeline = round_robin(p, at, cbt, cs, quantum)
print("WT:", a)
print("TT:", b)
print("RT: ", c)
wtbar = average(a)
ttbar = average(b)
rtbar = average(c)
print("Average of WT: ", wtbar)
print("Average of TT: ", ttbar)
print("Average of RT: ", rtbar) 

plot_gantt_rr(timeline, cs)
