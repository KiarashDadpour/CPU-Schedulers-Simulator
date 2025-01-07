import matplotlib.pyplot as plt


def average(lst, p: int):
    time = 0
    for i in lst:
        time += i
    return time / p


def fcfs(p, at: list, cbt: list, cs=1):
    current_time = 0
    WT = []
    TT = []
    timeline = []  # برای رسم نمودار گانت

    for process in range(p):
        start_time = max(current_time, at[process])
        end_time = start_time + cbt[process]
        wt = start_time - at[process]
        tt = end_time - at[process]
        WT.append(wt)
        TT.append(tt)
        timeline.append((process + 1, start_time, end_time))  # (PID, Start Time, End Time)
        current_time = end_time + cs  # اضافه کردن زمان کانتکست سوییچ

    return WT, TT, timeline


def plot_gantt(timeline, cs):
    fig, ax = plt.subplots(figsize=(10, 6))
    half_cs = cs / 2  # محاسبه نیمه CS

    for i, process in enumerate(timeline):
        index, start, end = process

        # رسم فرآیند با رنگ آبی
        ax.broken_barh([(start, end - start)], (index - 0.4, 0.8), facecolors='tab:blue')

        # رسم نیمه دوم CS در پایان فرآیند فعلی
        if cs > 0 and i < len(timeline) - 1:  # بررسی اینکه فرآیند آخر نباشد
            cs_start = end
            ax.broken_barh([(cs_start, half_cs)], (index - 0.4, 0.8), facecolors='tab:red', alpha=0.5)

        # رسم نیمه اول CS در ابتدای فرآیند بعدی
        if cs > 0 and i < len(timeline) - 1:
            next_start = timeline[i + 1][1]
            cs_start_next = next_start - half_cs
            ax.broken_barh([(cs_start_next, half_cs)], (timeline[i + 1][0] - 0.4, 0.8), facecolors='tab:orange', alpha=0.5)

    # اضافه کردن نیمه CS به پایان فرآیند آخر
    if cs > 0:
        last_process_end = timeline[-1][2]
        ax.broken_barh([(last_process_end, half_cs)], (len(timeline) - 0.4, 0.8), facecolors='tab:green', alpha=0.5)

    ax.set_ylim(0, len(timeline) + 1)
    ax.set_xlim(0, max(t[2] for t in timeline) + cs)
    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_yticks([t[0] for t in timeline])
    ax.set_yticklabels([f"P{t[0]}" for t in timeline])
    ax.grid(True)
    max_time = max(t[2] for t in timeline) + cs
    ax.set_xticks(range(0, max_time + 1, 2))
    plt.title("FCFS")
    plt.show()


p = 5
at = [0, 2, 3, 4, 5]
cbt = [10, 8, 3, 7, 12]
cs = 1  

WT, TT, timeline = fcfs(p, at, cbt, cs)

print("Waiting Times:", WT)
print("Turnaround Times:", TT)
wtbar = average(WT, p)
ttbar = average(TT, p)
print("Average of WT:", wtbar)
print("Average of TT:", ttbar)

plot_gantt(timeline, cs)
