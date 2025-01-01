import sys
import json
from openai import OpenAI  # Use your preferred GPT integration

# Mock OpenAI initialization
def initialize_openai():
    return OpenAI(api_key="YOUR_API_KEY")  # Replace with your actual OpenAI key

def analyze_data(enriched_data):
    """Sends enriched data to GPT for analysis."""
    openai_client = initialize_openai()
    try:
        # Parse input
        data = json.loads(enriched_data)

        # Generate prompt for GPT analysis
        prompt = (
            f"Analyze the following threat data:\n"
            f"IP: {data.get('ip')}\n"
            f"Threat Info: {data.get('threat_info')}\n"
            f"Message: {data.get('message')}\n\n"
            f"Provide actionable insights and categorize the threat."
        )

        # Call GPT API
        response = openai_client.completions.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=150
        )

        return json.dumps({"analysis": response.choices[0].text.strip()}, indent=4)
    except Exception as e:
        return f"Error in GPT analysis: {str(e)}"

if __name__ == "__main__":
    # Input enriched data as JSON
    input_data = sys.argv[1]
    result = analyze_data(input_data)
    print(result)
