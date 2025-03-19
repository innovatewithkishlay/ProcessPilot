import tkinter as tk
from tkinter import ttk
import psutil
import subprocess

def update_process_list():
    for row in tree.get_children():
        tree.delete(row)
    
    high_cpu = False
    high_mem = False
    total_cpu = 0
    total_mem = 0

    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            cpu = proc.info['cpu_percent']
            mem = proc.info['memory_percent']
            
            total_cpu += cpu
            total_mem += mem

            if cpu > 50:  # If a process is using >50% CPU
                high_cpu = True
            if mem > 50:  # If a process is using >50% Memory
                high_mem = True

            tree.insert("", "end", values=(pid, name, f"{cpu:.2f}%", f"{mem:.2f}%"))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if high_cpu or high_mem:
        status_label.config(text="⚠️ High Resource Usage Detected!", fg="red")
    else:
        status_label.config(text="✅ Everything is Running Fine!", fg="green")

    root.after(2000, update_process_list)  

def kill_process():
    selected_item = tree.selection()
    if selected_item:
        pid = tree.item(selected_item, "values")[0]
        try:
            subprocess.run(["taskkill", "/F", "/PID", pid], check=True)
            update_process_list()
        except subprocess.CalledProcessError:
            status_label.config(text=f"Failed to terminate process (PID={pid})", fg="red")

def give_advice():
    advice_text = "🔹 Close unnecessary background apps.\n"
    advice_text += "🔹 Check Task Manager for unusual apps.\n"
    advice_text += "🔹 Restart heavy applications if lagging.\n"

    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            cpu = proc.info['cpu_percent']
            mem = proc.info['memory_percent']
            if cpu > 50 or mem > 50:
                advice_text += f"⚠️ Consider closing {proc.info['name']} (CPU: {cpu:.2f}%, MEM: {mem:.2f}%)\n"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    advice_label.config(text=advice_text, fg="blue")

root = tk.Tk()
root.title("Advanced Process Monitor")
root.geometry("800x500")
root.configure(bg="yellow")

columns = ("PID", "Process Name", "CPU %", "Memory %")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15, style="Custom.Treeview")

style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="black", background="grey")
style.configure("Treeview", font=("Arial", 11), rowheight=30) 
style.map("Treeview", background=[("selected", "#cce5ff")])  

for col in columns:
    tree.heading(col, text=col, anchor="center")
    tree.column(col, anchor="center", width=180, stretch=tk.NO)

tree.pack(pady=10, padx=10, fill="both", expand=True)

status_label = tk.Label(root, text="Checking System...", font=("Arial", 12, "bold"), bg="yellow")
status_label.pack(pady=5)

kill_button = tk.Button(root, text="Kill Selected Process", command=kill_process, bg="red", fg="white", font=("Arial", 12, "bold"))
kill_button.pack(pady=5)

advice_button = tk.Button(root, text="Get Advice", command=give_advice, bg="blue", fg="white", font=("Arial", 12, "bold"))
advice_button.pack(pady=5)

advice_label = tk.Label(root, text="", font=("Arial", 11, "bold"), bg="yellow")
advice_label.pack(pady=5)

update_process_list()

root.mainloop()
