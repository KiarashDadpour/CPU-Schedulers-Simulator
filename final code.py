import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import threading
from collections import deque
import tkinter as tk
import webbrowser

class MLFQPage(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("MLFQ")
        self.geometry(f"600x600") 
        self.selected_algorithms = ["RR", "RR", "SRTF", "FCFS"]  # Defaults

        # Labels and combo boxes for queue algorithms
        self.label1 = customtkinter.CTkLabel(self, text="Preemptive 1:")
        self.label1.pack()
        self.options1 = ["RR", "SRTF"]
        self.combobox1 = customtkinter.CTkComboBox(
            self, values=self.options1, command=lambda _: self.update_algorithm(0, self.combobox1.get())
        )
        self.combobox1.pack()

        self.label2 = customtkinter.CTkLabel(self, text="Preemptive 2:")
        self.label2.pack()
        self.combobox2 = customtkinter.CTkComboBox(
            self, values=self.options1, command=lambda _: self.update_algorithm(1, self.combobox2.get())
        )
        self.combobox2.pack()

        self.label3 = customtkinter.CTkLabel(self, text="Preemptive 3:")
        self.label3.pack()
        self.combobox3 = customtkinter.CTkComboBox(
            self, values=self.options1, command=lambda _: self.update_algorithm(2, self.combobox3.get())
        )
        self.combobox3.pack()

        self.label4 = customtkinter.CTkLabel(self, text="Non-Preemptive:")
        self.label4.pack()
        self.options2 = ["FCFS", "SPN", "HRRN"]
        self.combobox4 = customtkinter.CTkComboBox(
            self, values=self.options2, command=lambda _: self.update_algorithm(3, self.combobox4.get())
        )
        self.combobox4.pack()

        # Confirm button
        self.confirm_button = customtkinter.CTkButton(self, text="Confirm", command=self.confirm_selection)
        self.confirm_button.pack(pady=10)

        self.selected_algorithms = {}  # To store algorithm for each queue

    def update_algorithm(self, index, choice):
        """Update the algorithm for the specified queue."""
        self.selected_algorithms[index] = choice

    def confirm_selection(self):
        """Store selected algorithms in the parent and close the window."""
        if self.master is None:
            print("Error: Parent window not found!")
            return
        if not hasattr(self.master, 'mlfq_algorithms'):
            self.master.mlfq_algorithms = []
        
        self.master.mlfq_algorithms = [
            self.combobox1.get(),
            self.combobox2.get(),
            self.combobox3.get(),
            self.combobox4.get(),
        ]
        print(f"MLFQ Algorithms Updated: {self.master.mlfq_algorithms}")
        self.destroy()
         
class InfoPage(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.image_references = []
        self.title("Info Page")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}") 

        # Create a Text Widget directly
        self.text_widget = tk.Text(self, wrap="word", font=("Arial", 16), padx=10, pady=10)
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=10)
    # def insert_image(self, text_widget, image_path):
    #     """Insert an image into the text widget at the current position."""
    #     image = Image.open(image_path)
    #     image = image.resize((300, 200))  # تنظیم سایز تصویر
    #     photo = ImageTk.PhotoImage(image)

    #     # درج تصویر در ویجت Text
    #     text_widget.image_create("end", image=photo)
    #     text_widget.insert("end", "\n")  # اضافه کردن خط جدید بعد از عکس

    #     # نگهداری مرجع تصویر برای جلوگیری از حذف شدن آن
    #     self.image_references.append(photo)
    #     # HTML-like content
        self.html_content = """
<p>
   <strong>FCFS</strong> 
</p>
<p>
  First-Come, First-Served (FCFS) is one of the simplest CPU scheduling algorithms, where processes are executed in the exact order of their arrival. It operates on a <em>non-preemptive</em> basis, meaning once a process starts execution, it runs to completion before the next process begins. FCFS is easy to implement using a simple FIFO (First-In, First-Out) queue, ensuring fairness by servicing requests in the order they arrive. However, it can lead to significant performance issues, particularly the <strong>convoy effect</strong>, where shorter processes get stuck waiting behind longer ones, leading to high average waiting and turnaround times. This algorithm does not prioritize processes based on their importance or execution time, making it unsuitable for time-sensitive applications. FCFS is best suited for batch processing systems with predictable workloads, where response time is not a critical concern. Despite its limitations, FCFS is still widely used in disk scheduling and situations where tasks must be executed sequentially.
<p>
   <strong>SPN</strong> 
</p>
<p>
  Shortest Process Next (SPN), also known as Shortest Job Next (SJN), is a CPU scheduling algorithm that selects the process with the shortest expected execution time. It operates on a <em>non-preemptive</em> basis, meaning once a process starts execution, it runs to completion without interruption. SPN minimizes average waiting and turnaround times by prioritizing shorter jobs, making it optimal in scenarios where process execution times are known in advance. However, it suffers from <strong>starvation</strong>, where longer processes may be delayed indefinitely if shorter ones keep arriving. Additionally, predicting process execution times accurately can be challenging, which may lead to inefficiencies. This algorithm is best suited for batch processing environments with predictable workloads and limited process variations.
</p>

<p>
   <strong>HRRN</strong> 
</p>
<p>
  Highest Response Ratio Next (HRRN) is a CPU scheduling algorithm that aims to improve process scheduling fairness by selecting the process with the highest response ratio, calculated as <em>(waiting time + service time) / service time</em>. It operates on a <em>non-preemptive</em> basis, ensuring that once a process starts execution, it runs until completion. HRRN effectively addresses the issue of starvation seen in shortest job first algorithms by gradually increasing the priority of longer waiting processes. It provides a good balance between short and long processes, leading to improved turnaround times. However, since it requires frequent calculation of response ratios for all processes, it may introduce some computational overhead. This algorithm is particularly effective in environments with varying job sizes and where both short and long tasks must be handled efficiently.
</p>

<p>
   <strong>RR</strong> 
</p>
<p>
  Round Robin (RR) is a widely used CPU scheduling algorithm that assigns a fixed time quantum to each process in a cyclic order. It operates on a <em>preemptive</em> basis, meaning a running process is interrupted if it exceeds its allocated time slice and placed back in the ready queue. RR ensures fairness by giving equal opportunity to all processes, making it particularly well-suited for time-sharing and multitasking systems. However, its performance heavily depends on the choice of time quantum; a very small quantum results in excessive context switching overhead, while a large quantum may lead to poor response times. RR generally provides better response times for interactive users but may result in higher average waiting times compared to other scheduling algorithms. It is commonly used in operating systems designed for interactive environments such as operating system kernels and real-time systems.
</p>

<p>
   <strong>SRTF</strong> 
</p>
<p>
  Shortest Remaining Time First (SRTF), also known as Preemptive Shortest Job Next, is a CPU scheduling algorithm that selects the process with the shortest remaining execution time at any given moment. It operates on a <em>preemptive</em> basis, meaning a newly arriving process with a shorter burst time can preempt the currently running process. SRTF provides optimal average waiting and turnaround times but introduces challenges such as <strong>starvation</strong> of longer processes and the overhead of frequent context switching. Additionally, it requires precise knowledge of remaining execution times, which may not always be feasible. This algorithm is particularly beneficial for environments where short tasks arrive frequently, such as real-time processing and interactive systems that prioritize fast response times.
</p>

<p>
   <strong>MLFQ</strong> 
</p>
<p>
  Multi-Level Feedback Queue (MLFQ) is an advanced CPU scheduling algorithm that categorizes processes into multiple priority-based queues, with each queue having its own scheduling policy and time quantum. It operates on a <em>preemptive</em> basis, allowing dynamic adjustments to process priorities based on their behavior and execution history. Processes that frequently utilize CPU time are gradually moved to lower-priority queues, while interactive processes that require quick responses are kept in higher-priority queues. MLFQ effectively balances fairness and system responsiveness, making it suitable for general-purpose operating systems. However, it can be complex to configure and requires careful tuning of parameters such as the number of queues, priority adjustment policies, and demotion/promotion criteria. MLFQ is ideal for systems with diverse workloads, such as modern operating systems, gaming applications, and cloud computing environments.
</p>


"""

        # Display HTML-like content
        self.display_html_like_content(self.text_widget, self.html_content)

        # Disable editing after inserting content
        self.text_widget.config(state="disabled")

    def display_html_like_content(self, text_widget, content):
        # Enable text widget for inserting
        text_widget.config(state="normal")

        lines = content.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                text_widget.insert("end", "\n")
                continue  # Skip empty lines

            # Check for HTML-like tags
            if "InsertImage1.1" in line:
                self.insert_image(text_widget, "./IMG_8565.jpg")
                continue
            elif "InsertImage1.2" in line:
                self.insert_image(text_widget, "./IMG_8566.jpg")
                continue
            while "<" in line and ">" in line:
                start_tag = line.find("<")
                end_tag = line.find(">")
                tag = line[start_tag + 1:end_tag]
                line = line[:start_tag] + line[end_tag + 1:]

                if tag.startswith("/"):
                    tag = tag[1:]
                    text_widget.tag_remove(tag, "end-1c linestart", "end-1c lineend")
                else:
                    if tag == "strong":
                        text_widget.tag_configure(tag, font=("Arial", 12, "bold"))
                    elif tag == "em":
                        text_widget.tag_configure(tag, font=("Arial", 12, "italic"))
                    elif tag == "p":
                        # Add spacing for paragraphs
                        text_widget.insert("end", "\n")
                        continue

                    # Insert formatted text with the applied tag
                    text_widget.insert("end", line[:line.find("<")], tag)
                    line = line[line.find("<"):]

            # Insert the remaining text without adding unnecessary newlines
            text_widget.insert("end", line + "\n")

        text_widget.insert("end","\n")  # Ensure a final newline for readability
        text_widget.config(state="disabled")
                 
