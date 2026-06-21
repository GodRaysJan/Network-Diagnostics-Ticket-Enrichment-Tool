import os
import sys
import socket
import subprocess
import requests
import json
from datetime import datetime
from scapy.all import sniff, IP

# 🔴 REPLACE THIS WITH YOUR ACTUAL DISCORD WEBHOOK URL
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

def check_ping(target="8.8.8.8"):
    """Pings a target IP to check basic layer 3 connectivity."""
    # Handle Windows vs Linux/Mac ping command flags
    param = "-n" if os.name == "nt" else "-c"
    command = ["ping", param, "2", target]
    
    # Run the ping command silently
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return "SUCCESS" if result.returncode == 0 else "FAILED"

def check_dns(target="google.com"):
    """Attempts to resolve a domain name to verify DNS configuration."""
    try:
        socket.gethostbyname(target)
        return "SUCCESS"
    except socket.gaierror:
        return "FAILED"

def sample_network_traffic(duration=5):
    """Sniffs network traffic for a brief window to capture active protocols."""
    captured_protocols = set()
    
    def packet_callback(packet):
        if IP in packet:
            proto = packet[IP].proto
            # Translate common protocol numbers to readable names
            proto_map = {6: "TCP", 17: "UDP", 1: "ICMP"}
            captured_protocols.add(proto_map.get(proto, f"Other ({proto})"))

    print(f"[*] Capturing local network telemetry for {duration} seconds...")
    try:
        # Sniff packets silently
        sniff(prn=packet_callback, timeout=duration, store=False)
    except Exception:
        return ["Capture Failed (Requires Admin Permissions)"]
        
    return list(captured_protocols) if captured_protocols else ["No active local traffic observed"]

def run_diagnostics():
    """Compiles local system data, network results, and formats a JSON ticket."""
    print("[*] Launching Automated IT Support Network Diagnostic Tool...")
    
    # 1. Gather baseline system intelligence
    hostname = socket.gethostname()
    username = os.getlogin() if os.name == "nt" else os.getenv("USER")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Run automated network checks
    internet_status = check_ping()
    dns_status = check_dns()
    observed_traffic = sample_network_traffic(duration=5)
    
    # 3. Create enriched ticket structure
    ticket_payload = {
        "ticket_meta": {
            "title": "🚨 AUTOMATED TRIAGE: Network Disconnect Detected",
            "timestamp": timestamp,
            "priority": "HIGH" if internet_status == "FAILED" else "LOW"
        },
        "user_environment": {
            "hostname": hostname,
            "reported_by": username,
            "os_platform": os.name.upper()
        },
        "diagnostic_results": {
            "gateway_ping_8.8.8.8": internet_status,
            "dns_resolution_google_com": dns_status,
            "active_subnet_protocols": observed_traffic
        }
    }
    
    return ticket_payload

def dispatch_ticket(payload):
    """Formats the payload into a clean Discord embed layout and posts it."""
    # Create a cleanly structured visual layout for the Discord webhook channel
    diag = payload["diagnostic_results"]
    env = payload["user_environment"]
    
    discord_data = {
        "embeds": [{
            "title": payload["ticket_meta"]["title"],
            "color": 15158332 if diag["gateway_ping_8.8.8.8"] == "FAILED" else 3066993,
            "fields": [
                {"name": "👤 User Account", "value": f"**User:** {env['reported_by']}\n**Host:** {env['hostname']}", "inline": True},
                {"name": "⏰ Timestamp", "value": payload["ticket_meta"]["timestamp"], "inline": True},
                {"name": "🌐 Network Triage Results", "value": f"🔴 **Internet Access:** {diag['gateway_ping_8.8.8.8']}\n🔍 **DNS Resolution:** {diag['dns_resolution_google_com']}", "inline": False},
                {"name": "📡 Passive Sniffer Protocol Sample", "value": ", ".join(diag["active_subnet_protocols"]), "inline": False}
            ],
            "footer": {"text": "Tier 1 Automation Engine v1.0"}
        }]
    }

    try:
        response = requests.post(WEBHOOK_URL, json=discord_data)
        if response.status_code in [200, 204]:
            print("[+] Enriched diagnostic ticket successfully pushed to central support channel!")
        else:
            print(f"[!] Failed to push webhook. Server returned code: {response.status_code}")
    except Exception as e:
        print(f"[!] Network error dispatching ticket payload: {e}")

if __name__ == "__main__":
    # Ensure tool runs with appropriate permissions for Scapy sniffing
    if os.name == "posix" and os.geteuid() != 0:
        print("[!] Warning: Script running without root permissions. Packet sampling might fail.")
        
    ticket = run_diagnostics()
    dispatch_ticket(ticket)
