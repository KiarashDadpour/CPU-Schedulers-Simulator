import matplotlib.pyplot as plt

def average(lst):
    return sum(lst) / len(lst)

def find_ready_processes(p, at, current_time, completed):
    ready_processes = []
    for i in range(p):
        if at[i] <= current_time and not completed[i]:
            ready_processes.append(i)
    return ready_processes


def calculate_rpr(ready_processes, current_time, at, cbt):
    ready_processes = list(ready_processes)

    rprs = []
    for process in ready_processes:
        waiting_time = max(0, current_time - at[process])
        rpr = (waiting_time + cbt[process]) / cbt[process]
        rprs.append((rpr, process))

    return list(rprs)


def find_max_rpr(rprs, at):
    max_ratio = -1
    max_index = -1

    for i, (ratio, process) in enumerate(rprs):
        if ratio > max_ratio:
            max_ratio = ratio
            max_index = i
        elif ratio == max_ratio:
            if at[process] < at[rprs[max_index][1]]:
                max_index = i

    return rprs[max_index][1]


def hrrn(p, at, cbt, cs):
    current_time = 0

    WT = [0] * p
    TT = [0] * p
    completed = [False] * p
    timeline = []

    completed_count = 0

    while completed_count < p:
        ready_processes = find_ready_processes(p, at, current_time, completed)

        if len(ready_processes) == 0:
            next_arrival = float('inf')
            for i in range(p):
                if not completed[i]:
                    next_arrival = min(next_arrival, at[i])
            current_time = next_arrival
            continue

        rpr = calculate_rpr(ready_processes, current_time, at, cbt)

        max_index = find_max_rpr(rpr, at)

        start_time = current_time
        current_time += cbt[max_index]
        end_time = current_time

        TT[max_index] = end_time - at[max_index]  # Turnaround Time
        WT[max_index] = TT[max_index] - cbt[max_index]  # Waiting Time

        completed[max_index] = True
        completed_count += 1

        timeline.append((max_index + 1, start_time, end_time))

        current_time += cs

    RT = WT
    return WT, TT ,RT,  timeline


def plot_gantt_hrrn(timeline, cs):
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
    plt.title("HRRN")
    plt.show()

# Test the algorithm
p = 5
at = [0, 2, 3, 4, 5]
cbt = [10, 8, 3, 7, 12]
cs = 1

a, b, c, timeline = hrrn(p, at, cbt, cs)
print("WT:", a)
print("TT:", b)
print("RT: ", c)
wtbar = average(a)
ttbar = average(b)
rtbar = average(c)
print("Average of WT: ", wtbar)
print("Average of TT: ", ttbar)
print("Average of RT: ", rtbar)

plot_gantt_hrrn(timeline, cs)
