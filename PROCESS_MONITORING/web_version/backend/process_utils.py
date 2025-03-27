import psutil

def get_processes():
    processes = []
    total_threads = 0
    for proc in psutil.process_iter(attrs=['name', 'pid', 'cpu_percent', 'memory_info']):
        try:
            info = proc.info
            mem_mb = info['memory_info'].rss / (1024 * 1024)
            processes.append({
                'name': info['name'],
                'pid': info['pid'],
                'cpu_percent': info['cpu_percent'],
                'memory_usage': f"{mem_mb:.2f} MB"
            })
            total_threads += proc.num_threads()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes, total_threads

def kill_process(pid):
    try:
        proc = psutil.Process(pid)
        proc_name = proc.name()
        print(f"Attempting to kill process: {proc_name} (PID: {pid})")  # Debugging log
        proc.terminate()
        proc.wait(timeout=3)
        print(f"Successfully killed process: {proc_name} (PID: {pid})")  # Debugging log
        return {'success': True, 'message': f"Successfully killed the process: {proc_name}"}
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} was already terminated or not found.")  # Debugging log
        return {'success': True, 'message': f"The process was already terminated or not found."}
    except psutil.AccessDenied:
        print(f"Permission denied to kill process with PID {pid}.")  # Debugging log
        return {'success': False, 'message': "This process is critical for the system to run and cannot be terminated."}
    except Exception as e:
        print(f"Error while killing process with PID {pid}: {e}")  # Debugging log
        return {'success': False, 'message': str(e)}