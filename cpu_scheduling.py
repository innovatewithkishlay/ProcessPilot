import tkinter as tk
from tkinter import messagebox
from scheduling_algorithms import fcfs_scheduling
from gantt_chart import draw_gantt_chart

def schedule_fcfs():
    try:
        process_list = process_entry.get().split(',')
        burst_times = list(map(int, burst_entry.get().split(',')))
        
        if len(process_list) != len(burst_times):
            messagebox.showerror("Input Error", "Number of processes and burst times must be equal")
            return
        
        start_times, completion_times = fcfs_scheduling(burst_times)
        
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
