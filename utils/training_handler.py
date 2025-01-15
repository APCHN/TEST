import re

def parse_training_file(file_path):
    """
    Đọc file training.txt và phân tích hướng dẫn.
    """
    instructions = {}
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "GoogleDriveFolder:" in line:
                instructions["GoogleDriveFolder"] = line.split(":", 1)[1].strip()
            elif "Task:" in line:
                instructions["Task"] = line.split(":", 1)[1].strip()
    return instructions
