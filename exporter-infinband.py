# Add this to your Prometheus configuration.
#scrape_configs:
#  - job_name: 'infiniband'
#    static_configs:
#      - targets: ['your_server_ip:8000']

import subprocess
import time
from prometheus_client import start_http_server, Gauge

# Define the metrics
RECV_BYTES = Gauge('infiniband_recv_bytes', 'Bytes received over InfiniBand')
RECV_PACKETS = Gauge('infiniband_recv_packets', 'Packets received over InfiniBand')
XMIT_BYTES = Gauge('infiniband_xmit_bytes', 'Bytes transmitted over InfiniBand')
XMIT_PACKETS = Gauge('infiniband_xmit_packets', 'Packets transmitted over InfiniBand')

def get_infiniband_stats():
    try:
        result = subprocess.run(['perfquery'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        stats = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':')
                stats[key.strip()] = int(value.strip())
        return stats
    except Exception as e:
        print(f"Error getting InfiniBand stats: {e}")
        return {}

def update_metrics():
    stats = get_infiniband_stats()
    RECV_BYTES.set(stats.get('PortRcvData', 0))
    RECV_PACKETS.set(stats.get('PortRcvPackets', 0))
    XMIT_BYTES.set(stats.get('PortXmitData', 0))
    XMIT_PACKETS.set(stats.get('PortXmitPackets', 0))

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        update_metrics()
        time.sleep(60)
