# Basic Semantic Kernel Copilot

This repo demonstrates basic chat copilot capabilities of Semantic Kernel in Python. The example code includes the following:
- Basic copilot chat loop rendering output to the terminal
- Connecting Azure OpenAI chat and embedding models to the kernel
- Adding built-in Semantic Kernel plugins
- Custom semantic and native plugins
- Custom RAG plugin using Azure AI Search (using keyword search)

For a step-by-step explanation of the code see [Getting started with Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/get-started/quick-start-guide?pivots=programming-language-python).

## Running the Copilot
1. Clone this repo and open it in, e.g., VS Code.
1. Rename [.env.example](.env.example) to ```.env``` and populate it with your keys and endpoints for Azure AI / Azure OpenAI and Azure AI Search.
1. Install the [requirements](requirements.txt) using ```pip install -r requirements.txt```.
1. Customize the [example plugin](src/plugins/Example/example_plugin.py) and [search plugin](src/plugins/Example/example_plugin.py) to enable the kernel to execute custom code.
1. Run the [app.py](src/app.py) to start the copilot. Type your chat input in the terminal.
