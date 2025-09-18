@echo off
echo Creating sample icons from Windows system icons...
echo.

REM Check if we have PowerShell available for icon extraction
powershell -Command "Get-Command Add-Type" >nul 2>&1
if errorlevel 1 (
    echo PowerShell not available for icon extraction.
    echo Please download .ico files manually.
    pause
    exit /b 1
)

echo Extracting system icons...

REM Create a simple PowerShell script to extract icons
echo Add-Type -AssemblyName System.Drawing > extract_icon.ps1
echo $icon = [System.Drawing.Icon]::ExtractAssociatedIcon("%SystemRoot%\System32\notepad.exe") >> extract_icon.ps1
echo $icon.ToBitmap().Save("todo-icon-temp.png", [System.Drawing.Imaging.ImageFormat]::Png) >> extract_icon.ps1
echo $icon = [System.Drawing.Icon]::ExtractAssociatedIcon("%SystemRoot%\System32\mmc.exe") >> extract_icon.ps1
echo $icon.ToBitmap().Save("project-icon-temp.png", [System.Drawing.Imaging.ImageFormat]::Png) >> extract_icon.ps1

powershell -ExecutionPolicy Bypass -File extract_icon.ps1

if exist "todo-icon-temp.png" (
    echo Created todo-icon-temp.png
)
if exist "project-icon-temp.png" (
    echo Created project-icon-temp.png
)

del extract_icon.ps1 2>nul

echo.
echo Temporary PNG icons created. 
echo Convert these to .ico format using an online converter like ico-convert.com
echo Then rename them to todo-icon.ico and project-icon.ico
echo.
pause
