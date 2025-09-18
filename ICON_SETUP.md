# Icon Setup Guide

## Quick Icon Sources (Free)

### For Todo List Manager (todo-icon.ico):
- 📝 Checklist icons
- 📋 Clipboard icons
- ✅ Task completion icons
- 📄 Document icons

### For Project Task Manager (project-icon.ico):
- 🪛 Tools/Settings icons
- 📊 Project/Dashboard icons
- 🏗️ Construction/Building icons
- 📈 Chart/Analytics icons

## Recommended Free Icon Sites:

1. **Icons8** (https://icons8.com/icons)
   - Search: "checklist", "todo", "project", "kanban"
   - Download as ICO format (Windows icon)
   - Sizes: 256x256 or 512x512 recommended

2. **FlatIcon** (https://www.flaticon.com/)
   - Free with attribution
   - Download as ICO format
   - Good variety of business/productivity icons

3. **IconFinder** (https://www.iconfinder.com/)
   - Filter by "Free" and "ICO format"
   - Professional looking icons

## Creating Your Own Icons:

### From PNG/JPG Images:
1. **Online Converter**: ico-convert.com
   - Upload your image (PNG works best)
   - Select multiple sizes (16x16, 32x32, 48x48, 256x256)
   - Download the .ico file

2. **Using Paint (Windows built-in)**:
   - Create a 256x256 pixel image
   - Save as PNG first
   - Use online converter to convert to ICO

### Icon Design Tips:
- **Simple designs** work best at small sizes
- **High contrast** for visibility
- **Square format** (1:1 ratio)
- **Multiple sizes** in one ICO file for best quality

## File Naming:
- Todo app icon: `todo-icon.ico`
- Project app icon: `project-icon.ico`
- Place both files in: `c:\Users\gwenb\Documents\pyTODOLIST\`

## Testing Icons:
After downloading/creating your icons:
1. Place them in your project folder
2. Run the updated build script
3. Check the resulting EXE files in Windows Explorer
4. The custom icons should appear on the executable files

## Current Build Command:
```bash
.\build_apps.bat
```

The script will automatically detect if icon files exist and use them during the build process.
