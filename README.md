# Network-Diagnostics-Ticket-Enrichment-Tool
A lightweight, automated Tier 1 network troubleshooting script written in Python. This tool minimizes the gap between users and support teams by replacing vague "my internet is down" complaints with rich, actionable technical telemetry pushed directly to a centralized support channel.
📋 Project Overview

When a user loses connectivity, valuable time is lost trying to gather basic diagnostics. This tool automates that collection loop by:
1. Verifying Layer 3 gateway routing via ICMP ping checks.
2. Validating domain name configurations via asynchronous DNS lookup.
3. Checking local interface card (NIC) operations by capturing a raw traffic sample.
4. Structuring findings into a standardized JSON schema and dispatching it to a ticketing tracking channel via webhook.

---

## 🛠️ Features & Technical Stack

- **Automated Network Core:** `socket`, `subprocess`
- **Packet Sniffing Engine:** `Scapy` (Layer 2/3 protocol sampling)
- **API Integration:** `requests` (Webhook dispatch)
- **Data Serialization:** Standardized `JSON` schema
- **Cross-Platform:** Built-in adjustments for Windows (`nt`) and Linux/macOS (`posix`) environments.

---

## 🚀 Getting Started

### 1. Prerequisites
Python 3.x must be installed on the host system.

### 2. Dependencies
Install the required packages using pip:
```bash
pip install scapy requests`
```
Note: Because Scapy interacts with the network adapter to sniff traffic, the script must be run with administrative/root privileges.
3. Setup Ingestion Channel (Webhook)
   
Open your tracking channel (e.g., Discord or Slack).
   
Go to Channel Settings -> Integrations -> Webhooks and create a new webhook.
   
Copy the Webhook URL.
    
Open triage_tool.py and paste your URL into the global variable:

Python ```WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"```

💻 Usage

On Windows

Open PowerShell or Command Prompt as Administrator and execute:

PowerShell```python triage_tool.py```

On Linux / macOS

Open your terminal and execute:

Bash```sudo python3 triage_tool.py```

📊 Automated Payload Output

When executed, the script bundles local metrics into an immutable JSON payload that maps directly into your tracking integration.

Sample JSON Triage Event:
```{
  "ticket_meta": {
    "title": "🚨 AUTOMATED TRIAGE: Network Disconnect Detected",
    "timestamp": "2026-06-21 15:30:45",
    "priority": "HIGH"
  },
  "user_environment": {
    "hostname": "ENG-WORKSTATION01",
    "reported_by": "tayyab_jan",
    "os_platform": "NT"
  },
  "diagnostic_results": {
    "gateway_ping_8.8.8.8": "FAILED",
    "dns_resolution_google_com": "FAILED",
    "active_subnet_protocols": ["UDP", "TCP"]
  }
}
```

Ingestion Interface View (Mock UI Alert):

Healthy Network State: Triggers a green notification flag summarizing stable infrastructure baselines.

Outage Network State: Triggers a high-priority red alert tracking exact failures, shifting Mean Time to Resolution (MTTR) down dramatically.

🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to expand the tool (e.g., adding automated trace-routing or local DHCP lease extraction).