class ContactCard(customtkinter.CTkFrame):
    def __init__(self, master, img_path, email, github, **kwargs):
        super().__init__(master, corner_radius=12, fg_color=("gray95", "#2b2b2b"), **kwargs)
        self.grid_columnconfigure(0, weight=1)

        # تصویر (CTkImage مقیاس‌پذیر و هماهنگ با تم)
        img = customtkinter.CTkImage(light_image=Image.open(img_path), size=(200, 200))
        customtkinter.CTkLabel(self, image=img, text="").grid(row=0, column=0, padx=16, pady=(16, 8))

        # استایل لینک
        link_font  = customtkinter.CTkFont(size=14, underline=True)
        link_color = ("#1D4ED8", "#93C5FD")  # آبی خوانا در هر دو تم

        # ایمیل (کلیک = mailto)
        email_lbl = customtkinter.CTkLabel(self, text=email, font=link_font,
                                 text_color=link_color, cursor="hand2",
                                 wraplength=260, anchor="center")
        email_lbl.grid(row=1, column=0, padx=16, pady=(0, 6), sticky="ew")
        email_lbl.bind("<Button-1>", lambda e: webbrowser.open_new(f"mailto:{email}"))

        # گیت‌هاب (نمایش کوتاه ولی با لینک کامل)
        gh_lbl = customtkinter.CTkLabel(self, text="GitHub profile", font=link_font,
                              text_color=link_color, cursor="hand2", anchor="center")
        gh_lbl.grid(row=2, column=0, padx=16, pady=(0, 16), sticky="ew")
        gh_lbl.bind("<Button-1>", lambda e, url=github: webbrowser.open_new(url))

