# Cybersecurity Home Lab with Honeypot and ELK Stack

## Project Overview
This project demonstrates the setup of a cybersecurity home lab using VirtualBox. The lab includes:

- **Honeypot VM**: A vulnerable machine used as a target for simulated attacks.
- **ELK Stack VM**: Collects, enriches, and visualizes logs from the honeypot.
- **Threat Intelligence Enrichment**: Logs are enriched using Abuse IPDB.
- **Automated Analysis**: Log analysis is conducted using ChatGPT.
- **Script/Playbook Automation**: Logstash triggers scripts for automated responses.
- **Secure Isolation**: The honeypot is securely isolated to ensure safety.

---

## Features

- **Vulnerable Target**: A simple honeypot to simulate attacks.
- **Log Forwarding**: Filebeat sends honeypot logs to Logstash.
- **Threat Intel Integration**: Enrich logs with Abuse IPDB data.
- **AI Analysis**: Leverage ChatGPT to analyze log patterns.
- **Visualization**: Use Kibana for log visualization.
- **Automated Responses**: Execute scripts based on specific log triggers.

---

## Architecture

1. **Honeypot VM**
   - Runs a vulnerable service or application (e.g., DVWA or Metasploitable).
   - Logs forwarded to ELK Stack via Filebeat.

2. **ELK Stack VM**
   - Elasticsearch: Indexes logs.
   - Logstash: Processes logs, enriches them with Abuse IPDB data, and triggers scripts.
   - Kibana: Visualizes log data and analysis.
   - Hosts Python scripts for:
     - Threat enrichment using Abuse IPDB.
     - Log analysis using ChatGPT.
     - Automated playbook execution.

3. **Automation**
   - Logstash `exec` output plugin triggers response scripts.
   - Responses include actions like blocking malicious IPs.

4. **Secure Setup**
   - Honeypot is isolated using a VirtualBox Host-Only Network and outbound traffic restrictions.

---

## Installation and Setup

### Prerequisites
- VirtualBox installed.
- Minimum of 8 GB RAM and 50 GB disk space.
- Access to Abuse IPDB and OpenAI ChatGPT APIs.

### Step 1: Set Up ELK Stack VM
1. Install Docker and Docker Compose.
2. Use the provided `docker-compose.yml` to deploy Elasticsearch, Logstash, and Kibana.
3. Configure Logstash to query Abuse IPDB and integrate ChatGPT for analysis.
4. Verify ELK stack functionality via Kibana.

### Step 2: Set Up Honeypot VM
1. Install a vulnerable application (e.g., DVWA or Metasploitable).
2. Configure Filebeat to send logs to Logstash.
3. Secure the honeypot using:
   - Host-Only Network.
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

---

## Best Practices
- Regularly update all VMs and dependencies.
- Limit honeypot exposure to your internal network.
- Monitor resource usage and adjust configurations as needed.

---

## License
This project is licensed under the MIT License.

---

## Acknowledgments
- [Abuse IPDB](https://www.abuseipdb.com/)
- [Elastic Stack](https://www.elastic.co/)
- [OpenAI ChatGPT](https://openai.com/)

---

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.
