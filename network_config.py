# backend/network_config.py
# Simple network configuration (simulation)
# You can change region weights, which server to route to, etc.

NETWORK = {
    "regions": {
        "asia": {"host": "127.0.0.1", "port": 5001},
        "europe": {"host": "127.0.0.1", "port": 5002},
        "us": {"host": "127.0.0.1", "port": 5003}
    },
    "routing_policy": "round_robin"  # or "region_preference"
}
