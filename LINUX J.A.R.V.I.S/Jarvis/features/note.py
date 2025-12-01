import os
import subprocess
import datetime

def note(text):
    """Creates and opens a note using Notepad or Notepad++."""
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"

    # Define the note storage directory
    note_dir = "D:\\Main Project\\3\\JARVIS-master\\Notes"
    os.makedirs(note_dir, exist_ok=True)  # Ensure the directory exists

    file_path = os.path.join(note_dir, file_name)

    # Save the note
    with open(file_path, "w") as f:
        f.write(text)

    # Set Notepad++ path (modify if installed elsewhere)
    notepad_plus = r"C:\Program Files (x86)\Notepad++\notepad++.exe"
    
    # Check if Notepad++ exists, else use Windows Notepad
    if os.path.exists(notepad_plus):
        notepad_exe = notepad_plus
    else:
        notepad_exe = r"C:\\Windows\\System32\\notepad.exe"

    try:
        subprocess.Popen([notepad_exe, file_path])  # Open the note
    except Exception as e:
        print(f"Error opening Notepad: {e}")

