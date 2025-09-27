# File Organizer

A simple file organizer built with **Python** and **Tkinter**.  
It allows you to select a source directory and automatically organize files into categories such as documents, images, audio, videos, and more.

---

## Features
- Graphical interface using Tkinter
- Select source and destination directories
- Automatic organization into subfolders:
  - Documents
  - Data files
  - Images
  - Audio
  - Videos
  - Compressed files
  - Executables / installers
  - Others
- Progress bar showing the operation status
- Copy path to clipboard (via **pyperclip**)
- Error handling (missing directory, permission denied, etc.)

---

## Requirements
- pyperclip

Install dependencies with:
```bash
git clone https://github.com/davisocoloski/file-organizer.git
cd file-organizer
pip install -r requirements.txt
