# urban-enigma
Introducing LangServe - a framework with surprising utility for simple LangChain Runnables

<p align="center">
    <img src="images/service.png">
</p>

This GitHub repository is a companion to the Medium article [How to Deploy (Almost) Any LangChain Runnable in One Line](https://medium.com/mitb-for-all/how-to-deploy-almost-any-langchain-runnable-in-one-line-70e7ec1240d1)

## Setup
This repository uses the [uv package installer](https://docs.astral.sh/uv/pip/packages/). 

To create a virtual environment with the dependencies installed, simply type in your terminal:
```
uv sync
```

Ollama is also needed. Visit [Ollama's Download Documentation](https://ollama.com/download) to install Ollama on your machine.

Once done, run
```
ollama pull llama-guard3
```
