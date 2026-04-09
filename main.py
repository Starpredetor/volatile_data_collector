import psutil
import platform
import socket
from datetime import datetime

def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "release": platform.release(),
        "time": str(datetime.now())
    }

def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append(proc.info)
    return processes

def get_network_connections():
    connections = []
    for conn in psutil.net_connections():
        connections.append({
            "pid": conn.pid,
            "local": str(conn.laddr),
            "remote": str(conn.raddr),
            "status": conn.status
        })
    return connections

def get_logged_in_users():
    users = []
    for user in psutil.users():
        users.append({
            "name": user.name,
            "terminal": user.terminal,
            "host": user.host
        })
    return users

def main():
    print("\n=== Volatile Data Capture ===\n")

    print("System Info:")
    print(get_system_info(), "\n")

    print("Processes:")
    for p in get_processes()[:10]:  # limit for display
        print(p)

    print("\nNetwork Connections:")
    for c in get_network_connections()[:10]:
        print(c)

    print("\nLogged-in Users:")
    for u in get_logged_in_users():
        print(u)

if __name__ == "__main__":
    main()