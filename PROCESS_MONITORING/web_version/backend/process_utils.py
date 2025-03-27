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
        proc.terminate()
        proc.wait(timeout=3)
        return {'success': True, 'message': f"Process {proc.name()} (PID: {pid}) terminated."}
    except psutil.NoSuchProcess:
        return {'success': False, 'message': f"Process with PID {pid} not found."}
    except psutil.AccessDenied:
        return {'success': False, 'message': f"Permission denied to kill process {pid}."}
    except Exception as e:
        return {'success': False, 'message': str(e)}