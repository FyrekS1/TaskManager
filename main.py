import json
from customtkinter import *
from tkinter import messagebox, PhotoImage
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_data_path():
    appdata = os.getenv('APPDATA')
    folder = os.path.join(appdata, "Fyreks", "TaskManager")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "tasks.json")

FILE = get_data_path()

def load_tasks():
    if os.path.exists(FILE):
        with open(FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def complete_task(taskname):
    tasks = load_tasks()
    if taskname in tasks:
        tasks[taskname]["done"] = True
        save_tasks(tasks)
        refresh_task_list()

def delete_task(taskname):
    tasks = load_tasks()
    if taskname in tasks:
        del tasks[taskname]
        save_tasks(tasks)
        refresh_task_list()

def refresh_task_list():
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    tasks = load_tasks()
    if not tasks:
        CTkLabel(scroll_frame, text="Нет задач").pack(pady=10)
        return

    for name, info in tasks.items():
        status = "✅" if info['done'] else "❌"
        frame_task = CTkFrame(scroll_frame)
        frame_task.pack(fill="x", pady=5, padx=5)

        label = CTkLabel(frame_task, text=f"{name}: {info['task']} {status}", anchor="w")
        label.pack(side="left", fill="x", expand=True, padx=5)

        btn_done = CTkButton(frame_task, text="Выполнить", width=80,
                             command=lambda n=name: complete_task(n))
        btn_done.pack(side="left", padx=5)

        btn_delete = CTkButton(frame_task, text="Удалить", width=80,
                               command=lambda n=name: delete_task(n))
        btn_delete.pack(side="left", padx=5)

def add_task():
    name = entry_name.get().strip()
    task = entry_task.get().strip()

    if not name or not task:
        messagebox.showwarning("Ошибка", "Имя и описание задачи не могут быть пустыми")
        return

    tasks = load_tasks()
    if name in tasks:
        messagebox.showwarning("Ошибка", "Задача с таким именем уже существует")
        return

    tasks[name] = {"task": task, "done": False}
    save_tasks(tasks)

    entry_name.delete(0, "end")
    entry_task.delete(0, "end")
    entry_name.focus()
    refresh_task_list()

set_appearance_mode("dark")
set_default_color_theme("blue")

root = CTk()
root.title("Task Manager")

icon_path = resource_path("icon.png")

try:
    icon = PhotoImage(file=icon_path)
    root.iconphoto(False, icon)
except Exception as e:
    print("Ошибка загрузки иконки:", e)

root.geometry("600x600")

frame_input = CTkFrame(root)
frame_input.pack(fill="x", pady=10, padx=10)

entry_name = CTkEntry(frame_input, placeholder_text="Имя задачи")
entry_name.pack(side="left", padx=5, pady=5)

entry_task = CTkEntry(frame_input, placeholder_text="Описание задачи")
entry_task.pack(side="left", padx=5, pady=5, fill="x", expand=True)

btn_add = CTkButton(frame_input, text="Добавить", command=add_task)
btn_add.pack(side="left", padx=5, pady=5)

scroll_frame = CTkScrollableFrame(root, width=580, height=450)
scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

refresh_task_list()

root.mainloop()
