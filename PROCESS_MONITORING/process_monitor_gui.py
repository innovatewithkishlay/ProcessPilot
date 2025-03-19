import tkinter as tk
from tkinter import ttk, messagebox
import psutil
from process_monitor import get_processes, kill_process

def refresh_process_list():
    for row in tree.get_children():
        tree.delete(row)
    
    processes = get_processes()
    for proc in processes:
        tree.insert("", "end", values=proc)

def on_kill():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a process to kill.")
        return
    
    proc_id = tree.item(selected_item, 'values')[0]  # Get Process ID
    if kill_process(int(proc_id)):
        messagebox.showinfo("Success", "Process terminated successfully.")
        refresh_process_list()
    else:
        messagebox.showerror("Error", "Failed to terminate the process.")

# GUI Setup
root = tk.Tk()
root.title("Process Monitor")
root.geometry("600x400")

tree = ttk.Treeview(root, columns=("PID", "Name", "CPU%", "Memory%"), show="headings")
tree.heading("PID", text="PID")
tree.heading("Name", text="Name")
tree.heading("CPU%", text="CPU %")
tree.heading("Memory%", text="Memory %")
tree.pack(fill=tk.BOTH, expand=True)

btn_refresh = tk.Button(root, text="Refresh", command=refresh_process_list)
btn_refresh.pack(side=tk.LEFT, padx=10, pady=10)

btn_kill = tk.Button(root, text="Kill Process", command=on_kill)
btn_kill.pack(side=tk.RIGHT, padx=10, pady=10)

refresh_process_list()
root.mainloop()
