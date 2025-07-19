import streamlit as st
import os
import shutil
import zipfile
from datetime import datetime

# --- Modular File & Folder Management Functions ---
def view_directory_contents(path):
    try:
        return os.listdir(path)
    except Exception as e:
        return str(e)

def create_file_folder(path, is_folder):
    try:
        if is_folder:
            os.makedirs(path, exist_ok=True)
        else:
            with open(path, 'w') as f:
                pass
        return f"{'Folder' if is_folder else 'File'} created: {path}"
    except Exception as e:
        return str(e)

def delete_file_folder(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return f"Deleted: {path}"
    except Exception as e:
        return str(e)

def rename_file_folder(src, dst):
    try:
        os.rename(src, dst)
        return f"Renamed {src} to {dst}"
    except Exception as e:
        return str(e)

def copy_file_folder(src, dst):
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        return f"Copied {src} to {dst}"
    except Exception as e:
        return str(e)

def move_file_folder(src, dst):
    try:
        shutil.move(src, dst)
        return f"Moved {src} to {dst}"
    except Exception as e:
        return str(e)

def search_file_folder(root, name):
    matches = []
    for dirpath, dirnames, filenames in os.walk(root):
        if name in dirnames or name in filenames:
            matches.append(os.path.join(dirpath, name))
    return matches

def get_file_folder_size(path):
    total_size = 0
    try:
        if os.path.isfile(path):
            total_size = os.path.getsize(path)
        else:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.isfile(fp):
                        total_size += os.path.getsize(fp)
        return f"Size: {total_size / (1024*1024):.2f} MB"
    except Exception as e:
        return str(e)

def open_file_folder(path):
    try:
        os.startfile(path)
        return f"Opened: {path}"
    except Exception as e:
        return str(e)

def zip_files(src_paths, zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for src in src_paths:
                if os.path.isfile(src):
                    zipf.write(src, os.path.basename(src))
                else:
                    for foldername, subfolders, filenames in os.walk(src):
                        for filename in filenames:
                            file_path = os.path.join(foldername, filename)
                            arcname = os.path.relpath(file_path, os.path.dirname(src))
                            zipf.write(file_path, arcname)
        return f"Created zip: {zip_path}"
    except Exception as e:
        return str(e)

def unzip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(extract_to)
        return f"Extracted to: {extract_to}"
    except Exception as e:
        return str(e)

def list_recently_modified(path, count=10):
    try:
        entries = []
        for root, dirs, files in os.walk(path):
            for name in files + dirs:
                full_path = os.path.join(root, name)
                mtime = os.path.getmtime(full_path)
                entries.append((full_path, mtime))
        entries.sort(key=lambda x: x[1], reverse=True)
        return [f"{e[0]} (Last modified: {datetime.fromtimestamp(e[1])})" for e in entries[:count]]
    except Exception as e:
        return [str(e)]

# --- Main Windows Section ---
def windows_section():
    st.header("🪟 Windows Assistant")
    category = st.selectbox("Choose Category", [
        "🗂️ File & Folder Management",
        # Add more categories here as you implement them
    ])

    if category == "🗂️ File & Folder Management":
        task = st.selectbox("Choose Task", [
            "View directory contents",
            "Create file/folder",
            "Delete file/folder",
            "Rename file/folder",
            "Copy file/folder",
            "Move file/folder",
            "Search for file/folder",
            "Get file/folder size",
            "Open file/folder",
            "Zip files/folders",
            "Unzip files",
            "List recently modified files/folders"
        ])
        st.divider()
        if task == "View directory contents":
            path = st.text_input("Directory path", value=os.getcwd())
            if st.button("View"):
                result = view_directory_contents(path)
                st.write(result)
        elif task == "Create file/folder":
            path = st.text_input("Path for new file/folder")
            is_folder = st.checkbox("Is Folder?", value=True)
            if st.button("Create"):
                result = create_file_folder(path, is_folder)
                st.success(result)
        elif task == "Delete file/folder":
            path = st.text_input("Path to delete")
            if st.button("Delete"):
                result = delete_file_folder(path)
                st.success(result)
        elif task == "Rename file/folder":
            src = st.text_input("Source path")
            dst = st.text_input("Destination path (new name)")
            if st.button("Rename"):
                result = rename_file_folder(src, dst)
                st.success(result)
        elif task == "Copy file/folder":
            src = st.text_input("Source path")
            dst = st.text_input("Destination path")
            if st.button("Copy"):
                result = copy_file_folder(src, dst)
                st.success(result)
        elif task == "Move file/folder":
            src = st.text_input("Source path")
            dst = st.text_input("Destination path")
            if st.button("Move"):
                result = move_file_folder(src, dst)
                st.success(result)
        elif task == "Search for file/folder":
            root = st.text_input("Root directory", value=os.getcwd())
            name = st.text_input("File/Folder name to search")
            if st.button("Search"):
                matches = search_file_folder(root, name)
                st.write(matches)
        elif task == "Get file/folder size":
            path = st.text_input("Path to file/folder")
            if st.button("Get Size"):
                result = get_file_folder_size(path)
                st.success(result)
        elif task == "Open file/folder":
            path = st.text_input("Path to open")
            if st.button("Open"):
                result = open_file_folder(path)
                st.success(result)
        elif task == "Zip files/folders":
            srcs = st.text_area("Paths to files/folders (comma separated)")
            zip_path = st.text_input("Destination zip file path")
            if st.button("Zip"):
                src_paths = [s.strip() for s in srcs.split(",") if s.strip()]
                result = zip_files(src_paths, zip_path)
                st.success(result)
        elif task == "Unzip files":
            zip_path = st.text_input("Zip file path")
            extract_to = st.text_input("Extract to directory")
            if st.button("Unzip"):
                result = unzip_file(zip_path, extract_to)
                st.success(result)
        elif task == "List recently modified files/folders":
            path = st.text_input("Directory path", value=os.getcwd())
            count = st.number_input("How many recent?", min_value=1, max_value=50, value=10)
            if st.button("List Recent"):
                result = list_recently_modified(path, int(count))
                st.write(result)
