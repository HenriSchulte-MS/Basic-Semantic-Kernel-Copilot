from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function

class ExamplePlugin:

    @kernel_function(
        description="",
        name=""
    )
    def example_function(self, query: Annotated[str, ""]) -> Annotated[str, ""]:
        return ""