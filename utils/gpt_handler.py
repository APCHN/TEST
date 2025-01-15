import openai
import os
from dotenv import load_dotenv

# Load API key từ file .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(messages, model="gpt-3.5-turbo"):
    """
    Gửi danh sách messages tới GPT-3.5 và nhận phản hồi.
    """
    try:
        # Sử dụng messages thay vì prompt
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        return response['choices'][0]['message']['content']
    except Exception as e:  # Bắt lỗi chung thay vì openai.error.OpenAIError
        return f"Error with OpenAI API: {e}"
