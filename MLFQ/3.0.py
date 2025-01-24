from collections import deque
import matplotlib.pyplot as plt


def average(lst):
    return sum(lst) / len(lst)


def get_min_remaining_time_process(queue, remaining_time):
    min_time = float('inf')
    selected_process = None
    for process in queue:
        if remaining_time[process] < min_time:
            min_time = remaining_time[process]
            selected_process = process
    return selected_process


def get_max_response_ratio_process(queue, current_time, at, remaining_time):
    max_ratio = -1
    selected_process = None
    for process in queue:
        waiting_time = current_time - at[process]
        response_ratio = (waiting_time + remaining_time[process]) / remaining_time[process]
        if response_ratio > max_ratio:
            max_ratio = response_ratio
            selected_process = process
    return selected_process


def create_queues(num_queues):
    queues = []
    for i in range(num_queues):
        queues.append(deque())
    return queues


def mlfq_scheduler(p, at, cbt, quantum, cs, first_queue_algo, second_queue_algo,third_queue_algo, last_queue_algo):
    current_time = 0
    WT = [0] * p
    TT = [0] * p
    RT = [0] * p
    timeline = []

    queues = create_queues(4)
    remaining_time = cbt.copy()
    process_queue_time = [0] * p
    first_response = [False] * p

    queue_algorithms = []
    queue_algorithms.append(first_queue_algo)
    queue_algorithms.append(second_queue_algo)
    queue_algorithms.append(third_queue_algo)
    queue_algorithms.append(last_queue_algo)
    print("Selected algorithms:", queue_algorithms)

    quantum_times = [quantum, quantum * 2, quantum * 4]

    unassigned_processes = []
    for i in range(p):
        unassigned_processes.append(i)
    i = 0
    while len(unassigned_processes) > 0 or any(queues):
        for process in unassigned_processes[:]:
            if at[process] <= current_time:
                queues[0].append(process)
                unassigned_processes.remove(process)

        executed = False

        for queue_level in range(len(queues)):
            queue = queues[queue_level]
            if len(queue) == 0:
                continue

            current_algorithm = queue_algorithms[queue_level]
            process = None
            execute_time = 0

            if current_algorithm == 'RR':
                if len(queue) > 0:
                    process = queue[0]
                    if remaining_time[process] < quantum_times[queue_level]:
                        execute_time = remaining_time[process]
                    else:
                        execute_time = quantum_times[queue_level]

            elif current_algorithm == 'SRTF':
                if len(queue) > 0:
                    process = get_min_remaining_time_process(queue, remaining_time)
                    execute_time = quantum_times[i]

            elif current_algorithm == 'FCFS':
                if len(queue) > 0:
                    process = queue[0]
                    execute_time = remaining_time[process]

            elif current_algorithm == 'SPN':
                if len(queue) > 0:
                    process = get_min_remaining_time_process(queue, remaining_time)
                    execute_time = remaining_time[process]

            elif current_algorithm == 'HRRN':
                if len(queue) > 0:
                    process = get_max_response_ratio_process(queue, current_time, at, remaining_time)
                    execute_time = remaining_time[process]

            if process is None:
                continue

            if not first_response[process]:
                RT[process] = current_time - at[process]
                first_response[process] = True

            timeline.append((process + 1, current_time, current_time + execute_time))
            remaining_time[process] -= execute_time
            process_queue_time[process] += execute_time

            if remaining_time[process] <= 0:
                queue.remove(process)
                TT[process] = current_time + execute_time - at[process]
                WT[process] = TT[process] - cbt[process]
            elif queue_level < 3 and process_queue_time[process] >= quantum_times[queue_level]:
                queue.remove(process)
                queues[queue_level + 1].append(process)
                process_queue_time[process] = 0

            current_time += execute_time + cs
            executed = True
            break

        if not executed:
            current_time += 1
    i += 1
    return WT, TT, RT, timeline


def plot_gantt_mlfq(timeline, cs):
    fig, ax = plt.subplots(figsize=(10, 6))
    half_cs = cs / 2

    for i in range(len(timeline)):
        process = timeline[i]
        index = process[0]
        start = process[1]
        end = process[2]
        y_pos = index * 1.47

        # Plot process execution
        ax.broken_barh([(start, end - start)], (y_pos - 0.4, 0.8), facecolors='tab:blue')

        # Plot context switches
        if cs > 0 and i < len(timeline) - 1:
            cs_start = end
            ax.broken_barh([(cs_start, half_cs)], (y_pos - 0.4, 0.8),
                           facecolors='tab:red', alpha=0.5)

            next_start = timeline[i + 1][1]
            cs_start_next = next_start - half_cs
            next_y_pos = timeline[i + 1][0] * 1.47
            ax.broken_barh([(cs_start_next, half_cs)], (next_y_pos - 0.4, 0.8),
                           facecolors='tab:orange', alpha=0.5)

    # Plot final context switch
    if cs > 0:
        last_process_end = timeline[-1][2]
        ax.broken_barh([(last_process_end, half_cs)], (y_pos - 0.4, 0.8),
                       facecolors='tab:green', alpha=0.5)

    # Set up the plot
    ax.set_ylim(0, len(timeline))
    max_time = 0
    for t in timeline:
        if t[2] > max_time:
            max_time = t[2]
    ax.set_xlim(0, max_time + cs)

    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")

    # Set up y-axis ticks
    y_ticks = []
    y_labels = []
    for t in timeline:
        y_ticks.append(t[0] * 1.59)
        y_labels.append(f"P{t[0]}")
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)

    ax.grid(True)
    ax.set_xticks(range(0, max_time + cs + 1, 2))
    plt.title("MLFQ")
    plt.show()


p = 5
at = [0, 1, 2, 3, 4]  
cbt = [3, 6, 4, 5, 20]  
cs = 1  
quantum = 3
a, b, c, timeline = mlfq_scheduler(
    p, at, cbt, quantum, cs,
    first_queue_algo='SRTF',
    second_queue_algo='RR',
    third_queue_algo='RR',
    last_queue_algo='FCFS'
)


print("Waiting Times:", a)
print("Turnaround Times:", b)
print("Response Times:", c)
print("Average Waiting Time:", average(a))
print("Average Turnaround Time:", average(b))
print("Average Response Time:", average(c))

plot_gantt_mlfq(timeline, cs)
