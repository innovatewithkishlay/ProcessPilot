import matplotlib.pyplot as plt
import numpy as np

def draw_gantt_chart(processes, burst_times, start_times):
    fig, ax = plt.subplots(figsize=(10, 4))
    colors = ["red", "blue", "green", "purple", "orange"]
    
    for i, process in enumerate(processes):
        ax.barh(y=0, left=start_times[i], width=burst_times[i], 
                color=colors[i % len(colors)], edgecolor="black")
        ax.text(start_times[i] + burst_times[i] / 2, 0, f"{process}", 
                ha='center', va='center', color='white', fontsize=12)
    
    ax.set_xticks(np.arange(0, sum(burst_times) + 1, 1))
    ax.set_yticks([])
    ax.set_title("Gantt Chart for CPU Scheduling")
    ax.set_xlabel("Time")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()
