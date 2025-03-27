# ==================== IMPORTS ====================
import sys
import ctypes
import time
import threading
import psutil
import tkinter as tk
from tkinter import messagebox, font
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from datetime import datetime


#--killing process----
import ctypes, sys
if not ctypes.windll.shell32.IsUserAnAdmin():
    print("Restarting with admin rights...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()
 

# ==================== CONSTANTS ====================
BG_COLOR = '#121212'
SIDEBAR_COLOR = '#1e1e1e'
TEXT_COLOR = 'white'
USER_BUBBLE_COLOR = '#4a8cff'
BOT_BUBBLE_COLOR = '#2d2d2d'
TIMESTAMP_COLOR = '#888888'

# ==================== CHAT MESSAGE CLASS ====================
class ChatMessage(tk.Frame):
    def __init__(self, master, message, is_user=False, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg=BG_COLOR, padx=5, pady=2)
        self.is_user = is_user
        
        # Timestamp
        self.timestamp = tk.Label(
            self, 
            text=datetime.now().strftime("%H:%M"), 
            fg=TIMESTAMP_COLOR, 
            bg=BG_COLOR,
            font=('Helvetica', 7)
        )
        self.timestamp.pack(anchor='ne' if is_user else 'nw')
        
        # Message bubble
        bubble_bg = USER_BUBBLE_COLOR if is_user else BOT_BUBBLE_COLOR
        self.message_bubble = tk.Frame(
            self, 
            bg=bubble_bg,
            padx=12, 
            pady=8,
            highlightthickness=0,
            relief='flat'
        )
        self.message_bubble.pack(
            anchor='e' if is_user else 'w', 
            padx=(20, 5) if is_user else (5, 20),
            fill='x'
        )
        
        # Message text
        self.message_label = tk.Label(
            self.message_bubble, 
            text=message, 
            fg=TEXT_COLOR, 
            bg=bubble_bg,
            wraplength=300,
            justify='left',
            font=('Helvetica', 10)
        )
        self.message_label.pack(anchor='w')

# ==================== CHATBOT FUNCTIONS ====================
def open_chatbot():
    chat_window = tk.Toplevel(root)
    chat_window.title('Task Manager Assistant')
    chat_window.geometry('500x600')
    chat_window.configure(bg=BG_COLOR)
    chat_window.resizable(True, True)
    
    # Header
    header_frame = tk.Frame(chat_window, bg=SIDEBAR_COLOR, height=50)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    header_label = tk.Label(
        header_frame, 
        text="Task Manager Assistant", 
        fg=TEXT_COLOR, 
        bg=SIDEBAR_COLOR,
        font=('Helvetica', 12, 'bold')
    )
    header_label.pack(side='left', padx=15)
    
    # Close button
    close_button = ttk.Button(
        header_frame, 
        text="✕", 
        command=chat_window.destroy,
        bootstyle="light",
        width=2
    )
    close_button.pack(side='right', padx=5)
    
    # Chat display area
    chat_container = tk.Frame(chat_window, bg=BG_COLOR)
    chat_container.pack(fill='both', expand=True, padx=5, pady=5)
    
    # Canvas and scrollbar
    canvas = tk.Canvas(chat_container, bg=BG_COLOR, highlightthickness=0)
    scrollbar = ttk.Scrollbar(
        chat_container, 
        orient='vertical', 
        command=canvas.yview, 
        bootstyle="dark-round"
    )
    scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Mouse wheel scrolling
    def _on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
    
    # Input area
    input_frame = tk.Frame(chat_window, bg=SIDEBAR_COLOR, padx=10, pady=10)
    input_frame.pack(fill='x')
    
    user_input = tk.StringVar()
    input_entry = ttk.Entry(
        input_frame, 
        textvariable=user_input,
        bootstyle="light"
    )
    input_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
    
    send_button = ttk.Button(
        input_frame, 
        text="Send", 
        command=lambda: process_command(scrollable_frame, canvas, user_input),
        bootstyle="primary"
    )
    send_button.pack(side='right')
    
    # Welcome message
    welcome_messages = [
        "Hello! I'm your Task Manager Assistant. How can I help you today?",
        "Hi there! I can help you manage processes. What would you like to do?",
        "Welcome to Task Manager Assistant. Type 'help' to see what I can do."
    ]
    
    add_chat_message(
        scrollable_frame, 
        random.choice(welcome_messages), 
        is_user=False,
        canvas=canvas
    )
    
    # Bind Enter key to send message
    input_entry.bind('<Return>', lambda event: process_command(scrollable_frame, canvas, user_input))
    input_entry.focus_set()

def add_chat_message(frame, message, is_user=False, canvas=None):
    msg = ChatMessage(frame, message, is_user=is_user)
    msg.pack(fill='x', pady=3)
    if canvas:
        canvas.yview_moveto(1.0)

def process_command(frame, canvas, user_input_var):
    command = user_input_var.get().strip()
    if not command:
        return
        
    add_chat_message(frame, command, is_user=True, canvas=canvas)
    user_input_var.set('')
    
    threading.Thread(
        target=handle_chat_command, 
        args=(frame, canvas, command), 
        daemon=True
    ).start()

def handle_chat_command(frame, canvas, command):
    command = command.lower()
    
    if command in ['hi', 'hello', 'hey']:
        response = random.choice([
            "Hello! How can I assist you with your processes today?",
            "Hi there! What would you like to know about your running processes?",
            "Hey! Ready to manage some tasks?"
        ])
    elif "cpu" in command or "usage" in command:
        processes = []
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
            try:
                info = proc.info
                processes.append((info['pid'], info['name'], info['cpu_percent']))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        processes.sort(key=lambda x: x[2], reverse=True)
        response = "Here are the top CPU-consuming processes:\n"
        for p in processes[:5]:
            response += f"• {p[1]} (PID: {p[0]}) - {p[2]:.1f}%\n"
        if not processes:
            response = "Couldn't retrieve CPU usage information."
    elif "memory" in command or "ram" in command:
        processes = []
        for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info']):
            try:
                info = proc.info
                mem_mb = info['memory_info'].rss / (1024 * 1024)
                processes.append((info['pid'], info['name'], mem_mb))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        processes.sort(key=lambda x: x[2], reverse=True)
        response = "Here are the top memory-consuming processes:\n"
        for p in processes[:5]:
            response += f"• {p[1]} (PID: {p[0]}) - {p[2]:.1f} MB\n"
        if not processes:
            response = "Couldn't retrieve memory usage information."
    elif "kill" in command or "stop" in command or "end" in command:
        parts = command.split()
        pid = None
        name = None
        
        for part in parts:
            if part.isdigit():
                pid = int(part)
                break
        
        if pid is None:
            processes, _ = get_processes()
            for proc in processes:
                if proc[0].lower() in command:
                    name = proc[0]
                    pid = proc[1]
                    break
        
        if pid:
            try:
                proc = psutil.Process(pid)
                proc_name = proc.name()
                proc.terminate()
                proc.wait(timeout=3)
                refresh_processes()
                response = f"Successfully terminated process: {proc_name} (PID: {pid})"
            except psutil.NoSuchProcess:
                response = f"Error: Process with PID {pid} not found."
            except psutil.AccessDenied:
                response = f"Error: Permission denied to kill process {pid}. Try running as administrator."
            except Exception as e:
                response = f"Error: {str(e)}"
        else:
            response = "Please specify a process to kill by its name or PID. Example: 'kill chrome' or 'kill 1234'"
    elif "search" in command or "find" in command:
        search_term = command.replace("search", "").replace("find", "").strip()
        if search_term:
            processes, _ = get_processes()
            found = [p for p in processes if search_term.lower() in p[0].lower()]
            if found:
                response = f"Found {len(found)} matching processes:\n"
                for p in found[:5]:
                    response += f"• {p[0]} (PID: {p[1]})\n"
                if len(found) > 5:
                    response += f"...and {len(found)-5} more"
            else:
                response = f"No processes found matching '{search_term}'"
        else:
            response = "Please specify what to search for. Example: 'search chrome'"
    elif "advice" in command or "suggestion" in command:
        high_usage = []
        for child in tree.get_children():
            process_name = tree.item(child)['values'][0]
            cpu_usage = float(tree.item(child)['values'][2])
            mem_usage = float(tree.item(child)['values'][3].split()[0])
            
            if cpu_usage > 50:
                high_usage.append(f"• {process_name} is using {cpu_usage:.1f}% CPU")
            if mem_usage > 500:
                high_usage.append(f"• {process_name} is using {mem_usage:.1f} MB memory")
        
        response = "Here are some processes that might need attention:\n" + "\n".join(high_usage) if high_usage else "Your system looks good!"
    elif "help" in command or "commands" in command:
        response = """Available commands:
- CPU usage: "show cpu usage"
- Memory usage: "show memory"
- Kill process: "kill [name/PID]"
- Search: "search chrome"
- Advice: "give me advice"
- System info: "system status"
Type 'help' anytime for this menu"""
    elif "thank" in command:
        response = random.choice(["You're welcome!", "Happy to help!", "Anytime!"])
    elif "exit" in command or "quit" in command or "bye" in command:
        response = "Goodbye! Feel free to ask if you need more help later."
    else:
        response = random.choice([
            "I'm not sure I understand. Can you rephrase?",
            "Type 'help' to see what I can do",
            "I can help with process management. What do you need?"
        ])
    
    root.after(0, lambda: add_chat_message(frame, response, is_user=False, canvas=canvas))

# ==================== PROCESS MANAGEMENT FUNCTIONS ====================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        messagebox.showinfo("Admin Required", "Restarting with administrator privileges...")
        params = " ".join(f'"{arg}"' for arg in sys.argv) 
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        root.destroy() 
        sys.exit()

def get_processes():
    processes = []
    total_threads = 0
    for proc in psutil.process_iter(attrs=['name', 'pid', 'cpu_percent', 'memory_info', 'io_counters', 'num_threads']):
        try:
            info = proc.info
            mem_mb = info['memory_info'].rss / (1024 * 1024)
            disk_usage = info['io_counters'].write_bytes / (1024 * 1024) if info['io_counters'] else 0
            net_usage = (info['io_counters'].read_bytes * 8) / (1024 * 1024) if info['io_counters'] else 0
            processes.append((info['name'], info['pid'], info['cpu_percent'], f"{mem_mb:.2f} MB", f"{net_usage:.2f} Mbps", f"{disk_usage:.2f} MB/s"))
            total_threads += info['num_threads']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes, total_threads

def refresh_processes():
    search_query = search_var.get().strip().lower()
    if search_query == "search process...":
        search_query = ""
    
    selected_item = tree.selection()
    selected_process = None
    if selected_item:
        selected_process = tree.item(selected_item[0])['values'][0]

    for i in tree.get_children():
        tree.delete(i)

    processes, total_threads = get_processes()

    for process in processes:
        if search_query in process[0].lower():
            item_id = tree.insert('', 'end', values=process)
            if selected_process and process[0] == selected_process:
                tree.selection_set(item_id)

    process_count_label.config(text=f"🟢 Total Processes: {len(processes)}")
    thread_count_label.config(text=f"🧵 Total Threads: {total_threads}")

    root.after(2000, refresh_processes)

def kill_selected():
    selected_item = tree.selection()
    if selected_item:
        name = tree.item(selected_item)['values'][0]
        pid = tree.item(selected_item)['values'][1]
        try:
            killed = False  
            for proc in psutil.process_iter(attrs=['name', 'pid']):
                if proc.info['pid'] == pid:
                    proc.terminate()  
                    proc.wait(timeout=3) 
                    killed = True
                    break
            if killed:
                refresh_processes()  
            else:
                messagebox.showerror("Process Not Killed", f"Could not terminate {name}. It might already be closed.")
        except psutil.NoSuchProcess:
            messagebox.showinfo("Process Not Found", f"Process {name} no longer exists.")
            refresh_processes()
        except psutil.AccessDenied:
            response = messagebox.askyesno("Admin Privileges Required", 
                                           f"Permission denied to kill {name}.\nWould you like to restart with admin privileges?")
            if response:
                run_as_admin()

def toggle_advice():
    if advice_label.winfo_ismapped():
        advice_label.pack_forget()
        advice_button.config(text='Get Advice')
    else:
        show_advice()

def show_advice():
    high_usage_processes = []
    for child in tree.get_children():
        process_name = tree.item(child)['values'][0]
        cpu_usage = float(tree.item(child)['values'][2])
        mem_usage = float(tree.item(child)['values'][3].split()[0])
        disk_usage = float(tree.item(child)['values'][5].split()[0])
        
        if cpu_usage > 50:
            high_usage_processes.append(f'⚠️ {process_name} is using high CPU: {cpu_usage}%')
        if mem_usage > 500:
            high_usage_processes.append(f'🛑 {process_name} is using high memory: {mem_usage} MB')
        if disk_usage > 100:
            high_usage_processes.append(f'📂 {process_name} has high disk usage: {disk_usage} MB/s')
    
    advice_text = "\n".join(high_usage_processes) if high_usage_processes else "✅ Everything is running smoothly!"
    advice_label.config(text=advice_text)
    advice_label.pack(pady=5)
    advice_button.config(text='Close Advice')

def open_system_overview():
    overview_window = tk.Toplevel(root)
    overview_window.title('System Overview')
    overview_window.geometry('400x200')
    overview_window.configure(bg=BG_COLOR)

    tk.Label(overview_window, text='CPU Utilization:', fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)
    cpu_value = tk.Label(overview_window, text='', fg=TEXT_COLOR, bg=BG_COLOR)
    cpu_value.pack()

    tk.Label(overview_window, text='Process Count:', fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)
    process_value = tk.Label(overview_window, text='', fg=TEXT_COLOR, bg=BG_COLOR)
    process_value.pack()

    tk.Label(overview_window, text='Thread Count:', fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)
    thread_value = tk.Label(overview_window, text='', fg=TEXT_COLOR, bg=BG_COLOR)
    thread_value.pack()

    def update_overview():
        cpu_usage = psutil.cpu_percent(interval=1)
        process_count = len(psutil.pids())
        thread_count = sum([p.num_threads() for p in psutil.process_iter()])

        cpu_value.config(text=f'{cpu_usage}%')
        process_value.config(text=f'{process_count}')
        thread_value.config(text=f'{thread_count}')

        overview_window.after(1000, update_overview)
    update_overview()

def open_cpu_graph():
    cpu_window = tk.Toplevel(root)
    cpu_window.title('CPU Utilization')
    cpu_window.geometry('600x400')
    cpu_window.configure(bg=BG_COLOR)

    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
    cpu_data = [0] * 60
    line, = ax.plot(cpu_data, color='lime')
    ax.set_title('CPU Usage (%)', color=TEXT_COLOR)
    ax.set_ylim(0, 100)
    ax.set_xlim(0, 59)
    ax.set_facecolor(BG_COLOR)
    fig.patch.set_facecolor(BG_COLOR)
    ax.tick_params(colors=TEXT_COLOR)
    for spine in ax.spines.values():
        spine.set_color(TEXT_COLOR)

    canvas = FigureCanvasTkAgg(fig, master=cpu_window)
    canvas.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)

    def update_cpu_graph():
        while True:
            usage = psutil.cpu_percent()
            cpu_data.append(usage)
            cpu_data.pop(0)
            line.set_ydata(cpu_data)
            canvas.draw()
            time.sleep(1)
    threading.Thread(target=update_cpu_graph, daemon=True).start()

