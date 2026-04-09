import psutil
import platform
import socket
from datetime import datetime

# ---------------- SYSTEM INFO ----------------
def get_system_info():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "release": platform.release(),
        "time": str(datetime.now()),
        "uptime_since": str(boot_time)
    }

# ---------------- PROCESSES ----------------
def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'exe']):
        try:
            processes.append(proc.info)
        except:
            continue
    return processes

# ---------------- NETWORK ----------------
def get_network_connections():
    connections = []
    for conn in psutil.net_connections():
        connections.append({
            "pid": conn.pid,
            "type": "TCP" if conn.type == 1 else "UDP",
            "local": str(conn.laddr),
            "remote": str(conn.raddr),
            "status": conn.status
        })
    return connections

# ---------------- USERS ----------------
def get_logged_in_users():
    users = []
    for user in psutil.users():
        users.append({
            "name": user.name,
            "terminal": user.terminal,
            "host": user.host,
            "started": str(datetime.fromtimestamp(user.started))
        })
    return users

# ---------------- OPEN FILES ----------------
def get_open_files():
    files = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            open_files = proc.open_files()
            for f in open_files:
                files.append({
                    "pid": proc.pid,
                    "process": proc.name(),
                    "file": f.path
                })
        except:
            continue
    return files

# ---------------- LISTENING PORTS ----------------
def get_listening_ports():
    ports = []
    for conn in psutil.net_connections():
        if conn.status == 'LISTEN':
            ports.append({
                "pid": conn.pid,
                "port": conn.laddr.port if conn.laddr else None
            })
    return ports

# ---------------- MAIN ----------------
def main():
    print("\n========== VOLATILE DATA CAPTURE ==========\n")

    # System Info
    print("[SYSTEM INFORMATION]")
    print(get_system_info(), "\n")

    # Processes
    print("[RUNNING PROCESSES - TOP 10]")
    for p in get_processes()[:10]:
        print(p)

    # High CPU (basic anomaly hint)
    print("\n[HIGH CPU PROCESSES]")
    for p in get_processes():
        if p.get("cpu_percent", 0) > 10:
            print(p)

    # Network
    print("\n[NETWORK CONNECTIONS - TOP 10]")
    for c in get_network_connections()[:10]:
        print(c)

    # Listening Ports
    print("\n[LISTENING PORTS]")
    for port in get_listening_ports():
        print(port)

    # Users
    print("\n[LOGGED-IN USERS]")
    for u in get_logged_in_users():
        print(u)

    # Open Files
    print("\n[OPEN FILES - TOP 10]")
    for f in get_open_files()[:10]:
        print(f)

if __name__ == "__main__":
    main()