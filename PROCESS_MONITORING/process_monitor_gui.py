import psutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def get_processes():
    processes = []
    for proc in psutil.process_iter(attrs=['name', 'cpu_percent', 'memory_info', 'io_counters']):
        try:
            info = proc.info
            mem_mb = info['memory_info'].rss / (1024 * 1024)  # Convert to MB
            disk_usage = info['io_counters'].write_bytes / (1024 * 1024) if info['io_counters'] else 0  # MB/s
            net_usage = (info['io_counters'].read_bytes * 8) / (1024 * 1024) if info['io_counters'] else 0  # Mbps
            processes.append((info['name'], info['cpu_percent'], f"{mem_mb:.2f} MB", f"{net_usage:.2f} Mbps", f"{disk_usage:.2f} MB/s"))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes

def refresh_processes():
    search_query = search_var.get().strip().lower()
    if search_query == "search process...":
        search_query = ""
    
    for i in tree.get_children():
        tree.delete(i)
    for process in get_processes():
        if search_query in process[0].lower():
            tree.insert('', 'end', values=process)
    root.after(2000, refresh_processes)

def kill_selected():
    selected_item = tree.selection()
    if selected_item:
        name = tree.item(selected_item)['values'][0]
        try:
            for proc in psutil.process_iter(attrs=['name']):
                if proc.info['name'] == name:
                    proc.terminate()
                    break
            refresh_processes()
        except psutil.NoSuchProcess:
            pass

def toggle_advice():
    if advice_label.winfo_ismapped():
        advice_label.pack_forget()
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        advice_button.config(text='Get Advice')
    else:
        show_advice()

def show_advice():
    high_usage_processes = []
    for child in tree.get_children():
        process_name = tree.item(child)['values'][0]
        cpu_usage = float(tree.item(child)['values'][1])
        mem_usage = float(tree.item(child)['values'][2].split()[0])
        disk_usage = float(tree.item(child)['values'][4].split()[0])
        
        if cpu_usage > 50:
            high_usage_processes.append(f'⚠️ {process_name} is using high CPU: {cpu_usage}%')
        if mem_usage > 500:
            high_usage_processes.append(f'🛑 {process_name} is using high memory: {mem_usage} MB')
        if disk_usage > 100:
            high_usage_processes.append(f'📂 {process_name} has high disk usage: {disk_usage} MB/s')
    
    advice_text = "\n".join(high_usage_processes) if high_usage_processes else "✅ Everything is running smoothly!"
    advice_label.config(text=advice_text)
    advice_label.pack(pady=5)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    advice_button.config(text='Close Advice')

root = tk.Tk()
root.title('Process Monitor')
root.geometry('800x600')

# Search Bar
search_frame = tk.Frame(root)
search_frame.pack(fill=tk.X, padx=5, pady=5)
search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, font=('Arial', 12))
search_entry.insert(0, "Search process...")

def clear_placeholder(event):
    if search_entry.get() == "Search process...":
        search_entry.delete(0, tk.END)

def add_placeholder(event):
    if not search_entry.get().strip():
        search_entry.insert(0, "Search process...")

search_entry.bind("<FocusIn>", clear_placeholder)
search_entry.bind("<FocusOut>", add_placeholder)
search_entry.pack(fill=tk.X, padx=5, pady=5)

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

columns = ('Process Name', 'CPU %', 'Memory (MB)', 'Network (Mbps)', 'Disk (MB/s)')
tree = ttk.Treeview(frame, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

kill_button = tk.Button(button_frame, text='Kill Selected Process', command=kill_selected, bg='red', fg='white', font=('Arial', 12, 'bold'))
kill_button.pack(side=tk.LEFT, padx=5, pady=5)

advice_button = tk.Button(button_frame, text='Get Advice', command=toggle_advice, bg='blue', fg='white', font=('Arial', 12, 'bold'))
advice_button.pack(side=tk.RIGHT, padx=5, pady=5)

advice_label = tk.Label(root, text='', font=('Arial', 14, 'bold'), fg='green')
advice_label.pack(pady=5)
advice_label.pack_forget()

refresh_processes()
root.mainloop()