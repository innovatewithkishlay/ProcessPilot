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

if __name__ == '__main__':
    app.run(debug=True)