# ==================== MAIN GUI SETUP ====================
root = ttk.Window(themename='darkly')
root.title('Process Monitor')
root.geometry('1000x750')
root.configure(bg=BG_COLOR)

# Sidebar
sidebar_frame = tk.Frame(root, width=200, bg=SIDEBAR_COLOR)
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

# Sidebar widgets
overview_button = ttk.Button(sidebar_frame, text='System Overview', command=open_system_overview, bootstyle=PRIMARY)
overview_button.pack(pady=20, padx=10, fill=tk.X)

cpu_graph_button = ttk.Button(sidebar_frame, text='CPU Utilization', command=open_cpu_graph, bootstyle=PRIMARY)
cpu_graph_button.pack(pady=10, padx=10, fill=tk.X)

search_var = tk.StringVar(value='Search Process...')
search_entry = ttk.Entry(sidebar_frame, textvariable=search_var)
search_entry.pack(pady=10, padx=10, fill=tk.X)

kill_button = ttk.Button(sidebar_frame, text='Kill Selected Process', command=kill_selected, bootstyle=DANGER)
kill_button.pack(pady=10, padx=10, fill=tk.X)

advice_button = ttk.Button(sidebar_frame, text='Get Advice', command=toggle_advice, bootstyle=SUCCESS)
advice_button.pack(pady=10, padx=10, fill=tk.X)

