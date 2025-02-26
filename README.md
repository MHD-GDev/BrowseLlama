# BrowseLlama
- A simple Python script for your local LLM to search the web for answers.
### Requires
- LLM/s ( You can download from [Hugingface](https://huggingface.co/models) ).
- Python 3.x
- [Llama.cpp](https://github.com/ggml-org/llama.cpp)
### Installation
Note : For CUDA installation of llama_cpp_python use this command :
```
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python beautifulsoup4 requests
```
Otherwise:
```
pip install beautifulsoup4 llama_cpp_python requests
```
### Usage
1. Change the directory in online.py to your AI Models directory.
2. ```python online.py```
3. select your model.
4. Ask your question
5. Enjoy the answer :)

### Note:
You can get more than ```1``` answer by modifiying :
``` python
return results[:1]
```
