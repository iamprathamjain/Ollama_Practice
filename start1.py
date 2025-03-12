import requests
import json

url = "http://localhost:11434/api/generate"  # Fixed the URL format

data = {
    "model": "gemma:2b",
    "prompt": "Tell me about Lauv and his songs",
    "stream": True  # Ensure stream is set to True for streaming response
}

# Send a POST request with JSON data
response = requests.post(url, json=data, stream=True)

# Check the response status
if response.status_code == 200:
    print("Generated Text: ", end="", flush=True)

    # Iterate over the streaming response
    for line in response.iter_lines():
        if line:
            # Decode the line and parse the JSON
            decoded_line = line.decode("utf-8")
            result = json.loads(decoded_line)

            # Get the text from the response
            generated_text = result.get("response", "")

            # Print the generated text
            print(generated_text, end="", flush=True)
else:
    print(f"Error: Received status code {response.status_code}")
