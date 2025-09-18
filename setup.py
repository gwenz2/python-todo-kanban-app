import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some modules that are imported 
# dynamically need to be explicitly included
build_exe_options = {
    "packages": ["tkinter", "json", "os", "subprocess", "datetime"],
    "excludes": ["test", "unittest"],
    "include_files": []
}

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="TodoListManager",
    version="1.0",
    description="Modern Todo List and Project Task Manager",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("to-do-list.py", base=base, target_name="TodoListManager.exe"),
        Executable("notes.py", base=base, target_name="ProjectTaskManager.exe")
    ]
)
