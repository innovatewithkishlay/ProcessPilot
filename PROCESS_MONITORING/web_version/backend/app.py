import os
import psutil
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
            memory_usage = info['memory_info'].rss / (1024 * 1024)  # Convert to MB

            # AI-driven recommendations
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

if __name__ == '__main__':
    app.run(debug=True)