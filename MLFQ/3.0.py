from collections import deque

def average(lst):
    return sum(lst) / len(lst)

def mlfq_scheduler(p, at, cbt, cs=1, first_queue_algo='RR', second_queue_algo='RR',
                   third_queue_algo='SRTF', last_queue_algo='FCFS'):
    current_time = 0
    WT = [0] * p
    TT = [0] * p
    RT = [0] * p
    timeline = []

    # Create 4 queues
    queues = [deque() for _ in range(4)]
    remaining_time = cbt.copy()
    process_queue_time = [0] * p
    first_response = [False] * p

    # Store selected algorithms
    queue_algorithms = [first_queue_algo, second_queue_algo, third_queue_algo, last_queue_algo]
    print(f"Selected algorithms: {queue_algorithms}")

    # Quantum times for RR queues
    quantum_times = [2, 4, 6]

    unassigned_processes = list(range(p))

    while unassigned_processes or any(queues):
        # Add newly arrived processes
        for process in unassigned_processes[:]:
            if at[process] <= current_time:
                queues[0].append(process)
                unassigned_processes.remove(process)

        executed = False

        # Process each queue
        for queue_level, queue in enumerate(queues):
            if not queue:
                continue

            current_algorithm = queue_algorithms[queue_level]
            process = None
            execute_time = 0

            # Algorithm selection and execution
            if current_algorithm == 'RR':
                if queue:
                    process = queue[0]
                    execute_time = min(remaining_time[process], quantum_times[queue_level])

            elif current_algorithm == 'SRTF':
                if queue:
                    process = min(queue, key=lambda x: remaining_time[x])
                    execute_time = 1

            elif current_algorithm == 'FCFS':
                if queue:
                    process = queue[0]
                    execute_time = remaining_time[process]

            elif current_algorithm == 'SPN':
                if queue:
                    process = min(queue, key=lambda x: remaining_time[x])
                    execute_time = remaining_time[process]

            elif current_algorithm == 'HRRN':
                if queue:
                    # Calculate response ratio for each process
                    response_ratios = {}
                    for proc in queue:
                        waiting_time = current_time - at[proc]
                        response_ratio = (waiting_time + remaining_time[proc]) / remaining_time[proc]
                        response_ratios[proc] = response_ratio
                    process = max(queue, key=lambda x: response_ratios[x])
                    execute_time = remaining_time[process]

            if process is None:
                continue

            # Record first response time
            if not first_response[process]:
                RT[process] = current_time - at[process]
                first_response[process] = True

            # Execute process
            timeline.append((process + 1, current_time, current_time + execute_time))
            remaining_time[process] -= execute_time
            process_queue_time[process] += execute_time

            # Handle process completion or queue changes
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

    return WT, TT, RT, timeline


# Test the scheduler with specific algorithms
p = 5
at = [0, 1, 2, 3, 4]
cbt = [3, 6, 4, 5, 2]
cs = 1

# You can choose algorithms for each queue
a, b, c, timeline = mlfq_scheduler(
    p, at, cbt, cs,
    first_queue_algo='RR',  # Options: 'RR', 'SRTF'
    second_queue_algo='SRTF',  # Options: 'RR', 'SRTF'
    third_queue_algo='RR',  # Options: 'RR', 'SRTF'
    last_queue_algo='FCFS'  # Options: 'FCFS', 'SPN', 'HRRN'
)
print("WT:", a)
print("TT:", b)
print("RT: ", c)
wtbar = average(a)
ttbar = average(b)
rtbar = average(c)
print("Average of WT: ", wtbar)
print("Average of TT: ", ttbar)
print("Average of RT: ", rtbar)
