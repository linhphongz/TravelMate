from infra.API_LLM import LLM
from infra.API_Weather import API_Weather
import json
import google.generativeai as genai
from domain.PDFVectorDatabase import PDFVectorDatabase
class LLMProcessor:
    """
    A class to process interactions with a Large Language Model (LLM) 
    along with weather API and function calling utilities.

    Attributes:
        model: An instance of the LLM class.
        weather_api: An instance of the API_Weather class.
        tools: A tool for function calling.
        system_instruction: A string containing system instructions for the model.
    """

    def __init__(self):
        """
        Initializes the LLMProcessor with instances of required components.
        """
        self.model = LLM.get_model()
        self.weather_api = API_Weather()
        self.chat = self.model.start_chat()
        self.db = PDFVectorDatabase()

    def __set_system_instruction(self):
        """
        Sets the model's system instruction.

        This method assigns the system instruction to the model's 
        system instruction attribute.

        Returns:
            An instance of the model with updated system instructions.
        """
        self.model._system_instruction = self.system_instruction
        self.model._tools = self.tools
        return self.model

    def execute_question(self, question):
        """
        Executes a function call if function calling is activated.

        Parameters:
            question: The user's question.

        Returns:
            The result of the function call if executed, otherwise None.
        """
        result = self.chat.send_message(question)
        print(result)
        if self.__is_function_call(result):
            return self.__handle_function_call(result)
        return result

    def __is_function_call(self, result):
        """
        Checks if the result contains a function call.

        Parameters:
            result: The result object containing candidates.

        Returns:
            bool: True if a function call is present, False otherwise.
        """
        return 'function_call' in result.candidates[0].content.parts[0]

    def __handle_function_call(self, result):
        """
        Handles the function call from the result.

        Parameters:
            result: The result object containing candidates.

        Returns:
            dict: The response from the function call if executed.
        """
        fc = result.candidates[0].content.parts[0].function_call
        converted_format = json.dumps(type(fc).to_dict(fc), indent=4)
        parsed_data = json.loads(converted_format)

        function_name = parsed_data["name"]
        function_args = parsed_data["args"]
        print(parsed_data)
        if function_name == "get_weather":
            city_value = function_args.get('city')
            response_from_api = self.weather_api.get_weather_data(city_value)
            response = self.chat.send_message(
                genai.protos.Content(
                    parts=[
                        genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=function_name,
                                response=response_from_api
                            )
                        )
                    ]
                )
            )
            return response
        if function_name == "RAG_before":
            print(function_args)
            query_question = function_args['info']
            R_reponse = self.db.search(query=query_question)
            response = self.chat.send_message(
                genai.protos.Content(
                    parts=[
                        genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=function_name,
                                response={'response':R_reponse}
                            )
                        )
                    ]
                )
            )
            return response
