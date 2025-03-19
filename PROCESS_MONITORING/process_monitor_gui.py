import psutil
import tkinter as tk
from tkinter import ttk

def get_processes():
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info', 'io_counters']):
        try:
            info = proc.info
            mem_mb = info['memory_info'].rss / (1024 * 1024)  # Convert to MB
            disk_usage = info['io_counters'].write_bytes / (1024 * 1024) if info['io_counters'] else 0  # MB/s
            net_usage = (info['io_counters'].read_bytes * 8) / (1024 * 1024) if info['io_counters'] else 0  # Mbps
            processes.append((info['pid'], info['name'], info['cpu_percent'], f"{mem_mb:.2f} MB", f"{net_usage:.2f} Mbps", f"{disk_usage:.2f} MB/s"))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes

def refresh_processes():
    for i in tree.get_children():
        tree.delete(i)
    for process in get_processes():
        tree.insert('', 'end', values=process)
    root.after(2000, refresh_processes)

def kill_selected():
    selected_item = tree.selection()
    if selected_item:
        pid = tree.item(selected_item)['values'][0]
        try:
            proc = psutil.Process(int(pid))
            proc.terminate()
            refresh_processes()
        except psutil.NoSuchProcess:
            pass

def toggle_advice():
    if advice_label.winfo_ismapped():
        advice_label.pack_forget()
        advice_button.config(text='Get Advice')
    else:
        show_advice()

def show_advice():
    high_usage_processes = [(tree.item(child)['values'][1], tree.item(child)['values'][2]) for child in tree.get_children() if float(tree.item(child)['values'][2]) > 50]
    advice_text = ""
    if high_usage_processes:
        advice_text = 'High CPU usage detected! Consider closing:\n' + '\n'.join([f"{name} ({cpu}%)" for name, cpu in high_usage_processes])
    else:
        advice_text = 'Everything is running smoothly!'
    advice_label.config(text=advice_text)
    advice_label.pack()
    advice_button.config(text='Close Advice')

root = tk.Tk()
root.title('Process Monitor')
root.geometry('900x600')
root.configure(bg='yellow')

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

columns = ('PID', 'Process Name', 'CPU %', 'Memory (MB)', 'Network (Mbps)', 'Disk (MB/s)')
tree = ttk.Treeview(frame, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=140)

tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

button_frame = tk.Frame(root, bg='yellow')
button_frame.pack(fill=tk.X)

kill_button = tk.Button(button_frame, text='Kill Selected Process', command=kill_selected, bg='red', fg='white', font=('Arial', 12, 'bold'))
kill_button.pack(side=tk.LEFT, padx=5, pady=5)

advice_button = tk.Button(button_frame, text='Get Advice', command=toggle_advice, bg='blue', fg='white', font=('Arial', 12, 'bold'))
advice_button.pack(side=tk.RIGHT, padx=5, pady=5)

advice_label = tk.Label(root, text='', font=('Arial', 14, 'bold'), fg='green', bg='yellow', justify='left')
advice_label.pack(pady=10)

refresh_processes()
root.mainloop()