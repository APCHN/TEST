import openai
import os
from dotenv import load_dotenv

# Load API key từ file .env
load_dotenv()
openai.api_key = os.getenv("Osk-proj-eO8j8dGwQTaaf_5k3t5FDIP_1jJx57GNZkO7sfikueTO3V4UvKB-7859mr4K-FsOSaLjnMZ8J5T3BlbkFJvutoUi4o8APZyv-DOizJ-al08BQv-QoxSLz9_vtDlo45sfKvT4qqozXT6FCSfsilzsLwlDgEUA")

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
