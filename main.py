import getpass
import json
import os
import platform
import socket

def detect_os():
    system = platform.system()
    if system == "Windows":
        return "Windows"
    if system == "Linux":
        return "Linux"
    if system == "Darwin":
        return "macOS"
    return "Unknown"

def collect_os_info():
    uname = platform.uname()
    info = {
        "os_family": detect_os(),
        "os_name": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "kernel": uname.release,
        "architecture": platform.machine(),
        "processor": platform.processor() or "unknown",
    }
    try:
        load_avg = os.getloadavg()
    except (OSError, AttributeError):
        load_avg = None

    env_info = {
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn(),
        "current_user": getpass.getuser(),
        "home_dir": os.path.expanduser("~"),
        "cwd": os.getcwd(),
        "cpu_count": os.cpu_count(),
        "load_avg_1_5_15": load_avg,
        "pid": os.getpid(),
        "process_uid": _safe_getuid(),
    }

    net_info = {
        "hostname_resolved_ip": _resolve_hostname(),
    }

    return {
        "os": info,
        "environment": env_info,
        "network": net_info,
    }

def _safe_getuid():
    if hasattr(os, "getuid"):
        try:
            return os.getuid()
        except Exception:
            return None
    return None

def _resolve_hostname():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return None

def save_report(data, output_path = "os_report.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=str)

def main():
    info = collect_os_info()
    save_report(info)
    print(os.path.abspath("os_report.json"))

main()