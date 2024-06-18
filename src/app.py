from semantic_kernel import Kernel
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureTextEmbedding
from semantic_kernel.core_plugins.math_plugin import MathPlugin
from semantic_kernel.core_plugins.text_plugin import TextPlugin
from semantic_kernel.core_plugins.time_plugin import TimePlugin
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from dotenv import load_dotenv
import os
import asyncio
import logging
from colorama import Fore, Style
from plugins.Search.search_plugin import SearchPlugin
from plugins.Example.example_plugin import ExamplePlugin

async def main():
    logging.basicConfig(level=logging.INFO)
    logging.debug("Starting application")

    # Load the environment variables
    logging.debug("Loading environment variables")
    load_dotenv()
    azure_ai_endpoint = os.getenv("AZURE_AI_ENDPOINT")
    azure_ai_key = os.getenv("AZURE_AI_KEY")
    logging.debug(f"Azure AI endpoint: {azure_ai_endpoint}, Azure AI key: {azure_ai_key}")
    azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    azure_search_key = os.getenv("AZURE_SEARCH_KEY")
    logging.debug(f"Azure Search endpoint: {azure_search_endpoint}, Azure Search key: {azure_search_key}")

    # Set up the kernel
    logging.debug("Setting up the kernel")
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            service_id="gpt-4o",
            deployment_name="gpt-4o",
            endpoint=azure_ai_endpoint,
            api_key=azure_ai_key,
        ),
    )
    kernel.add_service(
        AzureTextEmbedding(
            service_id="text-embedding",
            deployment_name="text-embedding-ada-002",
            endpoint=azure_ai_endpoint,
            api_key=azure_ai_key
        ),
    )

    # Import plugins
    logging.debug("Importing plugins")
    math_plugin = kernel.add_plugin(MathPlugin(), "math")
    text_plugin = kernel.add_plugin(TextPlugin(), "text")
    time_plugin = kernel.add_plugin(TimePlugin(), "time")
    chat_plugin = kernel.add_plugin(
        parent_directory=os.path.join(os.getcwd(), "src/plugins/"),
        plugin_name="chat"
    )
    search_plugin = SearchPlugin(azure_search_endpoint, azure_search_key)
    kernel.add_plugin(search_plugin, "search")
    example_plugin = kernel.add_plugin(ExamplePlugin(), "example")

    # Set up chat history
    chat_history = ChatHistory()
    chat_history.add_system_message("You are a helpful chatbot that can assist with a variety of tasks.")
    chat_history.add_assistant_message("Hello! How can I help you today?")

    # Chat loop
    logging.debug("Starting chat loop")
    while True:

        # Get user input
        user_input = input(f"{Fore.GREEN}You: ")
        print(f"{Style.RESET_ALL}")
        
        # Get reply
        reply = await kernel.invoke(
            function=chat_plugin["Chat"],
            arguments=KernelArguments(
                request=user_input,
                history=chat_history,
                settings=AzureChatPromptExecutionSettings(
                    function_call_behavior=FunctionCallBehavior.EnableFunctions(
                        auto_invoke=True,
                        filters={"excluded_plugins": ["Chat"]}
                    )
                )
            )
        )
        print(f"{Fore.YELLOW}Assistant: {reply}{Style.RESET_ALL}")
        
        # Update chat history
        chat_history.add_user_message(user_input)
        chat_history.add_assistant_message(str(reply))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except EOFError as e:
        print(f"Exiting...{Style.RESET_ALL}")