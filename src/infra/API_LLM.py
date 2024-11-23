import google.generativeai as genai
import os
from infra.ToolsFC import FunctionCalling
from infra.sysins import SYS_INS
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
class LLM:
    def __init__(self):
        """
        Initializes the LLM class for using the Gemini model.
        """
        pass

    @staticmethod
    def get_model():
        """
        Returns the initialized Gemini model.

        Returns:
            Model: An instance of the Gemini model.
        """
        return genai.GenerativeModel(tools=FunctionCalling.get_tool(),system_instruction=SYS_INS)
