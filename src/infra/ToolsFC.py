import google.generativeai as genai

class FunctionCalling:
    """
    A class to define function calling tools for Google Generative AI.

    This class includes methods to retrieve weather information and perform internal database queries 
    related to travel information.
    """

    def __init__(self):
        """
        Initializes the FunctionCalling class.
        """
        pass

    @staticmethod
    def get_tool() -> list:
        """
        Defines and returns tools for retrieving current weather information and querying internal travel information.

        Returns:
            list: A list of Tool objects, each containing a function declaration.
        """

        return [
            genai.protos.Tool(
                function_declarations=[
                    genai.protos.FunctionDeclaration(
                        name="get_weather",
                        description="Retrieve current weather information for a speciied city",
                        parameters=genai.protos.Schema(
                            type=genai.protos.Type.OBJECT,
                            properties={
                                "city": genai.protos.Schema(type=genai.protos.Type.STRING, description="Name of the city")
                            },
                            required=["city"]
                        )
                    )
                ]
            ),
            genai.protos.Tool(
                function_declarations=[
                    genai.protos.FunctionDeclaration(
                        name="RAG_before",
                        description="Provides documents/references related to the information you are searching for about Travelling",
                        parameters=genai.protos.Schema(
                            type=genai.protos.Type.OBJECT,
                            properties={
                                "info": genai.protos.Schema(
                                    type=genai.protos.Type.STRING,
                                    description="The information/field of Travelling'"
                                )
                            },
                            required=["info"]
                        )
                    )
                ]
            )
        ]
