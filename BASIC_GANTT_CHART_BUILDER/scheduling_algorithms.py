def fcfs_scheduling(burst_times):
    start_times = [0] * len(burst_times)
    completion_times = [0] * len(burst_times)
    
    for i in range(1, len(burst_times)):
        start_times[i] = start_times[i - 1] + burst_times[i - 1]
        completion_times[i] = start_times[i] + burst_times[i]
    
    return start_times, completion_times
