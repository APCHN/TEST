import streamlit as st
from utils.training_handler import parse_training_file
from utils.drive_handler import fetch_files_from_drive, download_file_content
from utils.file_handler import read_file
from utils.gpt_handler import ask_gpt

# Tiêu đề ứng dụng
st.title("Interactive Chatbot")

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

        # Cửa sổ chat
        st.subheader("Chatbot Interaction")

        # Lưu lịch sử hội thoại vào session_state
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "system", "content": f"This is the training data:\n{full_data}"}]

        # Hiển thị
