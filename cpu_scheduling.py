import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

def draw_gantt_chart(processes, burst_times, start_times):
    fig, ax = plt.subplots(figsize=(10, 4))
    y_labels = []
    colors = ["red", "blue", "green", "purple", "orange"]
    for i, process in enumerate(processes):
        ax.barh(y=0, left=start_times[i], width=burst_times[i], color=colors[i % len(colors)], edgecolor="black")
        ax.text(start_times[i] + burst_times[i] / 2, 0, f"{process}", ha='center', va='center', color='white', fontsize=12)
        y_labels.append(process)
    
    ax.set_xticks(np.arange(0, sum(burst_times) + 1, 1))
    ax.set_yticks([])
    ax.set_title("Gantt Chart for CPU Scheduling")
    ax.set_xlabel("Time")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

def schedule_fcfs():
    try:
        process_list = process_entry.get().split(',')
        burst_times = list(map(int, burst_entry.get().split(',')))
        if len(process_list) != len(burst_times):
            messagebox.showerror("Input Error", "Number of processes and burst times must be equal")
            return
        
        start_times = [0] * len(process_list)
        for i in range(1, len(process_list)):
            start_times[i] = start_times[i - 1] + burst_times[i - 1]
        
        draw_gantt_chart(process_list, burst_times, start_times)
    except ValueError:
        messagebox.showerror("Input Error", "Enter valid numbers for burst times")

# GUI Setup
root = tk.Tk()
root.title("CPU Scheduling Visualizer")
root.geometry("400x300")

tk.Label(root, text="Enter Processes (comma-separated):").pack()
process_entry = tk.Entry(root)
process_entry.pack()

tk.Label(root, text="Enter Burst Times (comma-separated):").pack()
burst_entry = tk.Entry(root)
burst_entry.pack()

tk.Button(root, text="Run FCFS Scheduling", command=schedule_fcfs).pack(pady=10)

root.mainloop()
