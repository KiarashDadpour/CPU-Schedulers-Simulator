# CPU Scheduling Algorithms Simulator
### A comprehensive GUI application for simulating and visualizing various CPU scheduling algorithms with interactive Gantt charts and performance metrics.

## 📋 Features
- ### Multiple Scheduling Algorithms Support:
  - #### Non-preemptive:
     - ##### First-Come, First-Served (FCFS)
     - ##### Shortest Process Next (SPN)
     - ##### Highest Response Ratio Next (HRRN)
     - ##### Non-Preemptive Priority (NPP)
   
  - #### Preemptive:
     - ##### Round Robin (RR)
     - ##### Shortest Remaining Time First (SRTF)
     - ##### Multi-Level Feedback Queue (MLFQ)
     - ##### Preemptive Priority (PP)

- ### Interactive GUI:
  - #### Easy-to-use input interface
  - #### Real-time visualization
  - #### Dynamic Gantt charts

- ### Performance Metrics:
  - #### Waiting Time (WT)
  - #### Turnaround Time (TT)
  - ####  Response Time (RT)

## 💻 Usage
### 1. Run the application:
```
python app.py
```
### 2. Select scheduling algorithm type:

- #### Choose between “Pre-emptive” and “Non pre-emptive” tabs
- #### Select specific algorithm

### 3. Enter process details:

- #### Number of processes
- #### Arrival times (AT)
- #### CPU burst times (CBT)
- #### Context switch time
- #### Quantum time (for RR, SRTF)
- #### Priorities (for Priority scheduling)

### 4. Click “Draw Plot” to visualize the scheduling


## 🐳 Docker Support
You can also run this project using Docker:
1. Build the Docker image:

```
docker build -t="CPU-Schedulers" .
```
2. Run the container:
```
docker run -it --rm CPU-Schedulers
```
## 👥 Authors
### Kiarash Dadpour
### Parnian Pourjafari
### Asal Mahmodi Nejad 