class ContactPage(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.minsize(900, 600)

        # ریشهٔ گرید
        self.grid_rowconfigure(0, weight=1)  # spacer بالا
        self.grid_rowconfigure(1, weight=0)  # container کارت‌ها
        self.grid_rowconfigure(2, weight=0)  # Close
        self.grid_rowconfigure(3, weight=1)  # spacer پایین
        self.grid_columnconfigure(0, weight=1)

        # کانتینر اصلی (دلخواه: ScrollableFrame اگر محتوا زیاد شد)
        container = customtkinter.CTkFrame(self, fg_color="transparent")
        container.grid(row=1, column=0, sticky="nsew", padx=24, pady=0)

        # سه ستون هم‌عرض
        container.grid_rowconfigure(0, weight=1)  # spacer بالا
        container.grid_rowconfigure(1, weight=0)  # ردیف کارت‌ها
        container.grid_rowconfigure(2, weight=1)  # spacer پایین
        container.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")

        # داده‌ها
        contacts = [
            {"img_path": "./kiarash.jpeg",
             "email": "kiarash.dadpour@gmail.com",
             "github": "https://github.com/KiarashDadpour"},
            {"img_path": "./IMG_8581.JPG",
             "email": "assalmahmodi82@gmail.com",
             "github": "https://github.com/AssalMahmodi"},
            {"img_path": "./2025-01-25 01.33.56.jpg",
             "email": "pari041503@gmail.com",
             "github": "https://github.com/pari041503"},
        ]

        # ساخت کارت‌ها
        row_idx = 1
        for col, c in enumerate(contacts):
            card = ContactCard(container, **c, width=300, height=320)
            card.grid(row=row_idx, column=col, padx=12, pady=12, sticky="n")

        # دکمهٔ بستن (وسط پایین)
        close_btn = customtkinter.CTkButton(self, text="Close", width=160, command=self.destroy)
        close_btn.grid(row=3, column=0, pady=(150, 24), sticky="n")

try:
    import pandas as pd
    HAS_PANDAS = True
except Exception:
    HAS_PANDAS = False
        
def average(lst):
    return sum(lst) / len(lst)   
        
### FCFS
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
    fig = Figure(figsize=(10, 4), dpi=100)
    ax = fig.add_subplot(111)
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
    ax.set_title("FCFS Gantt Chart")
    return fig

###  RR
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
    fig = Figure(figsize=(10, 4), dpi=100)
    ax = fig.add_subplot(111)
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
    ax.set_title("RR Gantt Chart")
    return fig

### SPN
def spn(p, at: list, cbt: list, cs: int):
    current_time = 0
    WT = deque([0] * p)
    TT = deque([0] * p)

    completed_count = 0
    completed = deque([False] * p)
    timeline = deque()

    while completed_count < p:
        Q = deque()
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
    RT = WT
    return WT, TT, RT, timeline

def find_min(Q: deque, cbt: list):
    min_value = float("inf")
    index_value = -1
    for index in Q:
        if cbt[index] < min_value:
            min_value = cbt[index]
            index_value = index
    return index_value

def plot_gantt_spn(timeline, cs):
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)
    half_cs = cs / 2  # Compute half of CS time

    for i, process in enumerate(timeline):
        index, start, end = process
        y_pos = index * 1.5

        # Draw the process bar in blue
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

    ax.set_ylim(0, (len(timeline) + 1) * 1.5)
    ax.set_xlim(0, max(t[2] for t in timeline) + cs)
    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_yticks([t[0] * 1.5 for t in timeline])
    ax.set_yticklabels([f"P{t[0]}" for t in timeline])
    ax.grid(True)
    max_time = max(t[2] for t in timeline) + cs
    ax.set_xticks(range(0, max_time + 1, 2))
    ax.set_title("SPN Gantt Chart")
    return fig

### HRRN
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
            next_process_arrive = float('inf')
            for i in range(p):
                if not completed[i]:
                    next_process_arrive = min(next_process_arrive, at[i])
            current_time = next_process_arrive
            continue

        rpr = calculate_rpr(ready_processes, current_time, at, cbt)

        max_index = find_max_rpr(rpr, at)

        start_time = current_time
        current_time += cbt[max_index]
        end_time = current_time

        TT[max_index] = end_time - at[max_index]
        WT[max_index] = TT[max_index] - cbt[max_index]

        completed[max_index] = True
        completed_count += 1

        timeline.append((max_index + 1, start_time, end_time))

        current_time += cs

    RT = WT
    return WT, TT ,RT,  timeline

def find_ready_processes(p, at, current_time, completed):
    ready_processes = []
    for i in range(p):
        if at[i] <= current_time and not completed[i]:
            ready_processes.append(i)
    return ready_processes

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

