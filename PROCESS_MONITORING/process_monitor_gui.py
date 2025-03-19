import tkinter as tk
from tkinter import ttk
import psutil
import subprocess


def update_process_list():
    for row in tree.get_children():
        tree.delete(row)
    
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            cpu = proc.info['cpu_percent']
            mem = proc.info['memory_percent']
            tree.insert("", "end", values=(pid, name, f"{cpu:.2f}%", f"{mem:.2f}%"))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    root.after(2000, update_process_list) 

s
def kill_process():
    selected_item = tree.selection()
    if selected_item:
        pid = tree.item(selected_item, "values")[0]
        try:
            subprocess.run(["taskkill", "/F", "/PID", pid], check=True)
            update_process_list()
        except subprocess.CalledProcessError:
            status_label.config(text=f"Failed to terminate process (PID={pid})", fg="red")


root = tk.Tk()
root.title("Process Monitor")
root.geometry("700x400")
root.configure(bg="white")


columns = ("PID", "Process Name", "CPU %", "Memory %")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)


style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="black")
style.configure("Treeview", font=("Arial", 11)) 
style.configure("Treeview", rowheight=25)  
style.map("Treeview", background=[("selected", "#cce5ff")])  


for col in columns:
    tree.heading(col, text=col, anchor="center")
    tree.column(col, anchor="center", width=150, stretch=tk.NO)

tree.pack(pady=10, padx=10, fill="both", expand=True)


kill_button = tk.Button(root, text="Kill Selected Process", command=kill_process, bg="red", fg="white", font=("Arial", 12, "bold"))
kill_button.pack(pady=10)


status_label = tk.Label(root, text="", font=("Arial", 12), bg="white")
status_label.pack()

update_process_list()


root.mainloop()
