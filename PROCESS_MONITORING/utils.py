import psutil

def get_high_usage_processes():
    """Returns a list of processes consuming high CPU or Memory."""
    high_usage_processes = []
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            cpu_usage = process.info['cpu_percent']
            mem_usage = process.info['memory_percent']
            if cpu_usage > 10 or mem_usage > 10:  # Threshold for high usage
                high_usage_processes.append(f"⚠️ {process.info['name']} (PID: {process.info['pid']}) - CPU: {cpu_usage}%, MEM: {mem_usage}%")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return high_usage_processes

def advisory_message():
    """Generates a system advisory based on process usage."""
    high_usage = get_high_usage_processes()
    if high_usage:
        return "\n".join(high_usage)
    else:
        return "✅ All processes are running optimally!"
