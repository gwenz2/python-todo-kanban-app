@echo off
title Todo List Manager
echo.
echo ========================================
echo    Todo List Manager
echo ========================================
echo.
echo 1. Todo List Manager
echo 2. Project Task Manager
echo 3. Exit
echo.
set /p choice=Choose an option (1-3): 

if "%choice%"=="1" (
    if exist "TodoListManager.exe" (
        start "" "TodoListManager.exe"
    ) else (
        echo TodoListManager.exe not found!
        pause
    )
)

if "%choice%"=="2" (
    if exist "ProjectTaskManager.exe" (
        start "" "ProjectTaskManager.exe"
    ) else (
        echo ProjectTaskManager.exe not found!
        pause
    )
)

if "%choice%"=="3" (
    exit
)

if not "%choice%"=="1" if not "%choice%"=="2" if not "%choice%"=="3" (
    echo Invalid choice!
    pause
    goto :eof
)
