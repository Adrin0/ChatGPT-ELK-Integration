# Cybersecurity Home Lab with Honeypot and ELK Stack

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Installation and Setup](#installation-and-setup)  
   - [Step 1: Set Up ELK Stack VM](#step-1-set-up-elk-stack-vm)  
   - [Step 2: Set Up Honeypot VM](#step-2-set-up-honeypot-vm)  
   - [Step 3: Test and Validate](#step-3-test-and-validate)  

---

## Project Overview

This project demonstrates the setup of a **cybersecurity home lab** using VirtualBox. The lab includes:

- **Honeypot VM:** A vulnerable machine used as a target for simulated attacks.
- **ELK Stack VM:** Collects, enriches, and visualizes logs from the honeypot.
- **Threat Intelligence Enrichment:** Logs are enriched using Abuse IPDB.
- **Automated Analysis:** Log analysis is conducted using ChatGPT.
- **Script/Playbook Automation:** Logstash triggers scripts for automated responses.
- **Secure Isolation:** The honeypot is securely isolated to ensure safety.

![Project Overview Diagram](./img/project-overview.png)

---

## Features

- **Vulnerable Target:** A honeypot to simulate attacks.
- **Log Forwarding:** Filebeat sends honeypot logs to Logstash.
- **Threat Intel Integration:** Logs enriched with Abuse IPDB.
- **AI Analysis:** Log patterns analyzed with ChatGPT.
- **Visualization:** Use Kibana for log dashboards.
- **Automated Responses:** Trigger response scripts based on specific logs.

![Features Screenshot](./img/features-screenshot.png)

---

## Architecture

### 1. Honeypot VM
- Runs a vulnerable application (e.g., DVWA, Metasploitable).
- Logs forwarded to ELK Stack via **Filebeat**.

### 2. ELK Stack VM
- **Elasticsearch:** Stores logs.
- **Logstash:** Processes and enriches logs.
- **Kibana:** Visualizes logs.
- Hosts Python scripts for:
   - **Threat enrichment** with Abuse IPDB.
   - **Log analysis** with ChatGPT.
   - **Automated responses** using scripts.

### 3. Automation
- Logstash triggers Python scripts via the `exec` plugin.
- Automated responses include blocking malicious IPs.

### 4. Security Isolation 
- Honeypot uses a **Host-Only Network**.
- Outbound traffic restricted using `iptables`.

![Architecture Diagram](./img/architecture-diagram.png)

---

## Installation and Setup

### Prerequisites
- **VirtualBox** installed.
- Minimum of **8 GB RAM** and **50 GB disk space**.
- Access to **Abuse IPDB** and **OpenAI APIs**.

---

### Step 1: Set Up ELK Stack VM

1. Clone Repository and Navigate to ELK-GPT Folder:
   ```bash
   git clone https://github.com/adrin0/ChatGPT-ELK-Integration
   cd ChatGPT-ELK-Integration/ELK-GPT

2. Run Setup Script:
    ```bash 
    chmod +x setup.sh
    ./setup.sh

3. Verify functionality:
    ```bash
    docker-compose up -d

- Access:`http://<ELK_VM_IP>:5601`

4. turn off containers 
    ```bash
    docker-compose down

### Step 2: Set Up Honeypot VM
1. 1. Clone Repository and Navigate to ELK-GPT Folder:
   ```bash
   git clone https://github.com/adrin0/ChatGPT-ELK-Integration
   cd ChatGPT-ELK-Integration/DVWA-VulnBox

2. Run Setup Script:
    ```bash 
    chmod +x setup.sh
    ./setup.sh

3. Update DVWA config file:
    ```bash
    cd DVWA/config
    sudo cp config.inc.php.dist config.inc.php
    sudo nano config.inc.php
- Update the database username and password settings:
    ```php
    $_DVWA[ 'db_user' ] = 'root';
    $_DVWA[ 'db_password' ] = 'your_mysql_root_password';

4. Install and Configure MySQL:
    ```bash
    sudo mysql_secure_installation
- Follow the prompts to set a root password and secure your MySQL installation.

5. Enable Apache Modules:
    ```bash
    sudo a2enmod rewrite
    sudo systemctl restart apache2

6. Finalize DVWA setup in Browser:
- Open your web browser and go to `http://<honeypot_ip>/DVWA/setup.php.`

7. Configure filebeat.yml to send beats to Logstash:

8. Secure the honeypot using firewall rules:
    ```bash
    sudo ufw allow from <your-ip-address> to any port 80
- Make sure filebeat has an open port to send beats.
- Outbound traffic restrictions (`iptables`).

### Step 3: Test and Validate
1. Simulate attacks on the honeypot.
2. Confirm logs are enriched with Abuse IPDB data and analyzed by ChatGPT.
3. Visualize logs in Kibana.
4. Verify automated responses are triggered.

---

## Usage
- Use the honeypot to test security tools and techniques.
- Analyze attack patterns and trends.
- Develop and test incident response playbooks.
