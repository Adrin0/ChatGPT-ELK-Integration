import subprocess
import sys

def run_script(script_name, input_data):
    """Runs a script with input data."""
    try:
        result = subprocess.run(
            [sys.executable, script_name, input_data],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e.stderr}")
        return None

if __name__ == "__main__":
    # Example input from Logstash
    log_entry = '{"ip": "8.8.8.8", "message": "Potential suspicious activity detected"}'

    print("Starting Threat Enrichment...")
    enriched_data = run_script("threat_enrichment.py", log_entry)

    if enriched_data:
        print("Threat Enrichment Complete.")
        print("Starting GPT Analysis...")
        gpt_analysis_result = run_script("gpt_analysis.py", enriched_data)

        if gpt_analysis_result:
            print("GPT Analysis Complete.")
            print("Final Processed Data:")
            print(gpt_analysis_result)
        else:
            print("GPT Analysis Failed.")
    else:
        print("Threat Enrichment Failed.")
