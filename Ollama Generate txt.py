import requests
import json
import random
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SUB_DIR = SCRIPT_DIR / "Vault"
SUB_DIR.mkdir(exist_ok=True)
reference_file = SCRIPT_DIR / "prompt.txt"
url = "http://localhost:11434/api/generate" #ollama URL
today = date.today()
date = today.strftime('%B %d, %Y')
filename = SUB_DIR / f"{date}.md"

# Initialize memory
memory_file = SCRIPT_DIR / "memory.json"
memory = []
if memory_file.exists():
    memory = json.load(memory_file)

txt = Path(reference_file).read_text()
models = ('gemma4', 'qwen3.5:latest', 'llava', 'llama3') #Random Model chooser. Placed here are random models I have running in my Ollama instance personally but you can put whatever models you prefer here
selected_item = random.choice(models)
first_prompt = (txt)
data = {
    "model": selected_item,
    "prompt": first_prompt,
}
response = requests.post(url, json=data)
if response.status_code == 200:
    try:
        response_lines = response.text.splitlines()
        full_response = ''.join([line['response'] for line in [json.loads(line) for line in response_lines]])
        # Check if the response is already in memory
        if full_response not in memory:
            memory.append(full_response)
            with open(memory_file, "w", encoding="utf-8") as file:
                json.dump(memory, file, indent=4)
            with open(filename, "w", encoding="utf-8") as file:
                file.write(full_response)
            print(f"Successfully saved unique response to {filename}")
        else:
            print("Duplicate response. Generating new one...")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response") 
else:
    print("Error:", response.status_code)
