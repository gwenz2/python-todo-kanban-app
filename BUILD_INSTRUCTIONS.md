# Todo List Application - Standalone Distribution

## Method 1: PyInstaller (Recommended - Single Executable File)

### Step 1: Install PyInstaller
```bash
pip install pyinstaller
```

### Step 2: Create Standalone Executable
```bash
# Navigate to your project directory
cd "c:\Users\gwenb\Documents\pyTODOLIST"

# Create single file executable (most portable)
pyinstaller --onefile --windowed --name "TodoListManager" to-do-list.py

# Alternative: Create folder with executable (faster startup)
pyinstaller --onedir --windowed --name "TodoListManager" to-do-list.py
```

### Step 3: Find Your Executable
- Single file: `dist\TodoListManager.exe`
- Folder version: `dist\TodoListManager\TodoListManager.exe`

### Step 4: Include Both Apps (Todo + Notes)
```bash
# Build both applications
pyinstaller --onefile --windowed --name "TodoListManager" to-do-list.py
pyinstaller --onefile --windowed --name "ProjectTaskManager" notes.py
```

## Method 2: Auto-py-to-exe (GUI Tool)

### Step 1: Install
```bash
pip install auto-py-to-exe
```

### Step 2: Run GUI
```bash
auto-py-to-exe
```

### Step 3: Configure Settings
- Script Location: Browse to `to-do-list.py`
- Onefile: One File
- Console Window: Window Based (hide the console)
- Additional Files: None needed (all dependencies are built-in)

## Method 3: cx_Freeze

### Step 1: Install
```bash
pip install cx_freeze
```

### Step 2: Create setup.py (see setup.py file)

### Step 3: Build
```bash
python setup.py build
```

## Distribution Options

### For Single Computer
1. Copy the `.exe` file to any folder
2. Double-click to run
3. The app will create `todos.json` and `project_tasks.json` in the same folder

### For Multiple Computers
1. **USB Drive**: Copy `.exe` to USB, run from anywhere
2. **Network Share**: Place on shared drive
3. **Email/Cloud**: Send the `.exe` file (small size ~10-15MB)
4. **Installer**: Use tools like Inno Setup or NSIS to create a proper installer

## Important Notes

1. **Data Files**: The JSON files (`todos.json`, `project_tasks.json`) will be created in the same directory as the executable
2. **Both Apps**: You'll need to build both `to-do-list.py` and `notes.py` separately if you want both features
3. **Navigation**: Update the file paths in the navigation code to work with executables
4. **Testing**: Always test the executable on a clean computer without Python installed

## Recommended Final Steps

1. Build both applications
2. Create a folder with both `.exe` files
3. Test on a computer without Python
4. Create a simple batch file or shortcut for easy access

## File Sizes (Approximate)
- Single file executable: 15-20 MB
- Folder distribution: 25-30 MB total
