import requests
from bs4 import BeautifulSoup
from llama_cpp import Llama
import argparse
import urllib.parse
import os

BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

# Get models from the specified directory
models_dir = os.path.expanduser("Path/to/AI/Models/Directory")
model_files = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]

# Display available models
print(f"{BLUE}Available models:{ENDC}")
for idx, model in enumerate(model_files, 1):
    print(f"{BLUE}{idx}. {model}{ENDC}")

# Get user choice
while True:
    try:
        choice = int(input("\nSelect a model number: "))
        if 1 <= choice <= len(model_files):
            selected_model = os.path.join(models_dir, model_files[choice-1])
            break
        print("Please select a valid number")
    except ValueError:
        print("Please enter a number")

def search_web(query):
    # Encode the search query for URL
    encoded_query = urllib.parse.quote(query)
    
    # Use DuckDuckGo as search engine (more privacy-focused)
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract search results
        results = []
        for result in soup.find_all('div', class_='result'):
            title = result.find('a', class_='result__a')
            snippet = result.find('a', class_='result__snippet')
            link = title['href'] if title else None
            
            if title and snippet and link:
                results.append({
                    'title': title.text.strip(),
                    'snippet': snippet.text.strip(),
                    'url': link
                })
        
        return results[:1]  # edit the number for how many results you want
    except Exception as e:
        print(f"Error searching web: {e}")
        return []

def main():
    # Search the web
    question = input(f"{GREEN}Enter your question: {ENDC} ")
    print(f"{YELLOW}Searching for: {question}{ENDC}")
    search_results = search_web(question)
    
    if not search_results:
        print(f"{RED}No search results found.{ENDC}")
        return

    # Prepare context for LLM
    context = "Based on the following search results, please answer the question:\n\n"
    for idx, result in enumerate(search_results, 1):
        context += f"Result {idx}:\nTitle: {result['title']}\nSnippet: {result['snippet']}\nSource: {result['url']}\n\n"
    
    context += f"Question: {question}\nAnswer:"

    # Initialize LLM with the model
    llm = Llama(model_path=selected_model, verbose=False)
    
    # Generate response using local LLM
    response = llm.create_completion(
        prompt=context,
        max_tokens=512,
        temperature=0.7,
        stop=["Question:", "\n\n"]
    )

    print(f"\n{YELLOW}Answer:{ENDC}")
    print(f"{GREEN}{response['choices'][0]['text'].strip()}{ENDC}")
    print(f"\n{YELLOW}Source:{ENDC}")
    for result in search_results:
        print(f"{BLUE}{result['url']}{ENDC}")

if __name__ == "__main__":
    main()