def calculate_rpr(ready_processes, current_time, at, cbt):
    ready_processes = list(ready_processes)

    rprs = []
    for process in ready_processes:
        waiting_time = max(0, current_time - at[process])
        rpr = (waiting_time + cbt[process]) / cbt[process]
        rprs.append((rpr, process))

    return list(rprs)

def plot_gantt_hrrn(timeline, cs):
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)
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

    ax.set_ylim(0, (len(timeline) + 1) * 1.5)
    ax.set_xlim(0, max(t[2] for t in timeline) + cs)
    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_yticks([t[0] * 1.5 for t in timeline])
    ax.set_yticklabels([f"P{t[0]}" for t in timeline])
    ax.grid(True)
    max_time = max(t[2] for t in timeline) + cs
    ax.set_xticks(range(0, max_time + 1, 2))
    ax.set_title("HRRN Gantt Chart")
    return fig

### SRTF
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
            next_process_arrive = float('inf')
            for i in range(p):
                if not completed[i]:
                    next_process_arrive = min(next_process_arrive, at[i])

            current_time = next_process_arrive
            continue

        current_process = find_shortest_process(arrived_processes, cbt1)

        if not first_run[current_process]:
            RT[current_process] = current_time - at[current_process]
            first_run[current_process] = True

        if current_running_time[current_process] >= quantum:
            current_time += cs
            current_running_time[current_process] = 0

            arrived_processes.clear()
            for i in range(p):
                if at[i] <= current_time and not completed[i] and cbt1[i] > 0:
                    arrived_processes.append(i)

            if len(arrived_processes) == 0:
                continue

            current_process = find_shortest_process(arrived_processes, cbt1)

        exe_time = min(quantum - current_running_time[current_process], cbt1[current_process])

        current_time += exe_time
        cbt1[current_process] -= exe_time
        current_running_time[current_process] += exe_time

        timeline.append((current_process + 1, current_time - exe_time, current_time))

        if cbt1[current_process] == 0:
            completed[current_process] = True
            completed_count += 1
            current_running_time[current_process] = 0

            TT[current_process] = current_time - at[current_process]
            WT[current_process] = TT[current_process] - cbt[current_process]
            current_time += cs

    return WT, TT, RT, timeline
    
def find_shortest_process(arrived_processes, cbt1):
    shortest_process = None
    shortest_time = float('inf')

    for process in arrived_processes:
        if cbt1[process] < shortest_time:
            shortest_time = cbt1[process]
            shortest_process = process

    return shortest_process

def plot_gantt_srtf(timeline, cs):
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)
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

    ax.set_ylim(0, (len(timeline) + 1) * 1.5)
    ax.set_xlim(0, max(t[2] for t in timeline) + cs)
    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_yticks([t[0] * 1.5 for t in timeline])
    ax.set_yticklabels([f"P{t[0]}" for t in timeline])
    ax.grid(True)
    max_time = max(t[2] for t in timeline) + cs
    ax.set_xticks(range(0, max_time + 1, 2))
    ax.set_title("SRTF Gantt Chart")
    return fig

### NPP
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

def plot_gantt_non_preemptive(timeline, cs):
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)
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
    ax.set_title("Non_PreemptiveـPriority Gantt Chart")
    return fig

### MLFQ
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
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)
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
    ax.set_title("MLFQ Gantt Chart")
    return fig
    
### PP
def get_highest_priority_process(ready_queue, priorities1):
    highest_priority = float('inf')
    selected_process = None

    for process in ready_queue:
        if priorities1[process] < highest_priority:
            highest_priority = priorities1[process]
            selected_process = process

    return selected_process

def preemptive(p, at, cbt, priorities, quantum, cs=1):
    current_time = 0
    WT = [0] * p
    TT = [0] * p
    RT = [0] * p
    timeline = []
    ready_queue = []
    completed_processes = 0
    first_response = [False] * p

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

        if not first_response[selected_process]:
            RT[selected_process] = current_time - at[selected_process]
            first_response[selected_process] = True

        exe_time = min(quantum, cbt1[selected_process])

        next_process_arrive = float('inf')
        for i in range(p):
            if at[i] > current_time and at[i] < current_time + exe_time and cbt1[i] > 0: # not in Q and
                if priorities1[i] < priorities1[selected_process]:
                    next_process_arrive = min(next_process_arrive, at[i])

        if next_process_arrive != float('inf'):
            exe_time = next_process_arrive - current_time

        timeline.append((selected_process + 1, current_time, current_time + exe_time))
        cbt1[selected_process] -= exe_time
        current_time += exe_time

        ready_queue.remove(selected_process)

        if cbt1[selected_process] <= 0:
            TT[selected_process] = current_time - at[selected_process]
            WT[selected_process] = TT[selected_process] - cbt[selected_process]
            completed_processes += 1
        else:
            ready_queue.append(selected_process)

        current_time += cs

    return WT, TT, RT, timeline

