This Python script creates a Prometheus exporter that monitors the following metrics:

1. CPU utilization
2. Memory utilization
3. CPU temperature
4. GPU temperature

Here's a breakdown of the script:

1. We import the necessary libraries: time, psutil for system information, subprocess for running shell commands, and prometheus_client for creating Prometheus metrics.
2. We define Gauge metrics for each of the values we want to monitor.
3. The get_cpu_temp() function retrieves the CPU temperature using psutil.
4. The get_gpu_temp() function uses the nvidia-smi command to get the GPU temperature. This assumes you have an NVIDIA GPU and the NVIDIA drivers installed.
5. The collect_metrics() function gathers all the metrics and updates the Gauge values.
6. In the main loop, we start the HTTP server on port 8000 and continuously collect metrics every 15 seconds.

   To use this exporter:

1. Install the required Python packages:
   ```pip install psutil prometheus_client```
2. Run the script:
   ```python ubuntu_k8s_exporter.py```
3. The metrics will be available at ```http://your_server_ip:8000```
4. Configure Prometheus to scrape these metrics by adding the following to your Prometheus configuration:
   ```
   scrape_configs:
    - job_name: 'ubuntu_k8s'
      static_configs:
        - targets: ['your_server_ip:8000']
  ```
