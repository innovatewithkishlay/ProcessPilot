import os
import shutil
import psutil
import subprocess
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from process_utils import get_processes, kill_process

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    print("Error: GROQ_API_KEY is not defined in the .env file.")
    exit(1)

app = Flask(__name__)
CORS(app)

# Helper function to execute OS commands
def execute_command(command, args):
    try:
        if command == "move_file":
            src, dest = args
            shutil.move(src, dest)
            return f"File moved from {src} to {dest}."
        elif command == "delete_file":
            file_path = args[0]
            if os.path.exists(file_path):
                os.remove(file_path)
                return f"File {file_path} has been deleted."
            else:
                return f"File {file_path} does not exist."
        elif command == "rename_file":
            src, dest = args
            os.rename(src, dest)
            return f"File renamed from {src} to {dest}."
        elif command == "list_processes":
            processes = [proc.info for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent'])]
            return processes
        elif command == "cpu_usage":
            return f"Current CPU usage is {psutil.cpu_percent(interval=1)}%."
        elif command == "memory_usage":
            memory = psutil.virtual_memory()
            return f"Total memory: {memory.total / (1024 ** 3):.2f} GB, Used: {memory.used / (1024 ** 3):.2f} GB, Free: {memory.available / (1024 ** 3):.2f} GB."
        elif command == "disk_usage":
            disk = psutil.disk_usage('/')
            return f"Total disk space: {disk.total / (1024 ** 3):.2f} GB, Used: {disk.used / (1024 ** 3):.2f} GB, Free: {disk.free / (1024 ** 3):.2f} GB."
        elif command == "open_task_manager":
            subprocess.Popen("taskmgr")
            return "Task Manager opened."
        elif command == "open_file_explorer":
            subprocess.Popen("explorer")
            return "File Explorer opened."
        else:
            return "Unknown command."
    except Exception as e:
        return f"Error executing command: {str(e)}"

# Helper function to detect intent and execute commands
def detect_and_execute_intent(user_input):
    user_input = user_input.lower()

    # File operations
    if "move file" in user_input:
        parts = user_input.split(" to ")
        src = parts[0].replace("move file ", "").strip()
        dest = parts[1].strip()
        return execute_command("move_file", (src, dest))
    elif "delete" in user_input and "file" in user_input:
        file_path = user_input.replace("delete file ", "").strip()
        return execute_command("delete_file", (file_path,))
    elif "rename file" in user_input:
        parts = user_input.split(" to ")
        src = parts[0].replace("rename file ", "").strip()
        dest = parts[1].strip()
        return execute_command("rename_file", (src, dest))

    # System stats
    elif "cpu usage" in user_input:
        return execute_command("cpu_usage", None)
    elif "memory usage" in user_input:
        return execute_command("memory_usage", None)
    elif "disk usage" in user_input:
        return execute_command("disk_usage", None)

    # Process management
    elif "list processes" in user_input or "running processes" in user_input:
        processes = execute_command("list_processes", None)
        return "\n".join([f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%" for proc in processes])

    # Open system tools
    elif "open task manager" in user_input:
        return execute_command("open_task_manager", None)
    elif "open file explorer" in user_input:
        return execute_command("open_file_explorer", None)

    # Default: Use Groq API for general queries
    else:
        return ask_groq(user_input)

# Helper function to query Groq API
def ask_groq(user_message):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": user_message}],
        }
        response = requests.post(GROQ_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP errors

        # Extract the chatbot's response
        return (
            response.json()
            .get("choices", [{}])[0]
            .get("message", {})
            .get("content", "No response from the chatbot.")
        )
    except requests.exceptions.RequestException as e:
        print("Groq API Error:", e)
        return "Sorry, I couldn't fetch a response. Please check your internet connection."

# Flask route for the chatbot
@app.route('/ask-ai', methods=['POST'])
def ask_ai():
    data = request.json
    user_input = data.get("query", "")
    if not user_input:
        return jsonify({"response": "<b>Please provide a valid query.</b>"}), 400

    # Get response from Groq API
    response = ask_groq(user_input)
    formatted_response = f"<b>{response}</b>"  # Make the response bold
    return jsonify({"response": formatted_response})

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

if __name__ == '__main__':
    app.run(debug=True)