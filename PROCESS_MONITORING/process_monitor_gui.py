import tkinter as tk
from tkinter import ttk, messagebox
import psutil

def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)
    return processes

def update_process_list():
    for row in tree.get_children():
        tree.delete(row)
    
    processes = get_processes()
    high_usage_detected = False
    high_usage_processes = []
    
    for process in processes:
        pid = process['pid']
        name = process['name']
        cpu = process['cpu_percent']
        memory = process['memory_percent']
        
        if cpu > 50 or memory > 50:  # Threshold for high usage
            high_usage_detected = True
            high_usage_processes.append(f"{name} (PID: {pid}) - CPU: {cpu}%, Memory: {memory}%")
        
        tree.insert("", "end", values=(pid, name, f"{cpu:.2f}%", f"{memory:.2f}%"))
    
    if high_usage_detected:
        alert_label.config(text="⚠️ High Resource Usage Detected!", fg="red")
    else:
        alert_label.config(text="✅ Everything is running fine!", fg="green")

def kill_selected_process():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "No process selected!")
        return
    
    pid = tree.item(selected_item, 'values')[0]
    try:
        psutil.Process(int(pid)).terminate()
        update_process_list()
        messagebox.showinfo("Success", f"Process {pid} terminated.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to terminate process: {e}")

def toggle_advice():
    if advice_frame.winfo_ismapped():
        advice_frame.pack_forget()
        advice_button.config(text="Get Advice")
    else:
        show_advice()
        advice_frame.pack(fill='x', padx=10, pady=5)
        advice_button.config(text="Close Advice")

def show_advice():
    processes = get_processes()
    advice_text.set("")
    
    high_usage_advice = []
    for process in processes:
        if process['cpu_percent'] > 50 or process['memory_percent'] > 50:
            high_usage_advice.append(f"Consider closing {process['name']} (PID: {process['pid']}) to free up resources.")
    
    if high_usage_advice:
        advice_text.set("\n".join(high_usage_advice))
    else:
        advice_text.set("No issues detected. Your system is running fine!")

root = tk.Tk()
root.title("Process Monitor")
root.geometry("600x400")
root.configure(bg="#f7e18e")  # Yellow background

frame = tk.Frame(root)
frame.pack(pady=10)

tree = ttk.Treeview(frame, columns=("PID", "Process Name", "CPU %", "Memory %"), show="headings")
for col in ("PID", "Process Name", "CPU %", "Memory %"):
    tree.heading(col, text=col)
    tree.column(col, width=250, anchor="center")

tree.pack(side="left", fill="both", expand=True)
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

alert_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f7e18e")
alert_label.pack(pady=5)

button_frame = tk.Frame(root, bg="#f7e18e")
button_frame.pack(pady=5)

kill_button = tk.Button(button_frame, text="Kill Selected Process", command=kill_selected_process, bg="red", fg="white")
kill_button.pack(side="left", padx=10)

advice_button = tk.Button(button_frame, text="Get Advice", command=toggle_advice, bg="blue", fg="white")
advice_button.pack(side="right", padx=10)

advice_frame = tk.Frame(root, bg="#fff8dc", relief="solid", bd=1)
advice_text = tk.StringVar()
advice_label = tk.Label(advice_frame, textvariable=advice_text, font=("Arial", 10), bg="#fff8dc", wraplength=580, justify="left")
advice_label.pack(pady=5, padx=5)

update_process_list()
root.mainloop()