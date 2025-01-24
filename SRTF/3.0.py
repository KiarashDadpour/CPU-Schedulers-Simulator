import matplotlib.pyplot as plt
from collections import deque


def average(lst):
    return sum(lst) / len(lst)


def find_shortest_process(arrived_processes, cbt1):
    shortest_process = None
    shortest_time = float('inf')

    for process in arrived_processes:
        if cbt1[process] < shortest_time:
            shortest_time = cbt1[process]
            shortest_process = process

    return shortest_process


def srtf(p, at, cbt, cs, quantum):
    current_time = 0
    WT = [0] * p
    TT = [0] * p
    RT = [0] * p
    first_run = [False] * p

    cbt1 = cbt.copy()
    timeline = []
    completed = [False] * p
    completed_count = 0
    current_running_time = [0] * p

    while completed_count < p:
        arrived_processes = deque()
        for i in range(p):
            if at[i] <= current_time and not completed[i] and cbt1[i] > 0:
                arrived_processes.append(i)

        if len(arrived_processes) == 0:
            next_arrival = float('inf')
            for i in range(p):
                if not completed[i]:
                    next_arrival = min(next_arrival, at[i])

            current_time = next_arrival
            continue

        current_process = find_shortest_process(arrived_processes, cbt1)

        if not first_run[current_process]:
            RT[current_process] = current_time - at[current_process]
            first_run[current_process] = True

        if current_running_time[current_process] >= quantum:
            # Perform context switch and find next shortest process
            current_time += cs
            current_running_time[current_process] = 0

            arrived_processes.clear()
            for i in range(p):
                if at[i] <= current_time and not completed[i] and cbt1[i] > 0:
                    arrived_processes.append(i)

            if len(arrived_processes) == 0:
                continue

            current_process = find_shortest_process(arrived_processes, cbt1)

        execution_time = min(quantum - current_running_time[current_process], cbt1[current_process])

        current_time += execution_time
        cbt1[current_process] -= execution_time
        current_running_time[current_process] += execution_time

        timeline.append((current_process + 1, current_time - execution_time, current_time))

        if cbt1[current_process] == 0:
            completed[current_process] = True
            completed_count += 1
            current_running_time[current_process] = 0

            TT[current_process] = current_time - at[current_process]
            WT[current_process] = TT[current_process] - cbt[current_process]
            current_time += cs

    return WT, TT, RT, timeline

def plot_gantt_srtf(timeline, cs):
    fig, ax = plt.subplots(figsize=(10, 6))
    half_cs = cs / 2  # Compute half of CS time

    for i, process in enumerate(timeline):
        index, start, end = process
        y_pos = index * 1.5  # Increase vertical spacing between processes

        # Draw the process bar in blue
        ax.broken_barh([(start, end - start)], (y_pos - 0.4, 0.8), facecolors='tab:blue')

        # Draw the second half of CS at the end of the current process
        if cs > 0 and i < len(timeline) - 1:
            cs_start = end
            ax.broken_barh([(cs_start, half_cs)], (y_pos - 0.4, 0.8), facecolors='tab:red', alpha=0.5)

        # Draw the first half of CS at the start of the next process
        if cs > 0 and i < len(timeline) - 1:
            next_start = timeline[i + 1][1]
            cs_start_next = next_start - half_cs
            ax.broken_barh([(cs_start_next, half_cs)], ((timeline[i + 1][0] * 1.5) - 0.4, 0.8), facecolors='tab:orange', alpha=0.5)

    # Add CS time at the end of the last process
    if cs > 0:
        last_process_end = timeline[-1][2]
        ax.broken_barh([(last_process_end, half_cs)], (y_pos - 0.4, 0.8), facecolors='tab:green', alpha=0.5)

    ax.set_ylim(0, (len(timeline) + 1) * 1.5)
    ax.set_xlim(0, max(t[2] for t in timeline) + cs)
    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_yticks([t[0] * 1.5 for t in timeline])
    ax.set_yticklabels([f"P{t[0]}" for t in timeline])
    ax.grid(True)
    max_time = max(t[2] for t in timeline) + cs
    ax.set_xticks(range(0, max_time + 1, 2))
    plt.title("SRTF")
    plt.show()

# Test the algorithm
p = 6
at = [0, 0, 1, 1,2, 2]
cbt = [4, 2, 1, 3, 2, 1]
cs = 1
q = 3

a, b, c, timeline = srtf(p, at, cbt, cs, q)
print("WT:", a)
print("TT:", b)
print("RT: ", c)
wtbar = average(a)
ttbar = average(b)
rtbar = average(c)
print("Average of WT: ", wtbar)
print("Average of TT: ", ttbar)
print("Average of RT: ", rtbar)

plot_gantt_srtf(timeline, cs)
