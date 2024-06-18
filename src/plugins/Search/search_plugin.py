from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function

class SearchPlugin:

    def __init__(self, search_endpoint: str, search_key: str):

        # Create Cognitive Search client
        self.search_client = SearchClient(
            endpoint=search_endpoint,
            index_name='<index-name>',
            credential=AzureKeyCredential(search_key)
        )

    
    @kernel_function(
        description="",
        name=""
    )
    def get_search_results(self, query: Annotated[str, "The search query"]) -> Annotated[str, "The search results"]:
        # Get search client
        search_client = self.search_client

        # Search the index
        results = search_client.search(search_text=query, top=1)

        top_result = next(results, None)
        if top_result:
            return str(top_result)
        else:
            raise Exception(f"Search for {query} did not return any results.")