def plot_gantt_preemptive(timeline, cs):
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)
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
    ax.set_title("PreemptiveـPriority Gantt Chart")
    return fig
    
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.mlfq_algorithms = ["RR", "RR", "SRTF", "FCFS"]
        ## screen size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()       
        self.geometry(f"{screen_width}x{screen_height}")
        ## screen
        self.title("OS")
        self.columnconfigure(0, weight=0, minsize=300)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0, minsize=300)
        self.rowconfigure(0, weight=1)
        ## slidebar
        self.sidebar_frame = customtkinter.CTkFrame(self)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")   
        self.sidebar_frame.rowconfigure(0, weight=0, minsize=350)
        self.sidebar_frame.rowconfigure(1, weight=1)
        self.sidebar_frame.columnconfigure(0, weight=0, minsize=320)  
        ## Tabview in slide bar (selecting algorithms)
        self.tabview = customtkinter.CTkTabview(self.sidebar_frame)
        self.tabview.grid(row=0, column=0, padx=10, pady=(5, 10), sticky="nsew")
            ## Non-preemptive Tab
        self.tabview.add("Non pre-emptive")
        self.radio_var_non_preemptive = customtkinter.StringVar(value="Non Pre_emptive")
                ## non pre-emptive radio buttons 
        # FCFS
        FCFS=customtkinter.CTkRadioButton(self.tabview.tab("Non pre-emptive"),text=f"FCFS",variable=self.radio_var_non_preemptive,value=f"FCFS")
        # SPN
        SPN=customtkinter.CTkRadioButton(self.tabview.tab("Non pre-emptive"),text=f"SPN",variable=self.radio_var_non_preemptive,value=f"SPN")
        # HRRN
        HRRN=customtkinter.CTkRadioButton(self.tabview.tab("Non pre-emptive"),text=f"HRRN",variable=self.radio_var_non_preemptive,value=f"HRRN")
        # Non_PreemptiveـPriority
        Non_Preemptive_Priority=customtkinter.CTkRadioButton(self.tabview.tab("Non pre-emptive"),text=f"Non-Preemptive Priority (NPP)",variable=self.radio_var_non_preemptive,value=f"Non-Preemptive Priority")
        ## non pre-emptive button
        self.show_button_non_preemptive = customtkinter.CTkButton(self.tabview.tab("Non pre-emptive"),text="choose",command=self.frame0_3)
        
        
        tab = self.tabview.tab("Non pre-emptive")

        FCFS.grid(row=0, column=0, sticky="w", pady=(30,10), padx=10)
        SPN.grid(row=1, column=0, sticky="w", pady=10, padx=10)
        HRRN.grid(row=2, column=0, sticky="w", pady=10, padx=10)
        Non_Preemptive_Priority.grid(row=3, column=0, sticky="w", pady=10, padx=10)

        self.show_button_non_preemptive.grid(row=4, column=0, sticky="w", pady=(100,10), padx=10)


        # Preemptive Tab
        self.tabview.add("Pre-emptive")
        self.radio_var_preemptive = customtkinter.StringVar(value="Pre-emptive")

        tab = self.tabview.tab("Pre-emptive")

        # RR
        RR = customtkinter.CTkRadioButton(
            tab, text="RR", variable=self.radio_var_preemptive, value="RR"
        )
        RR.grid(row=0, column=0, sticky="w", pady=(30, 10), padx=10)

        # SRTF
        SRTF = customtkinter.CTkRadioButton(
            tab, text="SRTF", variable=self.radio_var_preemptive, value="SRTF"
        )
        SRTF.grid(row=1, column=0, sticky="w", pady=10, padx=10)

        # MLFQ
        MLFQ = customtkinter.CTkRadioButton(
            tab, text="MLFQ", variable=self.radio_var_preemptive, value="MLFQ", command=self.MLFQPage
        )
        MLFQ.grid(row=2, column=0, sticky="w", pady=10, padx=10)

        # Preemptive Priority
        Preemptive_Priority = customtkinter.CTkRadioButton(
            tab, text="Preemptive Priority (PP)", variable=self.radio_var_preemptive, value="Preemptive Priority"
        )
        Preemptive_Priority.grid(row=3, column=0, sticky="w", pady=10, padx=10)

        # Choose button
        self.show_button_preemptive = customtkinter.CTkButton(
            tab, text="choose", command=self.frame0_2
        )
        self.show_button_preemptive.grid(row=4, column=0, sticky="w", pady=(100, 10), padx=10)

        # Ensure column 0 stays left-aligned, and column 1 expands if needed
        tab.grid_columnconfigure(0, weight=0)
        tab.grid_columnconfigure(1, weight=1)



        
        ## frame0 in slide bar (Entry)
        self.frame0 = customtkinter.CTkFrame(self.sidebar_frame)
        self.frame0.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 15))
        self.frame0.columnconfigure(0, weight=1)  
        self.frame0.rowconfigure(0, weight=0)     
        self.frame0.rowconfigure(1, weight=1)
        self.label_frame0 = customtkinter.CTkLabel(self.frame0,text="Entry place:",text_color=("#495155", "#D3D8DB"),font=customtkinter.CTkFont(size=20, weight="bold"),corner_radius=5,fg_color="transparent")
        self.label_frame0.grid(row=0, column=0, pady=10, padx=10, sticky="nw")  
            ## button in frame0
        self.button_frame0 = customtkinter.CTkButton(self.frame0, text="draw plot", command=lambda: threading.Thread(target=self.draw_plot).start())
        self.button_frame0.grid(row=3, column=0, sticky="s", padx=10, pady=(5,15))
        ## frame0_1 in frame0 (Inputs)
        self.frame0_1 = customtkinter.CTkFrame(self.frame0)
        self.frame0_1.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        ## plot frame
        self.plotframe = customtkinter.CTkFrame(self)
        self.plotframe.grid(row=0, column=1, padx=(10,5), sticky="nsew")
        self.plotframe.columnconfigure(0, weight=1)
        self.plotframe.rowconfigure(1, weight=1)
        self.labelplotframe = customtkinter.CTkLabel(self.plotframe,text="plot frame:",text_color=("#495155", "#D3D8DB"),font=customtkinter.CTkFont(size=20, weight="bold"),corner_radius=5,fg_color="transparent")
        self.labelplotframe.grid(row=0, column=0, pady=10, padx=10, sticky="new")
        self.plotframe1 = customtkinter.CTkFrame(self.plotframe)
        self.plotframe1.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        ## informationFrame
        self.infFrame = customtkinter.CTkFrame(self)
        self.infFrame.grid(row=0, column=2, padx=(5,10), sticky="nsew")
        self.infFrame.columnconfigure(0, weight=0, minsize=300)
        self.infFrame.rowconfigure(0, weight=1)
        # self.infFrame.rowconfigure(1,weight=0, minsize=300)
        self.infFrame.rowconfigure(1, weight=0)
        self.infFrame.rowconfigure(2, weight=0)
        results = customtkinter.CTkFrame(self.infFrame)
        results.grid(row=0, column=0, pady=(10,5), padx=10, sticky="nsew")   
        # recommend = customtkinter.CTkFrame(self.infFrame)
        # recommend.grid(row=1, column=0, pady=5, padx=10, sticky="nsew")
        # info_contact = customtkinter.CTkFrame(self.infFrame)
        # info_contact.grid(row=2, column=0, pady=(5,10), padx=10, sticky="nsew")
        button_info = customtkinter.CTkButton(self.infFrame, text="info", command=self.infopage)
        button_contact = customtkinter.CTkButton(self.infFrame, text="contact", command=self.contactpage)
        # info_contact.columnconfigure(0, weight=1)
        # info_contact.rowconfigure(0, weight=0)
        # info_contact.rowconfigure(1, weight=1)
        button_info.grid(row=1, column=0, pady=(15,5), sticky="s")
        button_contact.grid(row=2, column=0, pady=(5,15), sticky="s")
    def infopage(self):
        InfoPage(self)
    def contactpage(self):
        ContactPage(self)
    def MLFQPage(self):
        """Open the MLFQ configuration window."""
        if not hasattr(self, "mlfq_algorithms") or self.mlfq_algorithms is None:
            self.mlfq_algorithms = ["RR", "RR", "SRTF", "FCFS"]  # مقداردهی اولیه
        if hasattr(self, "mlfq_window") and self.mlfq_window.winfo_exists():
            self.mlfq_window.focus()
        else:
            self.mlfq_window = MLFQPage(self)
            self.mlfq_window.grab_set()
    # def MLFQ (self):
    #     """Create a temporary frame to gather additional MLFQ inputs and confirm selection."""
    #     # Remove the tabview to make space for the new frame
    #     self.tabview.grid_forget()
    #     # Create a new frame in the same location as the tabview
    #     self.mlfq_frame = customtkinter.CTkFrame(self.sidebar_frame)
    #     self.mlfq_frame.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="nsew")
    #     # Add a label to the frame
    #     label = customtkinter.CTkLabel(self.mlfq_frame, text="Enter MLFQ details here:", font=("Arial", 16))
    #     label.pack(pady=20)
    #     # Add a confirm button to remove the frame and restore the tabview
    #     confirm_button = customtkinter.CTkButton(self.mlfq_frame, text="Confirm", command=lambda: self.after(50, self.remove_mlfq_frame))
    #     confirm_button.pack(pady=(200,10))
    # def remove_mlfq_frame(self):
    #     """Remove the temporary MLFQ frame and restore the original tabview."""
    #     self.mlfq_frame.grid_forget()  # Remove the frame
    #     self.tabview.grid(row=0, column=0, padx=10, pady=(5, 10), sticky="nsew")  # Restore tabview
    #     self.update_idletasks()
    ## if any pre_emptive algorithm choose
    def frame0_2(self):
        for widget in self.frame0_1.winfo_children():
            widget.destroy()
        for widget in self.plotframe1.winfo_children():
            widget.destroy()
        self.entry0 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="numbers of processes: ")
        self.entry0.grid(row=1, column=0, padx=(20, 0), pady=(20,10), sticky="nsw")
        self.entry1 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="context swich: ")
        self.entry1.grid(row=2, column=0, padx=(20, 0), pady=10, sticky="nsw")
        self.entry4 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="quantom time: ")
        self.entry4.grid(row=3, column=0, padx=(20, 0), pady=10, sticky="nsw")
        self.entry2 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="AT ")
        self.entry2.grid(row=4, column=0, padx=(20, 0), pady=10, sticky="nsw")
        self.entry3 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="CBT ")
        self.entry3.grid(row=5, column=0, padx=(20, 0), pady=10, sticky="nsw")
        self.entry5 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="priorities if needed: ")
        self.entry5.grid(row=6, column=0, padx=(20, 0), pady=10, sticky="nsw")

    ## if any Non pre_emptive algorithm choose
    def frame0_3(self):
        for widget in self.frame0_1.winfo_children():
            widget.destroy()
        for widget in self.plotframe1.winfo_children():
            widget.destroy()
        self.entry0 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="numbers of processes: ")
        self.entry0.grid(row=1, column=0, padx=(20, 0), pady=(20, 20), sticky="nsw")
        self.entry1 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="context swich:")
        self.entry1.grid(row=2, column=0, padx=(20, 0), pady=(20, 20), sticky="nsw")
        self.entry2 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="AT ")
        self.entry2.grid(row=3, column=0, padx=(20, 0), pady=(20, 20), sticky="nsw")
        self.entry3 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="CBT")
        self.entry3.grid(row=4, column=0, padx=(20, 0), pady=(20, 20), sticky="nsw")
        self.entry4 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="Quantum time (if applicable):")
        self.entry4.grid(row=5, column=0, padx=(20, 0), pady=(20, 20), sticky="nsw")
        self.entry4.grid_remove()
        self.entry5 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="priorities if needed: ")
        self.entry5.grid(row=6, column=0, padx=(20, 0), pady=(20, 20), sticky="nsw")

    def get_inputs(self):
        try:
            # دریافت تعداد پروسه‌ها
            p = int(self.entry0.get())
            
            # دریافت زمان‌های ورود (Arrival Times)
            at = list(map(int, self.entry2.get().split()))
            
            # دریافت زمان‌های اجرای پروسه‌ها (Burst Times)
            cbt = list(map(int, self.entry3.get().split()))
            
            # دریافت زمان جابه‌جایی کانتکست (Context Switch)
            cs = int(self.entry1.get())
            
            # دریافت زمان کوانتوم (در صورتی که وجود داشته باشه)
            q = int(self.entry4.get()) if self.entry4.winfo_ismapped() else None
            
            # دریافت اولویت‌ها (اگر برای الگوریتم خاصی نیاز باشه)
            priorities = list(map(int, self.entry5.get().split())) if self.entry5.winfo_ismapped() else None

            # بررسی هماهنگی تعداد مقادیر ورودی‌ها
            if len(at) != p or len(cbt) != p or (priorities and len(priorities) != p):
                raise ValueError("تعداد مقادیر ورودی با تعداد پروسه‌ها هماهنگ نیست!")

            return p, at, cbt, cs, q, priorities
        except ValueError:
            raise ValueError("فرمت ورودی‌ها صحیح نیست!")

    def draw_plot(self):
        # Clear previous chart and error messages
        for widget in self.plotframe1.winfo_children():
            widget.destroy()
        for widget in self.infFrame.winfo_children():
            if isinstance(widget, customtkinter.CTkFrame):  # Keep other sections intact
                for sub_widget in widget.winfo_children():
                    sub_widget.destroy()

        try:
            
            p, at, cbt, cs, q , priorities = self.get_inputs()
            print("Inputs Retrieved:")
            print("Number of Processes (p):", p)
            print("Arrival Times (at):", at)
            print("Burst Times (cbt):", cbt)
            print("Context Switch (cs):", cs)
            print("Quantum (q):", q)
            print("Priorities:", priorities)
            selected_algorithm = None
            fig = None
            WT, TT, timeline = [], [], []

            # Check which tab is currently selected
            if self.tabview.get() == "Non pre-emptive":
                selected_algorithm = self.radio_var_non_preemptive.get()
            elif self.tabview.get() == "Pre-emptive":
                selected_algorithm = self.radio_var_preemptive.get()
                
            if not selected_algorithm:
                raise ValueError("No algorithm selected.")
            # Handle algorithm selection
            if selected_algorithm == "FCFS":
                WT, TT, RT, timeline = fcfs(p, at, cbt, cs)
                fig = plot_gantt_fcfs(timeline, cs)
            elif selected_algorithm == "SPN":
                WT, TT, RT, timeline = spn(p, at, cbt, cs)
                fig = plot_gantt_spn(timeline, cs)
            elif selected_algorithm == "HRRN":
                WT, TT, RT, timeline = hrrn(p, at, cbt, cs)
                fig = plot_gantt_hrrn(timeline, cs)
            elif selected_algorithm.strip().lower() == "non-preemptive priority".lower():
                WT, TT, RT, timeline = non_preemptive(p, at, cbt, priorities, cs)
                fig = plot_gantt_non_preemptive(timeline, cs)                
            elif selected_algorithm == "SRTF":
                if q is None:
                    label = customtkinter.CTkLabel(self.plotframe1, text="Quantum time is required for SRTF!", text_color="red", font=customtkinter.CTkFont(size=14, weight="bold"))
                    label.pack(pady=20)
                    return
                WT, TT, RT, timeline = srtf(p, at, cbt, cs, q)
                fig = plot_gantt_srtf(timeline, cs)
            elif selected_algorithm == "RR":
                if q is None:
                    label = customtkinter.CTkLabel(self.plotframe1, text="Quantum time is required for Round Robin!", text_color="red", font=customtkinter.CTkFont(size=14, weight="bold"))
                    label.pack(pady=20)
                    return
                WT, TT, RT, timeline = round_robin(p, at, cbt, cs, q)
                fig = plot_gantt_rr(timeline, cs)
            elif selected_algorithm == "MLFQ":
                print("Checking MLFQ algorithms...")
                if self.mlfq_algorithms is None:
                    print("Error: لطفاً ابتدا تنظیمات MLFQ را پیکربندی کنید!")
                    return

                print("Selected algorithms:", self.mlfq_algorithms)
                
                WT, TT, RT, timeline = mlfq_scheduler(
                    p, at, cbt, q, cs,
                    self.mlfq_algorithms[0] if len(self.mlfq_algorithms) > 0 else "RR",
                    self.mlfq_algorithms[1] if len(self.mlfq_algorithms) > 1 else "RR",
                    self.mlfq_algorithms[2] if len(self.mlfq_algorithms) > 2 else "SRTF",
                    self.mlfq_algorithms[3] if len(self.mlfq_algorithms) > 3 else "FCFS"
                )

                print("==== خروجی MLFQ ====")
                print("WT:", WT)
                print("TT:", TT)
                print("RT:", RT)
                print("Timeline:", timeline)
                fig = plot_gantt_mlfq(timeline, cs)

            elif selected_algorithm == "Preemptive Priority":
                if q is None:
                    label = customtkinter.CTkLabel(self.plotframe1, text="Quantum time is required for Round Robin!", text_color="red", font=customtkinter.CTkFont(size=14, weight="bold"))
                    label.pack(pady=20)
                    return
                WT, TT, RT, timeline = preemptive(p, at, cbt, priorities, cs)
                fig = plot_gantt_preemptive(timeline, cs) 
            else:
                raise ValueError("Please select a valid algorithm!")
                # label = customtkinter.CTkLabel(self.plotframe1, text="Please select an algorithm!", text_color="red", font=customtkinter.CTkFont(size=14, weight="bold"))
                # label.pack(pady=20)
                return
            if not self.mlfq_algorithms:
                print("Error: لطفاً ابتدا تنظیمات MLFQ را پیکربندی کنید!")
                return
            print(f"MLFQ algorithms before execution: {self.mlfq_algorithms}")
            if self.mlfq_algorithms is None:
                print("Error: MLFQ algorithms have not been set.")
            # Embed the new Gantt chart figure in the canvas
            if fig:
                canvas = FigureCanvasTkAgg(fig, self.plotframe1)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill="both", expand=True)
                canvas.draw()

            # Display WT and TT results in the results frame
            self.display_results(WT, TT, RT)

        except ValueError as ve:
            label = customtkinter.CTkLabel(self.plotframe1, text=str(ve), text_color="red", font=customtkinter.CTkFont(size=14, weight="bold"))
            label.pack(pady=20)
        except Exception as e:
            label = customtkinter.CTkLabel(self.plotframe1, text="An unexpected error occurred!", text_color="red", font=customtkinter.CTkFont(size=14, weight="bold"))
            label.pack(pady=20)
            print("Unexpected error:", e)
            
    def display_results(self, WT, TT, RT):
        """Displays formatted WT and TT lists in a fixed-size results frame."""
        results_frame = self.infFrame.winfo_children()[0]  # Assuming results frame is the first child
        
        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()

        # Set a fixed size for the results frame to prevent expansion
        results_frame.configure(width=300, height=500)  # Adjust as needed
        results_frame.pack_propagate(False)  # Prevent frame from resizing

        # Create a scrollable frame inside results frame to show content within fixed size
        scrollable_results = customtkinter.CTkScrollableFrame(results_frame, width=280, height=380)
        scrollable_results.pack(fill="both", expand=True, padx=10, pady=10)

        # Add a title for results
        title_label = customtkinter.CTkLabel(scrollable_results, text="Scheduling Results", font=("Arial", 18, "bold"))
        title_label.pack(pady=(10, 5))

        # Display Waiting Time (WT) results
        wt_label_title = customtkinter.CTkLabel(scrollable_results, text="Waiting Times (WT):", font=("Arial", 16, "bold"))
        wt_label_title.pack(pady=(10, 5))

        for i, wt in enumerate(WT, start=1):
            wt_label = customtkinter.CTkLabel(scrollable_results, text=f"WT{i} = {wt}", font=("Arial", 14))
            wt_label.pack(pady=2, padx=5, anchor="w")

        # Display Turnaround Time (TT) results
        tt_label_title = customtkinter.CTkLabel(scrollable_results, text="Turnaround Times (TT):", font=("Arial", 16, "bold"))
        tt_label_title.pack(pady=(10, 5))

        for i, tt in enumerate(TT, start=1):
            tt_label = customtkinter.CTkLabel(scrollable_results, text=f"TT{i} = {tt}", font=("Arial", 14))
            tt_label.pack(pady=2, padx=5, anchor="w")
            
        # Display Response Time (RT) results
        wt_label_title = customtkinter.CTkLabel(scrollable_results, text="Response Times (RT):", font=("Arial", 16, "bold"))
        wt_label_title.pack(pady=(10, 5))
        
        for i, rt in enumerate(RT, start=1):
            wt_label = customtkinter.CTkLabel(scrollable_results, text=f"RT{i} = {rt}", font=("Arial", 14))
            wt_label.pack(pady=2, padx=5, anchor="w")       
        
        # Display Averages
        avg_wt = sum(WT) / len(WT) if WT else 0
        avg_tt = sum(TT) / len(TT) if TT else 0
        avg_rt = sum(RT) / len(RT) if RT else 0
        

        avg_wt_label = customtkinter.CTkLabel(scrollable_results, text=f"Average WT = {avg_wt:.2f}", font=("Arial", 16, "bold"))
        avg_wt_label.pack(pady=(10, 2), padx=5, anchor="w")

        avg_tt_label = customtkinter.CTkLabel(scrollable_results, text=f"Average TT = {avg_tt:.2f}", font=("Arial", 16, "bold"))
        avg_tt_label.pack(pady=(2, 2), padx=5, anchor="w")
        
        avg_tt_label = customtkinter.CTkLabel(scrollable_results, text=f"Average RT = {avg_rt:.2f}", font=("Arial", 16, "bold"))
        avg_tt_label.pack(pady=(2, 10), padx=5, anchor="w")        


app = App()
app.mainloop()
