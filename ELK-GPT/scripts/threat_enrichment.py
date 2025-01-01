import sys
import json
import requests

# Replace with your actual API key
API_KEY = "YOUR_ABUSEIPDB_API_KEY"
API_URL = "https://api.abuseipdb.com/api/v2/check"

def enrich_data(log_entry):
    """Enriches log data with threat intelligence."""
    try:
        # Parse log entry
        data = json.loads(log_entry)
        ip_address = data.get("ip")

        if not ip_address:
            raise ValueError("No IP address found in the log entry.")

        # Make API request
        headers = {
            "Key": API_KEY,
            "Accept": "application/json"
        }
        params = {
            "ipAddress": ip_address
        }

        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code == 200:
            result = response.json()
            # Enrich log entry with threat information
            data["threat_info"] = result["data"]["abuseConfidenceScore"]
            return json.dumps(data, indent=4)
        else:
            raise Exception(f"API request failed: {response.text}")
    except Exception as e:
        return f"Error in enrichment: {str(e)}"

if __name__ == "__main__":
    # Input log entry as JSON
    input_log_entry = sys.argv[1]
    enriched_result = enrich_data(input_log_entry)
    print(enriched_result)
