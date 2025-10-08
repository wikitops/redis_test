#!/usr/bin/env python3
import socket
import subprocess
import os

def diagnose_redis_connection(redis_host, redis_port):
    print("🔍 Diagnosing Redis Connection...")
    
    # 1. Check if we can resolve the hostname
    try:
        ip = socket.gethostbyname(redis_host)
        print(f"✓ DNS Resolution: {redis_host} -> {ip}")
    except socket.gaierror as e:
        print(f"✗ DNS Resolution failed: {e}")
        return
    
    # 2. Check if we can connect to the port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            result = s.connect_ex((redis_host, redis_port))
            if result == 0:
                print(f"✓ Port {redis_port} is open on {redis_host}")
            else:
                print(f"✗ Port {redis_port} is closed on {redis_host} (error: {result})")
    except Exception as e:
        print(f"✗ Connection test failed: {e}")
    
    # 3. Check routing
    try:
        result = subprocess.run(
            ['traceroute', '-m', '5', redis_host],
            capture_output=True, text=True, timeout=10
        )
        print("Traceroute result:")
        print(result.stdout)
    except:
        print("Traceroute not available")
    
    # 4. Check current network configuration
    print("\n Current Network Configuration:")
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
        print(f"Container hostname: {hostname}")
        print(f"Container IP: {local_ip}")
    except:
        print(f"Container hostname: {hostname}")

if __name__ == "__main__":
    redis_host = os.getenv('REDIS_HOST', 'your-redis-ip-here')
    redis_port = os.getenv('REDIS_PORT', '6379')
    diagnose_redis_connection(redis_host, redis_port)