chatbot_button = ttk.Button(
    sidebar_frame, 
    text='💬 Assistant', 
    command=open_chatbot, 
    bootstyle=("light-outline", "success")
)
chatbot_button.pack(pady=10, padx=10, fill=tk.X)

advice_label = tk.Label(sidebar_frame, text='', bg=SIDEBAR_COLOR, fg=TEXT_COLOR, wraplength=180)

# Process Table
tree_frame = tk.Frame(root, bg=BG_COLOR)
tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

columns = ('Process Name', 'PID', 'CPU Usage %', 'Memory Usage', 'Network Usage', 'Disk Usage')
tree = ttk.Treeview(tree_frame, columns=columns, show='headings', style="darkly.Treeview")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor='center')
tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Status bar
status_frame = tk.Frame(root, bg=BG_COLOR)
status_frame.pack(fill=tk.X, pady=5)

process_count_label = tk.Label(status_frame, text='🟢 Total Processes: 0', bg=BG_COLOR, fg=TEXT_COLOR)
process_count_label.pack(side=tk.LEFT, padx=10)

thread_count_label = tk.Label(status_frame, text='🧵 Total Threads: 0', bg=BG_COLOR, fg=TEXT_COLOR)
thread_count_label.pack(side=tk.LEFT, padx=10)

# Initialize
refresh_processes()
root.mainloop()
