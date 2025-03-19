import tkinter as tk
from tkinter import ttk, messagebox
import psutil
from utils import advisory_message

def refresh_processes():
    """Fetch and display running processes in the table."""
    for row in tree.get_children():
        tree.delete(row)

    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            tree.insert("", "end", values=(process.info['pid'], process.info['name'], process.info['cpu_percent'], process.info['memory_percent']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    advisory_label.config(text=advisory_message())

def kill_selected_process():
    """Terminates the selected process."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "No process selected!")
        return

    process_data = tree.item(selected_item, "values")
    pid = int(process_data[0])

    try:
        psutil.Process(pid).terminate()
        messagebox.showinfo("Success", f"Process {pid} terminated!")
        refresh_processes()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to terminate process: {e}")

# GUI Setup
root = tk.Tk()
root.title("🔍 Process Monitor")
root.geometry("600x400")

columns = ("PID", "Process Name", "CPU %", "Memory %")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill="both", expand=True)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🔄 Refresh", command=refresh_processes).pack(side="left", padx=5)
tk.Button(btn_frame, text="❌ Kill Process", command=kill_selected_process).pack(side="left", padx=5)

advisory_label = tk.Label(root, text="", fg="red", wraplength=550)
advisory_label.pack(pady=10)

refresh_processes()
root.mainloop()
