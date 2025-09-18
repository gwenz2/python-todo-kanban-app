@echo off
echo Building Todo List Manager Applications...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    echo.
)

echo Building Todo List Manager...
if exist "todo-icon.ico" (
    echo Using custom icon for Todo List Manager...
    pyinstaller --onefile --windowed --name "TodoListManager" --icon="todo-icon.ico" to-do-list.py
) else (
    echo No todo-icon.ico found, building without custom icon...
    pyinstaller --onefile --windowed --name "TodoListManager" to-do-list.py
)

echo.
echo Building Project Task Manager...
if exist "project-icon.ico" (
    echo Using custom icon for Project Task Manager...
    pyinstaller --onefile --windowed --name "ProjectTaskManager" --icon="project-icon.ico" notes.py
) else (
    echo No project-icon.ico found, building without custom icon...
    pyinstaller --onefile --windowed --name "ProjectTaskManager" notes.py
)

echo.
echo Build complete!
echo.
echo Executables created in 'dist' folder:
echo - TodoListManager.exe
echo - ProjectTaskManager.exe
echo.
echo You can copy these files to any Windows computer and run them without Python installed.
echo.
pause
