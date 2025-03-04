import requests, os, urllib.parse, argparse, readline
from bs4 import BeautifulSoup
from llama_cpp import Llama
from datetime import datetime

BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

# Get models from the specified directory
models_dir = os.path.expanduser("~/.local/share/AI-Models")
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

llm = Llama(n_ctx= 8196, model_path=selected_model, verbose=False)

class History:
    def __init__(self):
        self.questions = []

    def add_history(self, question):
        self.question.append({
            'question': question,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

def wrap_input_user(prompt):
    try:
        readline.set_completer(None)
        return input(prompt)
    except EOFError:
        return "quit"    

def main():
    history = History()
    
    while True:
        question = wrap_input_user(f"{GREEN}Enter your question (or 'quit' to exit): {ENDC}")

        
        if question.lower() == 'quit':
            break
            
        # Rest of your code remains the same...
        print(f"{YELLOW}Searching for: {question}{ENDC}")
        search_results = search_web(question)
        
        if not search_results:
            print(f"{RED}No search results found.{ENDC}")
            continue
            
        # Prepare context for LLM
        context = "Based on the following search results, Always answer in 1 word:\n\n"
        for idx, result in enumerate(search_results, 1):
            context += f"Result {idx}:\nTitle: {result['title']}\nSnippet: {result['snippet']}\nSource: {result['url']}\n\n"
        
        context += f"Question: {question}\nAnswer:"
        
        # Generate response using local LLM
        response = llm.create_completion(
            prompt=context,
            max_tokens=2096,
            temperature=0.2,
            stop=["Question:", "\n\n"]
        )
        
        print(f"\n{YELLOW}Answer:{ENDC}")
        print(f"{GREEN}{response['choices'][0]['text'].strip()}{ENDC}")
        print(f"\n{YELLOW}Source:{ENDC}")
        for result in search_results:
            print(f"{BLUE}{result['url']}{ENDC}")
            
        # Save history to file
        with open("search_history.log", "a") as f:
            f.write(f"{question} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")        



if __name__ == "__main__":
    main()
