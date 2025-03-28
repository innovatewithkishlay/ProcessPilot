# ProcessPilot

## Overview

**ProcessPilot** is a modern, web-based tool designed to monitor and manage system processes. It provides a user-friendly interface to view running processes, track CPU and memory usage, filter processes via a search bar, terminate selected processes, and gain insights into system performance. Additionally, it includes an AI-powered chatbot for system-related queries and performance advice, a real-time CPU usage graph, and system details displayed at the bottom of the application.

## Features

- **View Running Processes:** Displays a list of currently running processes along with CPU usage, memory usage, and other relevant details.
- **Search Functionality:** Allows users to filter processes by name using a search bar.
- **Terminate Processes:** Enables users to kill a selected process directly from the web interface.
- **Process Insights:** Provides recommendations for processes with high CPU or memory usage.
- **AI Chatbot:** Includes an AI-powered chatbot to answer system-related queries such as CPU usage, memory status, and storage availability.
- **Performance Monitoring:** Offers insights into CPU performance and memory usage in real-time.
- **Dynamic Filtering:** Allows users to filter processes based on high CPU or memory usage.
- **CPU Usage Graph:** Displays a real-time graph of CPU usage to monitor system performance visually.
- **System Details:** Displays key system information (e.g., total memory, available memory, CPU cores) at the bottom of the application.
- **Responsive Design:** The web app is fully responsive and works seamlessly across devices.

## Requirements

### Backend

- Python 3.x
- Required Python Libraries:
  - `Flask` (for the backend server)
  - `Flask-CORS` (to handle cross-origin requests)
  - `psutil` (for process monitoring)
  - `wmi` (for Windows Management Instrumentation)
  - `pythoncom` (for COM initialization in multithreaded environments)

### Frontend

- React.js (for the user interface)
- Tailwind CSS (for styling)

## Installation

### Backend Setup

1. Navigate to the backend directory:
   ```sh
   cd ProcessPilot/backend
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the backend server:
   ```sh
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```sh
   cd ProcessPilot/frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the frontend development server:
   ```sh
   npm start
   ```

## Usage

1. Open the web application in your browser (default: `http://localhost:5174`).
2. Use the sidebar to navigate between features:
   - **All Processes:** View and manage all running processes.
   - **High CPU Usage:** Filter processes consuming high CPU resources.
   - **High Memory Usage:** Filter processes consuming high memory resources.
   - **AI Chat:** Interact with the AI chatbot for system-related queries.
   - **CPU Performance:** Monitor CPU performance in real-time with a graph.
   - **Process Insights:** Get recommendations for processes with high resource usage.
3. Use the search bar to filter processes by name.
4. Select a process and click "Kill Selected Process" to terminate it.
5. Use the AI chatbot to ask questions like:
   - "How much storage is available?"
   - "What is the current CPU usage?"
   - "Which task is consuming the most memory?"
6. View the **CPU Usage Graph** and **System Details** at the bottom of the application for real-time performance monitoring.

## API Endpoints

### Backend API

- **`GET /api/processes`**: Fetches a list of all running processes.
- **`POST /api/kill`**: Terminates a process by its PID.
  - Request Body: `{ "pid": <process_id> }`
- **`GET /api/cpu-details`**: Provides details about CPU performance and memory usage.
- **`GET /api/process-insights`**: Returns insights and recommendations for processes with high resource usage.
- **`POST /ask-ai`**: Handles AI chatbot queries.
  - Request Body: `{ "query": <user_query> }`

## Notes

- The application requires administrator privileges to terminate certain system processes.
- Ensure Python, Node.js, and required dependencies are installed before running the application.
- The backend server runs on `http://localhost:5000` by default, and the frontend runs on `http://localhost:5174`.

## License

This project is open-source and one can update it , also it is available under the MIT License.

## Author

Developed by Kishlay Kumar
