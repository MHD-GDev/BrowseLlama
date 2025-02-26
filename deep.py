import requests
from bs4 import BeautifulSoup
from llama_cpp import Llama
import argparse
import urllib.parse
import os
import textwrap
from duckduckgo_search import DDGS

BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

class EnhancedSearch:
    def __init__(self, model_path, max_pages=3):
        self.llm = Llama(model_path=model_path, verbose=False)
        self.max_pages = max_pages
    
    def deep_search(self, query):
        content = []
        print(f"{YELLOW}Searching and analyzing results...{ENDC}")
        
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query,
                region='wt-wt',
                safesearch='off',
                max_results=self.max_pages * 4
            ))
            
            if results:
                for result in results:
                    try:
                        response = requests.get(result['href'], timeout=5)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        main_text = soup.find_all(['p', 'article', 'section'])
                        text_content = ' '.join([t.get_text() for t in main_text])
                        cleaned_text = ' '.join(textwrap.wrap(text_content))[:150]
                        
                        content.append({
                            'title': result['title'],
                            'text': cleaned_text if cleaned_text else result['body'],
                            'source': result['href']
                        })
                        print(f"{BLUE}Retrieved: {result['title']}{ENDC}")
                    except:
                        content.append({
                            'title': result['title'],
                            'text': result['body'][:150],
                            'source': result['href']
                        })
        return content

    def process_query(self, query):
        search_results = self.deep_search(query)
        
        if not search_results:
            return "No results found", []
        
        context = "Based on key findings:\n\n"
        sources = []
        
        for result in search_results[:3]:
            truncated_text = result['text'][:150] + "..."
            context += f"Source: {result['title'][:50]}...\n"
            context += f"Content: {truncated_text}\n\n"
            sources.append(result['source'])
        
        prompt = f"{context}\nQ: {query}\nA:"
        
        response = self.llm.create_completion(
            prompt=prompt,
            max_tokens=256,
            temperature=0.7,
            stop=["Q:", "\n\n"]
        )
        
        return response['choices'][0]['text'], sources

def main():
    models_dir = os.path.expanduser("~/.local/share/AI-Models")
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]

    print(f"{BLUE}Available models:{ENDC}")
    for idx, model in enumerate(model_files, 1):
        print(f"{BLUE}{idx}. {model}{ENDC}")

    while True:
        try:
            choice = int(input("\nSelect a model number: "))
            if 1 <= choice <= len(model_files):
                selected_model = os.path.join(models_dir, model_files[choice-1])
                break
            print("Please select a valid number")
        except ValueError:
            print("Please enter a number")

    searcher = EnhancedSearch(selected_model)
    
    while True:
        question = input(f"\n{GREEN}Enter your question (or 'quit' to exit): {ENDC}")
        
        if question.lower() == 'quit':
            break
            
        print(f"\n{YELLOW}Performing deep search and analysis...{ENDC}")
        answer, sources = searcher.process_query(question)
        
        print(f"\n{YELLOW}Comprehensive Answer:{ENDC}")
        print(f"{GREEN}{answer.strip()}{ENDC}")
        
        print(f"\n{YELLOW}Sources Used:{ENDC}")
        for source in sources:
            print(f"{BLUE}{source}{ENDC}")

if __name__ == "__main__":
    main()
