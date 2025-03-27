import os
import psutil
import wmi
import pythoncom
from flask import Flask, jsonify, request
from flask_cors import CORS
from process_utils import get_processes, kill_process

app = Flask(__name__)
CORS(app)  

@app.route('/api/processes', methods=['GET'])
def fetch_processes():
    processes, total_threads = get_processes()
    return jsonify({'processes': processes, 'total_threads': total_threads})

@app.route('/api/kill', methods=['POST'])
def kill_selected_process():
    data = request.json
    pid = data.get('pid')

    if not pid:
        return jsonify({'error': 'PID is required'}), 400
    result = kill_process(pid)
    return jsonify(result)

@app.route('/api/cpu-details', methods=['GET'])
def get_cpu_details():
    cpu_count = psutil.cpu_count(logical=True)
    physical_cores = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq()
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()

    details = {
        "cpu_count": cpu_count,
        "physical_cores": physical_cores,
        "cpu_frequency": f"{cpu_freq.current:.2f} MHz",
        "cpu_usage": f"{cpu_usage}%",
        "total_memory": f"{memory.total / (1024 ** 3):.2f} GB",
        "available_memory": f"{memory.available / (1024 ** 3):.2f} GB",
        "used_memory": f"{memory.used / (1024 ** 3):.2f} GB",
    }
    return jsonify(details)

@app.route('/api/process-insights', methods=['GET'])
def process_insights():
    insights = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            info = proc.info
            cpu_usage = info['cpu_percent']
            memory_usage = info['memory_info'].rss / (1024 * 1024)

            recommendation = "Normal"
            if cpu_usage > 50:
                recommendation = "High CPU usage. Consider terminating if unnecessary."
            elif memory_usage > 500:
                recommendation = "High memory usage. Check if this process is needed."

            insights.append({
                'pid': info['pid'],
                'name': info['name'],
                'cpu_usage': f"{cpu_usage}%",
                'memory_usage': f"{memory_usage:.2f} MB",
                'recommendation': recommendation
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return jsonify(insights)

@app.route('/ask-ai', methods=['POST'])
def ask_ai():
    try:
        pythoncom.CoInitialize()  
        query = request.json.get('query', '').lower()
        c = wmi.WMI()

        if "slow" in query or "laptop is running slow" in query:
            cpu_load = c.Win32_Processor()[0].LoadPercentage
            os_info = c.Win32_OperatingSystem()[0]
            total_memory = round(int(os_info.TotalVisibleMemorySize) / 1024 / 1024, 2)
            free_memory = round(int(os_info.FreePhysicalMemory) / 1024 / 1024, 2)
            used_memory = total_memory - free_memory

            return jsonify({
                "response": f"Your laptop is running slow. Current CPU usage is {cpu_load}%. "
                            f"Total memory: {total_memory} GB, Used: {used_memory} GB, Free: {free_memory} GB."
            })

        elif "task taking more time" in query or "high usage" in query:
            high_usage_processes = []
            for proc in c.Win32_Process():
                try:
                    cpu_usage = proc.PercentProcessorTime
                    memory_usage = proc.WorkingSetSize / (1024 * 1024)  
                    if cpu_usage > 50 or memory_usage > 500:  
                        high_usage_processes.append({
                            "name": proc.Name,
                            "pid": proc.ProcessId,
                            "cpu_usage": f"{cpu_usage}%",
                            "memory_usage": f"{memory_usage:.2f} MB"
                        })
                except Exception:
                    continue

            if high_usage_processes:
                response = "Here are the tasks with high usage:\n"
                for process in high_usage_processes:
                    response += f"Task: {process['name']}, PID: {process['pid']}, CPU: {process['cpu_usage']}, Memory: {process['memory_usage']}\n"
                return jsonify({"response": response})
            else:
                return jsonify({"response": "No tasks with high usage detected."})

        elif "storage" in query or "disk" in query:
            drives = c.Win32_LogicalDisk(DriveType=3)
            storage_info = []
            for drive in drives:
                storage_info.append(
                    f"Drive {drive.DeviceID}: Total {round(int(drive.Size) / (1024 ** 3), 2)} GB, "
                    f"Free {round(int(drive.FreeSpace) / (1024 ** 3), 2)} GB"
                )
            return jsonify({
                "response": " | ".join(storage_info)
            })

        elif "tasks" in query or "processes" in query:
            processes = c.Win32_Process()
            return jsonify({
                "response": f"There are currently {len(processes)} running tasks."
            })

        elif "cpu" in query or "usage" in query:
            cpu_load = c.Win32_Processor()[0].LoadPercentage
            return jsonify({
                "response": f"The current CPU usage is {cpu_load}%."
            })

        elif "memory" in query or "ram" in query:
            os_info = c.Win32_OperatingSystem()[0]
            total_memory = round(int(os_info.TotalVisibleMemorySize) / 1024 / 1024, 2)
            free_memory = round(int(os_info.FreePhysicalMemory) / 1024 / 1024, 2)
            used_memory = total_memory - free_memory
            return jsonify({
                "response": f"Total memory: {total_memory} GB, Used: {used_memory} GB, Free: {free_memory} GB."
            })

        else:
            return jsonify({
                "response": "I can help with storage, tasks, CPU, or memory-related queries. Please refine your question."
            })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)