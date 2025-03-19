import tkinter as tk
from tkinter import ttk, messagebox
import psutil

def get_processes():
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def update_process_list():
    for row in tree.get_children():
        tree.delete(row)
    
    processes = get_processes()
    for process in processes:
        tree.insert("", tk.END, values=(process['pid'], process['name'], f"{process['cpu_percent']}%", f"{process['memory_percent']}%"))

def kill_selected_process():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "No process selected!")
        return
    
    pid = tree.item(selected_item)['values'][0]
    try:
        p = psutil.Process(pid)
        p.terminate()
        messagebox.showinfo("Success", f"Successfully terminated process: {pid}")
        update_process_list()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to terminate process: {e}")

def toggle_advice():
    if advice_label.winfo_ismapped():
        advice_label.pack_forget()
        advice_button.config(text="Get Advice")
    else:
        display_advice()
        advice_button.config(text="Close Advice")

def display_advice():
    processes = get_processes()
    high_usage_processes = [p for p in processes if p['cpu_percent'] > 50 or p['memory_percent'] > 50]
    
    if high_usage_processes:
        advice_text = "⚠️ High Resource Usage Detected! Consider closing these: \n"
        for p in high_usage_processes:
            advice_text += f"🔹 {p['name']} (CPU: {p['cpu_percent']}%, Memory: {p['memory_percent']}%)\n"
    else:
        advice_text = "✅ Everything is running fine!"
    
    advice_label.config(text=advice_text)
    advice_label.pack()

# GUI Setup
root = tk.Tk()
root.title("Process Monitor")
root.geometry("600x500")
root.configure(bg='lightyellow')

frame = tk.Frame(root)
frame.pack(pady=10, fill=tk.BOTH, expand=True)

columns = ("PID", "Process Name", "CPU %", "Memory %")
tree = ttk.Treeview(frame, columns=columns, show='headings', height=20)  # Increased height

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=140)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

btn_frame = tk.Frame(root, bg='lightyellow')
btn_frame.pack(pady=10)

kill_button = tk.Button(btn_frame, text="KILL SELECTED PROCESS", font=("Arial", 12, "bold"), command=kill_selected_process, bg='red', fg='white')
kill_button.grid(row=0, column=0, padx=10)

advice_button = tk.Button(btn_frame, text="Get Advice", font=("Arial", 12, "bold"), command=toggle_advice, bg='blue', fg='white')
advice_button.grid(row=0, column=1, padx=10)

advice_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="darkblue", bg="lightyellow", justify="left")

update_process_list()
root.mainloop()