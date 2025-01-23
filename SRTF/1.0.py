import matplotlib.pyplot as plt


def average(lst):
    return sum(lst) / len(lst)


def srtf(p, at, cbt, cs, quantum):
    current_time = 0
    WT = [0] * p
    TT = [0] * p
    remaining_time = cbt.copy()
    timeline = []
    completed = [False] * p
    completed_count = 0
    last_process = -1
    process_execution_time = [0] * p

    while completed_count < p:
        # Find arrived and not completed processes
        arrived_processes = [
            i for i in range(p)
            if at[i] <= current_time and not completed[i] and remaining_time[i] > 0
        ]

        if not arrived_processes:
            # If no process has arrived, move to next arrival
            next_arrival = min(at[i] for i in range(p) if not completed[i])
            current_time = next_arrival
            continue

        # Find process with shortest remaining time
        current_process = min(arrived_processes, key=lambda x: remaining_time[x])

        # Determine execution time
        if process_execution_time[current_process] >= quantum:
            # Perform context switch and find next shortest process
            current_time += cs
            process_execution_time[current_process] = 0

            # Recalculate arrived processes after context switch
            arrived_processes = [
                i for i in range(p)
                if at[i] <= current_time and not completed[i] and remaining_time[i] > 0
            ]

            if not arrived_processes:
                continue

            # Find new shortest process
            current_process = min(arrived_processes, key=lambda x: remaining_time[x])


        # Execute process

        execution_time = min(
            quantum - process_execution_time[current_process],  # Remaining quantum
            remaining_time[current_process]  # Remaining burst time
        )

        # Update times and tracking
        current_time += execution_time
        remaining_time[current_process] -= execution_time
        process_execution_time[current_process] += execution_time

        # Track timeline
        timeline.append((current_process + 1, current_time - execution_time, current_time))

        # Check if process is completed
        if remaining_time[current_process] == 0:
            completed[current_process] = True
            completed_count += 1
            process_execution_time[current_process] = 0

            # Calculate waiting and turnaround times
            TT[current_process] = current_time - at[current_process]
            WT[current_process] = TT[current_process] - cbt[current_process]
            current_time += cs


    return WT, TT, timeline


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

WT, TT, timeline = srtf(p, at, cbt, cs, q)
print("Waiting Times:", WT)
print("Turnaround Times:", TT)
print("Average Waiting Time:", average(WT))
print("Average Turnaround Time:", average(TT))

plot_gantt_srtf(timeline, cs)
