from semantic_kernel import Kernel
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureTextEmbedding
from semantic_kernel.core_plugins.math_plugin import MathPlugin
from semantic_kernel.core_plugins.text_plugin import TextPlugin
from semantic_kernel.core_plugins.time_plugin import TimePlugin
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
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
    chat_deployment_name = os.getenv("AZURE_CHAT_DEPLOYMENT_NAME")
    embedding_deployment_name = os.getenv("AZURE_EMBEDDING_DEPLOYMENT_NAME")
    logging.debug(f"Chat deployment name: {chat_deployment_name}, Embedding deployment name: {embedding_deployment_name}")
    azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    azure_search_key = os.getenv("AZURE_SEARCH_KEY")
    logging.debug(f"Azure Search endpoint: {azure_search_endpoint}, Azure Search key: {azure_search_key}")

    # Set up the kernel
    logging.debug("Setting up the kernel")
    kernel = Kernel()
    # Assign the service to a variable first, as we'll invoke it later
    chat_completion = AzureChatCompletion(
        service_id="chat",
        deployment_name=chat_deployment_name,
        endpoint=azure_ai_endpoint,
        api_key=azure_ai_key,
    )
    kernel.add_service(chat_completion)

    kernel.add_service(
        AzureTextEmbedding(
            service_id="embedding",
            deployment_name=embedding_deployment_name,
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

    # Set up execution settings to enable function calling
    execution_settings = AzureChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior(
            filters={"excluded_plugins": ["Chat"]}
        )
    )

    # Chat loop
    logging.debug("Starting chat loop")
    while True:

        # Get user input
        user_input = input(f"\n{Fore.GREEN}You: ")
        print(f"{Style.RESET_ALL}")
        
        # Get reply
        chat_history.add_user_message(user_input)
        reply = await chat_completion.get_chat_message_content(
            chat_history=chat_history,
            settings=execution_settings,
            kernel=kernel
        )
        chat_history.add_assistant_message(str(reply))

        print(f"{Fore.YELLOW}Assistant: {reply}{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except EOFError as e:
        print(f"Exiting...{Style.RESET_ALL}")