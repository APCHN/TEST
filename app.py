import streamlit as st
from utils.training_handler import parse_training_file
from utils.drive_handler import fetch_files_from_drive, download_file_content
from utils.file_handler import read_file
from utils.gpt_handler import ask_gpt

# Tạo giao diện
st.title("Chatbot Trainer with Google Drive Integration")

# Tải file training.txt
training_file = st.file_uploader("Upload training.txt", type=["txt"])

if training_file:
    with open("training.txt", "wb") as f:
        f.write(training_file.getbuffer())

    # Đọc file training
    instructions = parse_training_file("training.txt")
    folder_url = instructions.get("GoogleDriveFolder")
    task = instructions.get("Task", "No task specified")

    if folder_url:
        st.write(f"Fetching files from: {folder_url}...")
        files = fetch_files_from_drive(folder_url)
        data = []

        for file in files:
            content = download_file_content(file["id"])
            processed_content = read_file(content, file["mimeType"])
            data.append(processed_content)

        full_data = "\n".join(data)

        # Chatbot Interaction
        st.subheader("Chatbot")
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "system", "content": f"This is the training data:\n{full_data}"}]

        # Hiển thị lịch sử hội thoại
        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                st.write(f"**You:** {msg['content']}")
            else:
                st.write(f"**Bot:** {msg['content']}")

        # Nhập câu hỏi
        user_input = st.text_input("Ask your question:", key="user_input")
        if user_input:
            st.session_state["messages"].append({"role": "user", "content": user_input})
            prompt = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state["messages"]])
            bot_response = ask_gpt(prompt)
            st.session_state["messages"].append({"role": "assistant", "content": bot_response})

            st.experimental_rerun()
