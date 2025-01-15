import streamlit as st
from utils.training_handler import parse_training_file
from utils.drive_handler import fetch_files_from_drive, download_file_content
from utils.file_handler import read_file
from utils.gpt_handler import ask_gpt

# Tạo tiêu đề ứng dụng
st.title("Chatbot Trainer with Google Drive Integration")

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
    
    # Kiểm tra nếu có folder Google Drive
    if folder_url:
        st.write(f"Fetching files from: {folder_url}...")
        files = fetch_files_from_drive(folder_url)
        data = []

        # Tải nội dung từ Google Drive
        for file in files:
            content = download_file_content(file["id"])
            processed_content = read_file(content, file["mimeType"])
            data.append(processed_content)

        # Kết hợp tất cả dữ liệu thành một văn bản
        full_data = "\n".join(data)
        st.write("Data successfully loaded!")

        # Tạo cửa sổ chat
        st.subheader("Chatbot Interaction")

        # Lưu lịch sử hội thoại trong session state
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "system", "content": f"This is the training data:\n{full_data}"}]

        # Hiển thị lịch sử hội thoại
        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                st.write(f"**You:** {msg['content']}")
            else:
                st.write(f"**Bot:** {msg['content']}")

        # Nhập câu hỏi của người dùng
        user_input = st.text_input("Ask a question:", key="user_input")
        if user_input:
            # Ghi lại câu hỏi vào lịch sử
            st.session_state["messages"].append({"role": "user", "content": user_input})
            
            # Tạo prompt cho GPT-3.5
            prompt = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state["messages"]])
            bot_response = ask_gpt(prompt)

            # Ghi lại câu trả lời của bot
            st.session_state["messages"].append({"role": "assistant", "content": bot_response})
            
            # Làm mới giao diện để hiển thị lịch sử mới
            st.experimental_rerun()
