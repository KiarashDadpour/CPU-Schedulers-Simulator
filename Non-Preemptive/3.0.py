import matplotlib.pyplot as plt

def average(lst):
    return sum(lst) / len(lst)


def get_highest_priority_process(ready_queue, priorities1):
    highest_priority = float('inf')
    selected_process = None

    for process in ready_queue:
        if priorities1[process] < highest_priority:
            highest_priority = priorities1[process]
            selected_process = process

    return selected_process


def non_preemptive(p, at: list, cbt: list, priorities, cs=1):
    current_time = 0
    WT = [0] * p
    TT = [0] * p
    RT = [0] * p  # Response Time
    timeline = []
    ready_queue = []
    completed_processes = 0

    cbt1 = cbt.copy()
    priorities1 = priorities.copy()

    while completed_processes < p:
        for i in range(p):
            if at[i] <= current_time and i not in ready_queue and cbt1[i] > 0:
                ready_queue.append(i)

        if not ready_queue:
            current_time += 1
            continue

        selected_process = get_highest_priority_process(ready_queue, priorities1)

        if current_time < at[selected_process]:
            current_time = at[selected_process]

        start_time = current_time
        end_time = start_time + cbt1[selected_process]

        WT[selected_process] = start_time - at[selected_process]
        TT[selected_process] = end_time - at[selected_process]
        RT[selected_process] = start_time - at[selected_process]  # Response time

        timeline.append((selected_process + 1, start_time, end_time))

        current_time = end_time + cs

        cbt1[selected_process] = 0
        completed_processes += 1

        ready_queue.remove(selected_process)

    return WT, TT, RT, timeline


def plot_gantt_rr(timeline, cs):
    fig, ax = plt.subplots(figsize=(10, 6))
    half_cs = cs / 2  # Compute half of CS time

    for i, process in enumerate(timeline):
        index, start, end = process
        y_pos = index * 1.45
        ax.broken_barh([(start, end - start)], (y_pos - 0.4, 0.8), facecolors='tab:blue')
        if cs > 0 and i < len(timeline) - 1:
            cs_start = end
            ax.broken_barh([(cs_start, half_cs)], (y_pos - 0.4, 0.8), facecolors='tab:red', alpha=0.5)
        if cs > 0 and i < len(timeline) - 1:
            next_start = timeline[i + 1][1]
            cs_start_next = next_start - half_cs
            ax.broken_barh([(cs_start_next, half_cs)], ((timeline[i + 1][0] * 1.45) - 0.4, 0.8), facecolors='tab:orange', alpha=0.5)
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
    plt.title("Non-Preemtive")
    plt.show()

p = 6
at = [0, 0, 1, 1, 2, 2]
cbt = [4, 2, 1, 3, 2, 1]
cs = 1
priority = [2, 3, 1, 4, 3, 1]

a, b, c, timeline = non_preemptive(p, at, cbt, priority, cs)
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
