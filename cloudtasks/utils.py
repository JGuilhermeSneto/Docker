import os
import platform
import socket
import sys
import time

# Record start time for uptime calculation
START_TIME = time.time()

def get_system_info():
    """
    Collects runtime diagnostic information to demonstrate
    containerization, isolation, and cloud environment.
    """
    hostname = socket.gethostname()
    
    # Try resolving internal IP
    try:
        internal_ip = socket.gethostbyname(hostname)
    except Exception:
        internal_ip = "127.0.0.1"

    # Check if running inside a Docker container
    is_docker = (
        os.path.exists('/.dockerenv') or
        os.environ.get('IN_DOCKER', '').lower() in ('true', '1') or
        os.path.exists('/run/.containerenv')
    )

    uptime_seconds = int(time.time() - START_TIME)
    uptime_str = f"{uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m {uptime_seconds % 60}s"

    return {
        "hostname": hostname,
        "internal_ip": internal_ip,
        "is_docker": is_docker,
        "os_name": f"{platform.system()} {platform.release()}",
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "app_env": os.environ.get("APP_ENV", "Desenvolvimento"),
        "container_service": os.environ.get("SERVICE_NAME", "backend-django"),
        "port": os.environ.get("PORT", "8000"),
        "uptime": uptime_str,
    }

