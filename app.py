import streamlit as st
from utils.training_handler import parse_training_file
from utils.drive_handler import fetch_files_from_drive, download_file_content
from utils.file_handler import read_file
from utils.gpt_handler import ask_gpt

# Tạo tiêu đề ứng dụng
st.title("Interactive Chatbot Trainer")

# Tải file training.txt
training_file = st.file_uploader("Upload training.txt", type=["txt"])

if training_file:
    # Lưu file training.txt tạm thời
    with open("training.txt", "wb") as f:
        f.write(training_file.getbuffer())

    # Đọc file training.txt
    instructions = parse_training_file("training.txt")
    folder_url = instructions.get("GoogleDriveFolder")
    task = instructions.get("Task", "No task specified")

    # Tải dữ liệu từ Google Drive
    if folder_url:
        st.write(f"Fetching files from: {folder_url}...")
        files = fetch_files_from_drive(folder_url)
        data = []
        for file in files:
            content = download_file_content(file["id"])
            processed_content = read_file(content, file["mimeType"])
            data.append(processed_content)

        # Kết hợp dữ liệu từ các file thành một văn bản
        full_data = "\n".join(data)
        st.success("Training data successfully loaded!")

        # Chatbot Section
        st.subheader("Chatbot Interaction")

        # Lưu lịch sử hội thoại
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "system", "content": f"This is the training data:\n{full_data}"}]

        # Hiển thị lịch sử chat
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state["messages"]:
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                elif msg["role"] == "assistant":
                    st.markdown(f"**Bot:** {msg['content']}")

        # Trường nhập văn bản
        user_input = st.text_input("Type your message:", placeholder="Ask me anything...", key="user_input")

        # Nút gửi
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
