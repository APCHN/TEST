import streamlit as st
from utils.training_handler import parse_training_file
from utils.drive_handler import fetch_files_from_drive, download_file_content
from utils.file_handler import read_file
from utils.gpt_handler import ask_gpt

st.title("Chatbot Trainer: Huấn luyện từ file training.txt")

# Tải file training.txt
training_file = st.file_uploader("Tải lên file training.txt", type=["txt"])

if training_file:
    with open("training.txt", "wb") as f:
        f.write(training_file.getbuffer())
    
    # Đọc file training
    st.write("Đang đọc file training...")
    instructions = parse_training_file("training.txt")
    folder_url = instructions.get("GoogleDriveFolder")
    task = instructions.get("Task", "No task specified")

    if folder_url:
        st.write("Đang tải file từ Google Drive folder...")
        files = fetch_files_from_drive(folder_url)
        data = []
        for file in files:
            content = download_file_content(file["id"])
            processed_content = read_file(content, file["mimeType"])
            data.append(processed_content)
        
        st.write("Nhiệm vụ:", task)
        full_data = "\n".join(data)
        st.text_area("Dữ liệu tổng hợp:", full_data, height=300)

        user_input = st.text_input("Nhập câu hỏi:")
        if user_input:
            prompt = f"Task: {task}\n\nData:\n{full_data}\n\nQuestion: {user_input}"
            answer = ask_gpt(prompt)
            st.write("Chatbot trả lời:")
            st.write(answer)
