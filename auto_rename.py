import os
import re
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap import Style

# 辅助函数：读取文件并尝试不同的编码
def read_file(file):
    try:
        return file.read().decode('utf-8')
    except UnicodeDecodeError:
        file.seek(0)  # 重置文件指针
        return file.read().decode('gbk')

# 提取ZIP文件中的标题
def extract_title_from_zip(zip_file_path, info_textbox):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for name in zip_ref.namelist():
                info_textbox.insert(tk.END, f"Trying file: {name}\n")
                if name.endswith('.txt'):
                    with zip_ref.open(name) as maidata_file:
                        content = read_file(maidata_file)
                        title = re.search(r'&title=([^&]+)', content)
                        if title:
                            return title.group(1)
    except zipfile.BadZipFile:
        info_textbox.insert(tk.END, f"Error: Failed to open {zip_file_path}\n")
    except Exception as e:
        info_textbox.insert(tk.END, f"Error: {str(e)}\n")
    return None

# 清理文件名
def clean_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = re.sub(r'\s+', ' ', filename).strip()
    return filename

# 重命名ZIP文件
def rename_zip(zip_file_path, new_name):
    dir_path, file_name = os.path.split(zip_file_path)
    new_base_name = clean_filename(new_name)
    new_file_path = os.path.join(dir_path, new_base_name + '.zip')
    counter = 2
    while os.path.exists(new_file_path):
        new_file_path = os.path.join(dir_path, f'{new_base_name}_{counter}.zip')
        counter += 1
    os.rename(zip_file_path, new_file_path)
    return new_file_path

# 打开文件对话框并更新列表框
def open_files():
    file_paths = filedialog.askopenfilenames(filetypes=[('ZIP files', '*.zip')])
    if file_paths:
        listbox.delete(0, tk.END)  # 清空listbox中的内容
        for file_path in file_paths:
            listbox.insert(tk.END, file_path)

# 重命名文件的逻辑
def rename_files():
    processed_files = 0
    total_files = listbox.size()
    idx = 0
    while idx < listbox.size():
        file_path = listbox.get(idx)
        title = extract_title_from_zip(file_path, info_textbox)
        if title:
            found_info = f"Set title: {title}\n"
            info_textbox.insert(tk.END, found_info)
            info_textbox.see(tk.END)
            new_file_path = rename_zip(file_path, title)
            listbox.delete(idx)
            processed_files += 1
            progress_label.config(text=f'已处理文件：{processed_files}/{total_files}')
        else:
            messagebox.showwarning('无法重命名', f'无法从文件中提取标题：{file_path}')
            idx += 1

# 界面布局和逻辑
root = ttk.Window(themename='litera')  # 使用ttkbootstrap主题
root.title('重命名maimai ZIP文件')
root.geometry('600x400')
root.iconbitmap(r'E:\my_pyProject\auto_rename\myicon.ico')

top_frame = ttk.Frame(root, padding="3 3 12 12")
top_frame.grid(column=0, row=0, sticky=(tk.W, tk.E))

bottom_frame = ttk.Frame(root, padding="3 3 12 12")
bottom_frame.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))

open_button = ttk.Button(top_frame, text='打开ZIP文件', command=open_files)
open_button.grid(column=0, row=0, padx=10, pady=10)

rename_button = ttk.Button(top_frame, text='重命名ZIP文件', command=rename_files)
rename_button.grid(column=1, row=0, padx=10, pady=10)

progress_label = ttk.Label(top_frame, text='已处理文件：0/0')
progress_label.grid(column=2, row=0, padx=10, pady=10)

listbox = tk.Listbox(bottom_frame, borderwidth=2, relief="sunken")
listbox.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

scrollbar = ttk.Scrollbar(bottom_frame, orient=tk.VERTICAL, command=listbox.yview)
listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(column=1, row=0, sticky=(tk.N, tk.S))

info_textbox = tk.Text(bottom_frame, height=10, bg='light gray', fg='black', borderwidth=2, relief="sunken")
info_textbox.grid(column=0, row=1, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S))

scrollbar_info = ttk.Scrollbar(bottom_frame, orient=tk.VERTICAL, command=info_textbox.yview)
info_textbox.configure(yscrollcommand=scrollbar_info.set)
scrollbar_info.grid(column=1, row=1, sticky=(tk.N, tk.S))

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
bottom_frame.grid_columnconfigure(0, weight=1)
bottom_frame.grid_rowconfigure(0, weight=1)
bottom_frame.grid_rowconfigure(1, weight=1)

root.mainloop()
