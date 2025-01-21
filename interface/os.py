import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
# from tkinter import Canvas, Frame, Scrollbar
class InfoPage(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Info Page")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()       
        self.geometry(f"{screen_width}x{screen_height}") # اندازه دلخواه
        scrollable_frame = customtkinter.CTkScrollableFrame(self, width=580, text=" ", height=380)
        scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)
class ContactPage(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Contact Page")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()       
        self.geometry(f"{screen_width}x{screen_height}")  
        self.rowconfigure(0, weight=0 )
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        image_kia = Image.open("./kiarash.jpeg")  
        image_kia = image_kia.resize((200, 200))  
        photo = ImageTk.PhotoImage(image_kia)
        image_label_kia = customtkinter.CTkLabel(self, image=photo, text="")
        image_label_kia.image = photo  
        image_label_kia.grid(row=0, column=0, padx=(250,100), pady=50, sticky="nsew")
        image_asal = Image.open("./kiarash.jpeg")  
        image_asal = image_asal.resize((200, 200))  
        photo = ImageTk.PhotoImage(image_asal)
        image_label_asal = customtkinter.CTkLabel(self, image=photo, text="")
        image_label_asal.image = photo  
        image_label_asal.grid(row=0, column=1, padx=100, pady=50, sticky="nsew")
        image_pari = Image.open("./kiarash.jpeg")  
        image_pari = image_pari.resize((200, 200)) 
        photo = ImageTk.PhotoImage(image_pari)
        image_label_pari = customtkinter.CTkLabel(self, image=photo, text="")
        image_label_pari.image = photo  
        image_label_pari.grid(row=0, column=2, padx=(100,250), pady=50, sticky="nsew")
        label_kia = customtkinter.CTkLabel(self, text="email kia", font=("Arial", 16))
        label_kia.grid(row=1, column=0, padx=(250,100), pady=50, sticky="nsew")
        image_label_asal = customtkinter.CTkLabel(self, text="email asal", font=("Arial", 16))
        image_label_asal.grid(row=1, column=1, padx=(100,100), pady=50, sticky="nsew")
        image_label_pari = customtkinter.CTkLabel(self, text="email pari", font=("Arial", 16))
        image_label_pari.grid(row=1, column=2, padx=(100,250), pady=50, sticky="nsew")
        close_button = customtkinter.CTkButton(self, text="Close", command=self.destroy)
        close_button.grid(row=2, column=1, pady=30, sticky="s")

def fcfs(p, at: list, cbt: list, cs=1):
    current_time = 0
    WT = []
    TT = []
    timeline = []  # For Gantt chart
    for process in range(p):
        start_time = max(current_time, at[process])
        end_time = start_time + cbt[process]
        wt = start_time - at[process]
        tt = end_time - at[process]
        WT.append(wt)
        TT.append(tt)
        timeline.append((process + 1, start_time, end_time))  # (PID, Start Time, End Time)
        current_time = end_time + cs  # Add context switch time
    return WT, TT, timeline

def round_robin(p, at: list, cbt: list, cs: int, quantum: int):
    current_time = 0
    cbt1 = cbt[:]  # نگه‌داشتن نسخه اولیه cbt
    WT = [0] * p  # زمان انتظار
    TT = [0] * p  # زمان کل
    completed = [False] * p  # وضعیت تکمیل فرآیندها
    timeline = []  # تایم‌لاین اجرا
    queue = []  # صف فرآیندهای آماده
    while not all(completed):
        # اضافه کردن فرآیندهای رسیده به صف
        for process in range(p):
            if at[process] <= current_time and not completed[process] and process not in queue:
                queue.append(process)
        if not queue:
            # اگر صف خالی است، زمان را به جلو ببرید
            current_time += 1
            continue
        # اجرای فرآیند از صف
        process = queue.pop(0)
        start_time = current_time
        if cbt[process] > quantum:
            current_time += quantum
            cbt[process] -= quantum
        else:
            current_time += cbt[process]
            cbt[process] = 0
            completed[process] = True
            TT[process] = current_time - at[process]  # زمان کل
            WT[process] = TT[process] - cbt1[process]  # زمان انتظار
        # ثبت در تایم‌لاین
        timeline.append((process + 1, start_time, current_time))
        # اضافه کردن زمان Context Switching
        current_time += cs
        # اضافه کردن فرآیندهای جدید به صف
        for process in range(p):
            if at[process] <= current_time and not completed[process] and process not in queue:
                queue.append(process)
    return WT, TT, timeline

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

def create_gantt_figure(timeline, cs=None):
    if cs is None:
        cs=0
    fig = Figure(figsize=(10, 4), dpi=100)
    ax = fig.add_subplot(111)
    half_cs = cs / 2
    for i, process in enumerate(timeline):
        index, start, end = process 
        # Draw the process bar
        ax.broken_barh([(start, end - start)], (index - 0.4, 0.8), facecolors='tab:blue')
        # Draw half CS at the end of the current process
        if cs > 0 and i < len(timeline) - 1:
            cs_start = end
            ax.broken_barh([(cs_start, half_cs)], (index - 0.4, 0.8), facecolors='tab:red', alpha=0.5)
        # Draw half CS at the start of the next process
        if cs > 0 and i < len(timeline) - 1:
            next_start = timeline[i + 1][1]
            cs_start_next = next_start - half_cs
            ax.broken_barh([(cs_start_next, half_cs)], (timeline[i + 1][0] - 0.4, 0.8), facecolors='tab:orange', alpha=0.5)
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
    ax.set_title("FCFS Gantt Chart")
    return fig

def plot_gantt_rr(timeline, cs):
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)
    half_cs = cs / 2
 # Compute half of CS time
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

