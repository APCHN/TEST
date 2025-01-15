import streamlit as st
from utils.gpt_handler import ask_gpt

# Dữ liệu huấn luyện được gán cố định trong mã nguồn
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

# Lưu lịch sử hội thoại
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": training_data}]

# Hiển thị lịch sử hội thoại
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Bot:** {msg['content']}")

# Nhập câu hỏi từ người dùng
user_input = st.text_input("Type your message:", placeholder="Ask me anything...")

if st.button("Send"):
    if user_input:
        # Thêm câu hỏi của người dùng vào lịch sử
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Tạo prompt cho GPT-3.5
        prompt = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state["messages"]])
        bot_response = ask_gpt(prompt)

        # Thêm câu trả lời của bot vào lịch sử
        st.session_state["messages"].append({"role": "assistant", "content": bot_response})

        # Làm mới giao diện để hiển thị lịch sử mới
        st.experimental_rerun()
