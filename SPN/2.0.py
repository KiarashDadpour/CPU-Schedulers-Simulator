import matplotlib.pyplot as plt

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
    timeline = []

    while completed_count < p:
        Q = []
        for process in range(p):
            if at[process] <= current_time and not completed[process]:  
                Q.append(process)
        if not Q:
            current_time += 1
            continue
        shortest_process = find_min(Q, cbt)
        start_time = current_time
        current_time += cbt[shortest_process]  
        TT[shortest_process] = current_time - at[shortest_process]
        WT[shortest_process] = TT[shortest_process] - cbt[shortest_process]
        completed[shortest_process] = True
        completed_count += 1

        timeline.append((shortest_process + 1, start_time, current_time))  

        current_time += cs  

    return WT, TT, timeline

def plot_gantt_spn(timeline, cs):
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
    plt.title("SPN")
    plt.show()


p = 5
at = [0, 2, 3, 4, 5]
cbt = [10, 8, 3, 7, 12]
cs = 1

a, b, timeline = spn(p, at, cbt, cs)
print("Waiting Times:", a)
print("Turnaround Times:", b)

wtbar = average(a, p)
ttbar = average(b, p)
print("Average of WT: ", wtbar)
print("Average of TT: ", ttbar)

plot_gantt_spn(timeline, cs)
