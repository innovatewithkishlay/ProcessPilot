import psutil
from utils import advisory_message

def list_processes():
    """Lists all running processes."""
    print("\n🔍 Fetching running processes...\n")
    print(f"{'PID':<10}{'Process Name':<25}{'CPU%':<10}{'Memory%':<10}")
    print("="*50)

    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            print(f"{process.info['pid']:<10}{process.info['name']:<25}{process.info['cpu_percent']:<10}{process.info['memory_percent']:<10}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def kill_process(pid):
    """Terminates a process by PID."""
    try:
        process = psutil.Process(pid)
        process.terminate()
        print(f"✅ Process {pid} terminated successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    list_processes()
    print("\n📢 Advisory Message:")
    print(advisory_message())

    user_choice = input("\nEnter PID to terminate (or press Enter to skip): ")
    if user_choice.isdigit():
        kill_process(int(user_choice))
    else:
        print("✅ No process terminated. Exiting...")