def plot_gantt_spn(timeline, cs):
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)
    half_cs = cs / 2 # Compute half of CS time
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
    ax.set_title("SPN Gantt Chart")
    return fig

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
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
        self.sidebar_frame.columnconfigure(0, weight=1, minsize=320)   
        ## Tabview in slide bar (selecting algorithms)
        self.tabview = customtkinter.CTkTabview(self.sidebar_frame)
        self.tabview.grid(row=0, column=0, padx=10, pady=(5, 10), sticky="nsew")
            ## Non-preemptive Tab
        self.tabview.add("Non pre-emptive")
        self.radio_var_non_preemptive = customtkinter.StringVar(value="Non Pre_emptive")
                ## non pre-emptive radio buttons 
        # FCFS
        FCFS=customtkinter.CTkRadioButton(self.tabview.tab("Non pre-emptive"),text=f"FCFS",variable=self.radio_var_non_preemptive,value=f"FCFS")
        FCFS.pack(pady=(20,10))
        # SPN
        SPN=customtkinter.CTkRadioButton(self.tabview.tab("Non pre-emptive"),text=f"SPN",variable=self.radio_var_non_preemptive,value=f"SPN")
        SPN.pack(pady=10)
        # HRRN
        HRRN=customtkinter.CTkRadioButton(self.tabview.tab("Non pre-emptive"),text=f"HRRN",variable=self.radio_var_non_preemptive,value=f"HRRN")
        HRRN.pack(pady=10)
                ## non pre-emptive button
        self.show_button_non_preemptive = customtkinter.CTkButton(self.tabview.tab("Non pre-emptive"),text="choose",command=self.frame0_3)
        self.show_button_non_preemptive.pack(pady=(100,10))
            ## Preemptive Tab
        self.tabview.add("Pre-emptive")
        self.radio_var_preemptive = customtkinter.StringVar(value="Pre-emptive")
                ## pre-emptive radio buttons
        # RR                      
        RR=customtkinter.CTkRadioButton(self.tabview.tab("Pre-emptive"),text=f"RR",variable=self.radio_var_preemptive,value=f"RR")
        RR.pack(pady=(20,10))
        # SRTF
        SRTF=customtkinter.CTkRadioButton(self.tabview.tab("Pre-emptive"),text=f"SRTF",variable=self.radio_var_preemptive,value=f"SRTF")
        SRTF.pack(pady=10)
        # MLFQ
        MLFQ=customtkinter.CTkRadioButton(self.tabview.tab("Pre-emptive"),text=f"MLFQ",variable=self.radio_var_non_preemptive,value=f"MLFQ", command=self.MLFQ)
        MLFQ.pack(pady=10)
                ## pre-emptive button
        self.show_button_preemptive = customtkinter.CTkButton(self.tabview.tab("Pre-emptive"),text="choose",command=self.frame0_2)
        self.show_button_preemptive.pack(pady=(100,10))
        ## frame0 in slide bar (Entry)
        self.frame0 = customtkinter.CTkFrame(self.sidebar_frame)
        self.frame0.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 15))
        self.frame0.columnconfigure(0, weight=1)  
        self.frame0.rowconfigure(0, weight=0)     
        self.frame0.rowconfigure(1, weight=1)
        self.label_frame0 = customtkinter.CTkLabel(self.frame0,text="Entry place:",text_color=("#495155", "#D3D8DB"),font=customtkinter.CTkFont(size=20, weight="bold"),corner_radius=5,fg_color="transparent")
        self.label_frame0.grid(row=0, column=0, pady=10, padx=10, sticky="nw")  
            ## button in frame0
        self.button_frame0 = customtkinter.CTkButton(self.frame0, text="draw plot", command=self.draw_plot)
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
        self.infFrame.columnconfigure(0, weight=1)
        self.infFrame.rowconfigure(0, weight=0, minsize=450)
        self.infFrame.rowconfigure(1,weight=0, minsize=300)
        self.infFrame.rowconfigure(2, weight=1, minsize=50)
        results = customtkinter.CTkFrame(self.infFrame)
        results.grid(row=0, column=0, pady=(10,5), padx=10, sticky="nsew")
        recommend = customtkinter.CTkFrame(self.infFrame)
        recommend.grid(row=1, column=0, pady=5, padx=10, sticky="nsew")
        info_contact = customtkinter.CTkFrame(self.infFrame)
        info_contact.grid(row=2, column=0, pady=(5,10), padx=10, sticky="nsew")
        button_info = customtkinter.CTkButton(info_contact, text="info", command=self.infopage)
        button_contact = customtkinter.CTkButton(info_contact, text="contact", command=self.contactpage)
        info_contact.columnconfigure(0, weight=1)
        info_contact.rowconfigure(0, weight=0)
        info_contact.rowconfigure(1, weight=1)
        button_info.grid(row=0, column=0, pady=(15,5), sticky="s")
        button_contact.grid(row=1, column=0, pady=(5,15), sticky="s")
    def infopage(self):
        InfoPage(self)
    def contactpage(self):
        ContactPage(self)
    def MLFQ (self):
        """Create a temporary frame to gather additional MLFQ inputs and confirm selection."""
        # Remove the tabview to make space for the new frame
        self.tabview.grid_forget()
        # Create a new frame in the same location as the tabview
        self.mlfq_frame = customtkinter.CTkFrame(self.sidebar_frame)
        self.mlfq_frame.grid(row=0, column=0, padx=10, pady=(15, 10), sticky="nsew")
        # Add a label to the frame
        label = customtkinter.CTkLabel(self.mlfq_frame, text="Enter MLFQ details here:", font=("Arial", 16))
        label.pack(pady=20)
        # Add a confirm button to remove the frame and restore the tabview
        confirm_button = customtkinter.CTkButton(self.mlfq_frame, text="Confirm", command=self.remove_mlfq_frame)
        confirm_button.pack(pady=(200,10))
    def remove_mlfq_frame(self):
        """Remove the temporary MLFQ frame and restore the original tabview."""
        self.mlfq_frame.destroy()  # Remove the frame
        self.tabview.grid(row=0, column=0, padx=10, pady=(5, 10), sticky="nsew")  # Restore tabview
    ## if any pre_emptive algorithm choose
    def frame0_2(self):
        for widget in self.frame0_1.winfo_children():
            widget.destroy()
        for widget in self.plotframe1.winfo_children():
            widget.destroy()
        self.entry0 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="numbers of processes: ")
        self.entry0.grid(row=1, column=0, padx=(20, 0), pady=(20, 20), sticky="nsw")
        self.entry1 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="context swich: ")
        self.entry1.grid(row=2, column=0, padx=(20, 0), pady=(20, 20), sticky="nsw")
        self.entry4 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="quantom time: ")
        self.entry4.grid(row=3, column=0, padx=(20, 0), pady=(20, 20), sticky="nsw")
        self.entry2 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="AT ")
        self.entry2.grid(row=4, column=0, padx=(20, 0), pady=(20, 20), sticky="nsw")
        self.entry3 = customtkinter.CTkEntry(self.frame0_1, placeholder_text="CBT ")
        self.entry3.grid(row=5, column=0, padx=(20, 0), pady=(20, 20), sticky="nsw")
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
    def get_inputs(self):
        p = int(self.entry0.get())
        at = list(map(int, self.entry2.get().split())) 
        cbt = list(map(int, self.entry3.get().split()))
        cs= int(self.entry1.get()) if self.entry1.get().isdigit() else 0
        q = int(self.entry4.get()) if hasattr(self, 'entry4') and self.entry4.get().isdigit() else None
        if len(at) != p or len(cbt) != p:
            label = customtkinter.CTkLabel(self.plotframe1,text="Number of AT or CBT entries does not match the number of processes!",text_color="red",font=customtkinter.CTkFont(size=14, weight="bold"))
            label.pack(pady=20)
            return
        else:
            return p, at, cbt, cs, q
    def draw_plot(self):
        # Clear previous chart and error messages
        for widget in self.plotframe1.winfo_children():
            widget.destroy()
        try:
            p, at, cbt, cs, q = self.get_inputs()
            selected_algorithm = None
            fig = None
            # Check which tab is currently selected
            if self.tabview.get() == "Non pre-emptive":
                selected_algorithm = self.radio_var_non_preemptive.get()
            elif self.tabview.get() == "Pre-emptive":
                selected_algorithm = self.radio_var_preemptive.get()
            # Handle the selected algorithm accordingly
            if selected_algorithm == "FCFS":
                WT, TT, timeline = fcfs(p, at, cbt, cs)
                fig = create_gantt_figure(timeline, cs)
            elif selected_algorithm == "SPN":
                WT, TT, timeline = spn(p, at, cbt, cs)
                fig = plot_gantt_spn(timeline, cs)
            elif selected_algorithm == "RR":
                if q is None:
                    label = customtkinter.CTkLabel(self.plotframe1, text="Quantum time is required for Round Robin!", text_color="red", font=customtkinter.CTkFont(size=14, weight="bold"))
                    label.pack(pady=20)
                    return
                WT, TT, timeline = round_robin(p, at, cbt, cs, q)
                fig = plot_gantt_rr(timeline, cs)
            else:
                label = customtkinter.CTkLabel(self.plotframe1, text="Please select an algorithm!", text_color="red", font=customtkinter.CTkFont(size=14, weight="bold"))
                label.pack(pady=20)
                return
            # Embed the new Gantt chart figure in the canvas
            if fig:
                canvas = FigureCanvasTkAgg(fig, self.plotframe1)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill="both", expand=True)
                canvas.draw()
        except ValueError:
            label = customtkinter.CTkLabel(self.plotframe1, text="Input error! Please enter valid numbers.", text_color="red", font=customtkinter.CTkFont(size=14, weight="bold"))
            label.pack(pady=20)

app = App()
app.mainloop()
