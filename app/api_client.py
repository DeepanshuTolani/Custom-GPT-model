# # app/api_client.py

# # import os
# # from groq import Groq
# # from logger import CustomLogger  # Import your custom logger
# import os
# from dotenv import load_dotenv
# from groq import Groq
# from logger import CustomLogger

# load_dotenv()   # ✅ Load .env file

# class GroqClient:
#     """Class to interact with the Groq API."""

#     def __init__(self):
#        # self.api_key = os.getenv('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')  # Get the actual API key from environment
#         self.api_key = os.getenv("GROQ_API_KEY")
#         self.client = Groq(api_key=self.api_key)
#         self.logger = CustomLogger().get_logger()  # Initialize your custom logger

#     def get_response(self, messages):
#         """
#         Send messages to the Groq API and return the response.

#         :param messages: List of messages for the conversation.
#         :return: AI response as a string.
#         """
#         try:
#             print("DEBUG messages sent to Groq:", messages)   # ADD THIS
#             self.logger.info("Sending messages to Groq API...")
#             chat_completion = self.client.chat.completions.create(
#                 messages=messages,
#                 # model="llama3-8b-8192"
#               # model="mistral-saba-24b"  # Use the appropriate model for general use
#                 # model=llama3-70b-8192
#                 # model="llama-3.1-70b-versatile"
#                 model="llama-3.1-8b-instant"
#             )
#             response = chat_completion.choices[0].message.content
#             self.logger.info("Received response from Groq API.")
#             return response
#         # except Exception as e:
#         #     self.logger.error(f"Error communicating with Groq API: {e}")
#         #     return "Sorry, I couldn't get a response at this time."
#         except Exception as e:
#              print("🔥 GROQ ERROR FULL DETAILS:", repr(e))
#              raise   # re-throw error so we can see it clearly
import os
from dotenv import load_dotenv
from groq import Groq
from logger import CustomLogger

load_dotenv()   # Load .env file

class GroqClient:
    """Class to interact with the Groq API."""

    def __init__(self):
        #self.api_key = os.getenv("GROQ_API_KEY")
        self.api_key = os.getenv("GROQ_API_KEY")
        print("🔥 LOADED FROM ENV:", self.api_key)
        self.client = Groq(api_key=self.api_key)


        # ✅ DEBUG CHECK
        print("✅ API KEY FROM PYTHON:", self.api_key)

        if not self.api_key:
            raise ValueError("❌ GROQ_API_KEY not found in environment!")

        self.client = Groq(api_key=self.api_key)
        self.logger = CustomLogger().get_logger()

    def get_response(self, messages):
        try:
            print("DEBUG messages sent to Groq:", messages)
            self.logger.info("Sending messages to Groq API...")

            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.1-8b-instant"   # ✅ Correct model
            )

            response = chat_completion.choices[0].message.content
            self.logger.info("Received response from Groq API.")
            return response

        except Exception as e:
            print("🔥 GROQ ERROR FULL DETAILS:", repr(e))
            raise
