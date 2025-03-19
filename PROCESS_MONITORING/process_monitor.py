import psutil

def get_processes():
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process_list.append((proc.info['pid'], proc.info['name'], proc.info['cpu_percent'], proc.info['memory_percent']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return sorted(process_list, key=lambda x: x[2], reverse=True)  # Sort by CPU usage

def kill_process(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False
