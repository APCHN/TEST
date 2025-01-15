import streamlit as st
from utils.gpt_handler import ask_gpt

# Dữ liệu huấn luyện cố định
training_data = """
This is the training data for the chatbot.
The chatbot is trained on the following context:
1. Our mission is to provide excellent customer service.
2. Our core values are Integrity, Innovation, and Teamwork.
3. We operate in multiple countries including USA, UK, and Vietnam.
"""

# Tiêu đề ứng dụng
st.title("Interactive Chatbot")

# Cửa sổ chat
st.subheader("Chat with the bot")

# Lưu lịch sử hội thoại vào session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": training_data}]

# Hiển thị lịch sử hội thoại
chat_container = st.container()
with chat_container:
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Bot:** {msg['content']}")

# Trường nhập văn bản cho người dùng
user_input = st.text_input("Type your message:", placeholder="Ask me anything...")

# Xử lý khi người dùng gửi câu hỏi
if st.button("Send") and user_input.strip():
    # Thêm câu hỏi của người dùng vào lịch sử
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Gửi toàn bộ lịch sử hội thoại đến GPT-3.5
    bot_response = ask_gpt(st.session_state["messages"])

    # Thêm câu trả lời của bot vào lịch sử
    st.session_state["messages"].append({"role": "assistant", "content": bot_response})

    # Làm trống trường nhập liệu
    st.session_state["user_input"] = ""
