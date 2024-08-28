# Add this to your Prometheus configuration.
#scrape_configs:
#  - job_name: 'infiniband'
#    static_configs:
#      - targets: ['your_server_ip:8000']

import os
import re
import time
from prometheus_client import start_http_server, Gauge

# Define the metrics
IB_TX_ERRORS = Gauge('infiniband_tx_errors', 'InfiniBand TX errors', ['device'])
IB_RX_ERRORS = Gauge('infiniband_rx_errors', 'InfiniBand RX errors', ['device'])

def get_infiniband_stats():
    ib_devices = {}
    for device in os.listdir('/sys/class/infiniband'):
        with open(f'/sys/class/infiniband/{device}/ports/1/counters/port_rcv_errors', 'r') as f:
            rx_errors = int(f.read().strip())
        with open(f'/sys/class/infiniband/{device}/ports/1/counters/port_xmit_discards', 'r') as f:
            tx_errors = int(f.read().strip())
        ib_devices[device] = {'rx_errors': rx_errors, 'tx_errors': tx_errors}
    return ib_devices

def update_metrics():
    ib_stats = get_infiniband_stats()
    for device, stats in ib_stats.items():
        IB_TX_ERRORS.labels(device=device).set(stats['tx_errors'])
        IB_RX_ERRORS.labels(device=device).set(stats['rx_errors'])

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    
    # Main loop
    while True:
        update_metrics()
        time.sleep(60)  # Update every 60 seconds
