import os
import logging

logging.basicConfig(level=logging.INFO)

project_name = "MEDICAL_CHATBOT"

list_of_file= [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/logger.py",
    f"src/{project_name}/helper.py",
    f"src/{project_name}/prompt.py",
    ".env",
    "app.py",
    "Dockerfile",
    "setup.py",
    "store_index.py",
    "static",
    "research/trials.ipynb",
    "templates/chat.html",
]

for filepath in list_of_file:
    filedir, filename = os.path.split(filepath)  # Fix: Move this line up
    filepath = os.path.join(filedir, filename)  # Fix: Use the defined variables

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory:{filedir} for the file {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} is already exists")
