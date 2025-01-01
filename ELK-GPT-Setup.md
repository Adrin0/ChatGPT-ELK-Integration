# Project: AI-Driven Threat Intelligence Automation with ELK and GPT Integration (Local Deployment)

## **1. Project Setup Overview**

### **System Requirements:**
- OS: Ubuntu 22.04 / Windows 11 with WSL2
- CPU: 4 Cores
- RAM: 16 GB (minimum)
- Storage: 100 GB (recommended)
- Docker & Docker Compose installed
- Python 3.9+

## **2. Project Directory Structure**
```plaintext
elk-gpt-threat-intel/
├── docker-compose.yml
├── elasticsearch/
│   └── elasticsearch.yml
├── logstash/
│   ├── logstash.conf
│   └── pipelines.yml
├── kibana/
│   └── kibana.yml
├── scripts/
│   ├── threat_enrichment.py
│   ├── gpt_analysis.py
│   ├── automated_playbook.py
├── .env
└── README.md
```

## **3. Docker Compose Configuration**

### **docker-compose.yml**
```yaml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.13.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - xpack.security.enabled=false
    ulimits:
      memlock:
        soft: -1
        hard: -1
    ports:
      - "9200:9200"
    volumes:
      - ./elasticsearch/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml

  kibana:
    image: docker.elastic.co/kibana/kibana:8.13.0
    container_name: kibana
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
    volumes:
      - ./kibana/kibana.yml:/usr/share/kibana/config/kibana.yml

  logstash:
    image: docker.elastic.co/logstash/logstash:8.13.0
    container_name: logstash
    ports:
      - "5044:5044"
      - "9600:9600"
    depends_on:
      - elasticsearch
    volumes:
      - ./logstash/logstash.conf:/usr/share/logstash/pipeline/logstash.conf
      - ./logstash/pipelines.yml:/usr/share/logstash/config/pipelines.yml
```

## **4. Logstash Configuration**

### **logstash.conf**
```plaintext
input {
  beats {
    port => 5044
  }
}

filter {
  if [ip] {
    ruby {
      code => "
        require 'net/http'
        require 'json'
        uri = URI('https://api.abuseipdb.com/api/v2/check')
        req = Net::HTTP::Get.new(uri)
        req['Key'] = 'YOUR_ABUSEIPDB_API_KEY'
        req['Accept'] = 'application/json'
        req.set_form_data('ipAddress' => event.get('ip'))
        res = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) { |http| http.request(req) }
        result = JSON.parse(res.body)
        event.set('threat_info', result['data']['abuseConfidenceScore'])
      "
    }
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "threat-intel-%{+YYYY.MM.dd}"
  }
  stdout { codec => rubydebug }
  exec {
    command => "python3 /path/to/scripts/automated_playbook.py"
  }
}
```

### **pipelines.yml**
```yaml
- pipeline.id: main
  path.config: "/usr/share/logstash/pipeline/logstash.conf"
```

## **5. Python Scripts Workflow Overview**

### **Script Integration in the Workflow:**
1. **Logstash Input:** Logstash processes incoming logs from Beats agents.
2. **Threat Enrichment:** Logs containing IP addresses are passed to `threat_enrichment.py` for enrichment via API calls.
3. **GPT Analysis:** Enriched logs are analyzed by `gpt_analysis.py` to identify patterns and generate insights.
4. **Automated Playbook:** `automated_playbook.py` coordinates the flow between enrichment and analysis, orchestrating the scripts.
5. **Final Output:** Enriched and analyzed logs are sent to Elasticsearch for indexing and displayed in Kibana.

### **Script Triggers:**
- The `automated_playbook.py` script is triggered automatically by Logstash using the `exec` output plugin when logs meet predefined conditions.
- Optionally, it can also be executed manually or scheduled as a cron job.

## **6. Monitoring in Kibana**

### **Dashboard Creation:**
1. **Log into Kibana:** Navigate to `http://localhost:5601`.
2. **Create an Index Pattern:**
   - Go to **Stack Management > Index Patterns**.
   - Create an index pattern: `threat-intel-*`.
3. **Discover Logs:**
   - Navigate to **Discover**.
   - Select the `threat-intel-*` index pattern.
   - Inspect raw logs enriched with `threat_info` and GPT analysis fields.

### **Building Visualizations:**
1. **Threat Confidence Score Chart:**
   - Go to **Visualize Library > Create Visualization > Lens**.
   - Use the `threat_info` field to create bar or pie charts.
2. **GPT Analysis Insights:**
   - Create keyword or tag clouds based on GPT analysis outputs.

### **Custom Dashboard:**
1. Combine visualizations into a dashboard.
2. Add panels for threat scores, GPT analysis summaries, and raw logs.
3. Save and share your dashboard.

## **7. Verification and Testing**
- Run each Python script manually.
- Validate integration logs in Logstash.
- Monitor enriched and analyzed data in Kibana.

## **8. Start Services**
```bash
docker-compose up -d
```

## **9. Next Steps**
- Fine-tune visualizations and filters in Kibana.
- Implement alerts based on threat scores.
- Document incident response workflows.
