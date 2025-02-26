# BrowseLlama
- A simple Python script for your local LLM to search the web for answers.
### Requires
- LLM/s ( You can download from [Hugingface](https://huggingface.co/models) ).
- Python 3.x
- [Llama.cpp](https://github.com/ggml-org/llama.cpp)
### Installation
```
git clone https://github.com/MHD-GDev/BrowseLlama.git
```
Note : For CUDA installation of llama_cpp_python use this command :
```
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python beautifulsoup4 requests duckduckgo-search
```
Otherwise:
```
pip install beautifulsoup4 llama_cpp_python requests duckduckgo-search
```
### Usage
1. Change the directory in online.py to your AI Models directory.
2. ```python online.py```
3. select your model.
4. Ask your question
5. Enjoy the answer :)

### Note:
- You can get more than ```1``` answer by modifiying this code in online.py:
``` python
return results[:1]
```
- You can search more than 4 pages by modifiying this code in deep.py:
```python
max_results = self.max_pages * 10 # Change this
```
