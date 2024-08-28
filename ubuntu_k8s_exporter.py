import time
import psutil
import subprocess
from prometheus_client import start_http_server, Gauge

# Create Prometheus metrics
CPU_UTIL = Gauge('cpu_utilization_percent', 'CPU utilization in percent')
MEM_UTIL = Gauge('memory_utilization_percent', 'Memory utilization in percent')
CPU_TEMP = Gauge('cpu_temperature_celsius', 'CPU temperature in Celsius')
GPU_TEMP = Gauge('gpu_temperature_celsius', 'GPU temperature in Celsius')

def get_cpu_temp():
    try:
        temp = psutil.sensors_temperatures()['coretemp'][0].current
        return temp
    except:
        return None

def get_gpu_temp():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], capture_output=True, text=True)
        return float(result.stdout.strip())
    except:
        return None

def collect_metrics():
    # CPU utilization
    CPU_UTIL.set(psutil.cpu_percent())

    # Memory utilization
    mem = psutil.virtual_memory()
    MEM_UTIL.set(mem.percent)

    # CPU temperature
    cpu_temp = get_cpu_temp()
    if cpu_temp is not None:
        CPU_TEMP.set(cpu_temp)

    # GPU temperature
    gpu_temp = get_gpu_temp()
    if gpu_temp is not None:
        GPU_TEMP.set(gpu_temp)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    
    # Generate some requests.
    while True:
        collect_metrics()
        time.sleep(15)
