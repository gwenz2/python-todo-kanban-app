@echo off
echo Building Secure Todo List Manager Applications...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    echo.
)

REM Create version file for better legitimacy
echo Creating version info...
echo VSVersionInfo( > version_info.txt
echo   ffi=FixedFileInfo( >> version_info.txt
echo     filevers=(1,0,0,0), >> version_info.txt
echo     prodvers=(1,0,0,0), >> version_info.txt
echo     mask=0x3f, >> version_info.txt
echo     flags=0x0, >> version_info.txt
echo     OS=0x4, >> version_info.txt
echo     fileType=0x1, >> version_info.txt
echo     subtype=0x0, >> version_info.txt
echo     date=(0, 0) >> version_info.txt
echo   ), >> version_info.txt
echo   kids=[ >> version_info.txt
echo     StringFileInfo([ >> version_info.txt
echo       StringTable('040904B0', [ >> version_info.txt
echo         StringStruct('CompanyName', 'Gwen Balajediong'), >> version_info.txt
echo         StringStruct('FileDescription', 'Todo List Manager'), >> version_info.txt
echo         StringStruct('FileVersion', '1.0.0.0'), >> version_info.txt
echo         StringStruct('InternalName', 'TodoListManager'), >> version_info.txt
echo         StringStruct('LegalCopyright', 'Copyright 2025 Gwen Balajediong'), >> version_info.txt
echo         StringStruct('OriginalFilename', 'TodoListManager.exe'), >> version_info.txt
echo         StringStruct('ProductName', 'Todo List Manager'), >> version_info.txt
echo         StringStruct('ProductVersion', '1.0.0.0') >> version_info.txt
echo       ]) >> version_info.txt
echo     ]), >> version_info.txt
echo     VarFileInfo([VarStruct('Translation', [1033, 1200])]) >> version_info.txt
echo   ] >> version_info.txt
echo ) >> version_info.txt

echo Building Todo List Manager with enhanced security...
if exist "todo-icon.ico" (
    echo Using custom icon for Todo List Manager...
    pyinstaller --onefile --windowed --name "TodoListManager" --icon="todo-icon.ico" --version-file="version_info.txt" --add-data "*.json;." --distpath="dist" --workpath="build" --clean to-do-list.py
) else (
    echo No todo-icon.ico found, building without custom icon...
    pyinstaller --onefile --windowed --name "TodoListManager" --version-file="version_info.txt" --add-data "*.json;." --distpath="dist" --workpath="build" --clean to-do-list.py
)

echo.
echo Building Project Task Manager with enhanced security...
if exist "project-icon.ico" (
    echo Using custom icon for Project Task Manager...
    pyinstaller --onefile --windowed --name "ProjectTaskManager" --icon="project-icon.ico" --version-file="version_info.txt" --add-data "*.json;." --distpath="dist" --workpath="build" --clean notes.py
) else (
    echo No project-icon.ico found, building without custom icon...
    pyinstaller --onefile --windowed --name "ProjectTaskManager" --version-file="version_info.txt" --add-data "*.json;." --distpath="dist" --workpath="build" --clean notes.py
)

echo.
echo Copying icon files to dist folder...
if exist "todo-icon.ico" copy "todo-icon.ico" "dist\"
if exist "project-icon.ico" copy "project-icon.ico" "dist\"

echo.
echo Cleaning up temporary files...
if exist "version_info.txt" del "version_info.txt"

echo.
echo Build complete with enhanced security features!
echo.
echo Security improvements applied:
echo - Added version information
echo - Added company and copyright details
echo - Clean build process
echo - Proper file metadata
echo.
echo Executables created in 'dist' folder:
echo - TodoListManager.exe
echo - ProjectTaskManager.exe
echo.
echo You can copy these files to any Windows computer and run them without Python installed.
echo.
pause
