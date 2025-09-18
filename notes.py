"""
Project Task Manager - 3-Column Kanban Board
Copyright (c) 2025 Gwen Balajediong
All rights reserved.

A modern project management application with workspace support.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import json
import os
import subprocess
import sys
from datetime import datetime

class ProjectTaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Project Task Manager - by Gwen Balajediong")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)
        self.root.minsize(1200, 700)  # Increased minimum width
        
        # Set window icon for taskbar
        self.set_window_icon()
        
        # Center the main window on screen
        self.center_window(1200, 800)
        
        # Configure style
        self.setup_styles()
        
        # Project management - store files in Documents/GwenProject/
        self.projects_file = os.path.join(self.get_documents_path(), "project_workspaces.json")
        self.current_project = "Default"
        self.projects = {}
        
        # Load projects first
        self.load_projects()
        
        # File to store tasks for current project in Documents/GwenProject/
        default_file = os.path.join(self.get_documents_path(), 'project_tasks.json')
        self.data_file = self.projects.get(self.current_project, {}).get('file', default_file)
        
        # Task data
        self.tasks = []
        self.load_tasks()
        
        # Setup the UI
        self.setup_ui()
        
        # Load existing tasks
        self.refresh_task_board()
        
        # Bind window close event to save data
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set icon again after window is fully loaded (for taskbar)
        self.root.after(100, self.refresh_taskbar_icon)
    
    def set_window_icon(self):
        """Set window icon for taskbar and title bar"""
        try:
            # Try to load the icon file if it exists
            icon_path = os.path.join(os.path.dirname(__file__), "project-icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                # Additional method to force taskbar icon update
                self.root.iconbitmap(default=icon_path)
            else:
                # Fallback - try in current directory
                if os.path.exists("project-icon.ico"):
                    self.root.iconbitmap("project-icon.ico")
                    self.root.iconbitmap(default="project-icon.ico")
            
            # Force icon refresh for taskbar (Windows-specific)
            try:
                # This helps Windows recognize the icon change
                self.root.wm_iconbitmap(icon_path if os.path.exists(icon_path) else "project-icon.ico")
            except:
                pass
                
        except Exception:
            # If icon loading fails, continue without custom icon
            pass
    
    def refresh_taskbar_icon(self):
        """Force refresh of taskbar icon after window is fully loaded"""
        try:
            # Try to refresh the icon for the taskbar
            icon_path = os.path.join(os.path.dirname(__file__), "project-icon.ico")
            if os.path.exists(icon_path):
                # Force update the window icon
                self.root.iconbitmap(icon_path)
                self.root.wm_iconbitmap(icon_path)
            elif os.path.exists("project-icon.ico"):
                self.root.iconbitmap("project-icon.ico")
                self.root.wm_iconbitmap("project-icon.ico")
        except Exception:
            pass
    
    def get_documents_path(self):
        """Get the path to the GwenProject directory in Documents"""
        documents_path = os.path.expanduser("~/Documents/GwenProject")
        os.makedirs(documents_path, exist_ok=True)
        return documents_path
    
    def setup_styles(self):
        """Configure modern UI styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure treeview style
        style.configure("Custom.Treeview", 
                       background="#ecf0f1", 
                       foreground="#2c3e50", 
                       font=('Segoe UI', 10),
                       fieldbackground="#ecf0f1",
                       borderwidth=0)
        style.configure("Custom.Treeview.Heading", 
                       background="#9b59b6", 
                       foreground="white", 
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0,
                       relief="flat")
        
        # Configure scrollbar
        style.configure("Custom.Vertical.TScrollbar",
                       background="#bdc3c7",
                       troughcolor="#ecf0f1",
                       borderwidth=0,
                       arrowcolor="#7f8c8d")
    
    def center_window(self, width, height):
        """Center the window on the screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        # Main container with gradient-like effect
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header section
        header_frame = tk.Frame(main_container, bg='#8e44ad', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title container in header
        title_container = tk.Frame(header_frame, bg='#8e44ad')
        title_container.pack(expand=True, fill=tk.BOTH, padx=30, pady=15)
        
        title_label = tk.Label(title_container, text="🪛 Project Tasks", 
                              font=('Segoe UI', 28, 'bold'), 
                              bg='#8e44ad', fg='#ecf0f1')
        title_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Project selector and management
        project_frame = tk.Frame(title_container, bg='#8e44ad')
        project_frame.pack(side=tk.LEFT, anchor=tk.W, padx=(30, 0))
        
        # Current project label
        tk.Label(project_frame, text="Workspace:", 
                font=('Segoe UI', 10, 'bold'), 
                bg='#8e44ad', fg='#ecf0f1').pack(anchor=tk.W)
        
        # Project selector frame
        selector_frame = tk.Frame(project_frame, bg='#8e44ad')
        selector_frame.pack(fill=tk.X, pady=(2, 0))
        
        # Project dropdown
        self.project_var = tk.StringVar(value=self.current_project)
        self.project_dropdown = ttk.Combobox(selector_frame, textvariable=self.project_var,
                                           values=list(self.projects.keys()),
                                           state="readonly", width=15,
                                           font=('Segoe UI', 9))
        self.project_dropdown.pack(side=tk.LEFT, padx=(0, 5))
        self.project_dropdown.bind('<<ComboboxSelected>>', self.on_project_change)
        
        # Project management buttons
        new_project_btn = tk.Button(selector_frame, text="➕", 
                                   command=self.create_new_project,
                                   bg='#27ae60', fg='white', 
                                   font=('Segoe UI', 8, 'bold'),
                                   relief=tk.FLAT, bd=0, width=2, height=1,
                                   cursor='hand2', activebackground='#229954')
        new_project_btn.pack(side=tk.LEFT, padx=(0, 2))
        
        manage_btn = tk.Button(selector_frame, text="⚙️", 
                             command=self.manage_projects,
                             bg='#f39c12', fg='white', 
                             font=('Segoe UI', 8, 'bold'),
                             relief=tk.FLAT, bd=0, width=2, height=1,
                             cursor='hand2', activebackground='#e67e22')
        manage_btn.pack(side=tk.LEFT)
        
        # Modern add button in header
        add_btn = tk.Button(title_container, text="➕ New Task", 
                           command=self.show_add_dialog,
                           bg='#9b59b6', fg='white', 
                           font=('Segoe UI', 12, 'bold'),
                           relief=tk.FLAT, bd=0, padx=25, pady=12,
                           cursor='hand2',
                           activebackground='#8e44ad',
                           activeforeground='white')
        add_btn.pack(side=tk.RIGHT, anchor=tk.E)
        
        # Content area
        content_frame = tk.Frame(main_container, bg='#ecf0f1')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Stats section
        stats_frame = tk.Frame(content_frame, bg='#ecf0f1', height=60)
        stats_frame.pack(fill=tk.X, padx=30, pady=(20, 10))
        stats_frame.pack_propagate(False)
        
        self.stats_label = tk.Label(stats_frame, text="", 
                                   font=('Segoe UI', 12, 'bold'), 
                                   bg='#ecf0f1', fg='#7f8c8d')
        self.stats_label.pack(anchor=tk.W, pady=15)
        
        # Trello-style board with 3 columns
        board_frame = tk.Frame(content_frame, bg='#ecf0f1')
        board_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Create three columns
        self.create_column(board_frame, "📋 Pending", "pending", "#e74c3c")
        self.create_column(board_frame, "⚡ In Progress", "in_progress", "#f39c12")
        self.create_column(board_frame, "✅ Done", "done", "#27ae60")
    
    def create_column(self, parent, title, status, color):
        """Create a Trello-style column"""
        # Column container with better width management
        column_frame = tk.Frame(parent, bg='#ecf0f1', width=380)
        column_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        column_frame.pack_propagate(False)
        
        # Shadow frame for depth effect
        shadow_frame = tk.Frame(column_frame, bg='#bdc3c7', height=3)
        shadow_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Column header with gradient effect
        header_frame = tk.Frame(column_frame, bg=color, height=70)
        header_frame.pack(fill=tk.X, pady=(0, 0))
        header_frame.pack_propagate(False)
        
        # Header content with icon and count
        header_content = tk.Frame(header_frame, bg=color)
        header_content.pack(expand=True, fill=tk.BOTH, padx=20, pady=15)
        
        header_label = tk.Label(header_content, text=title, 
                               font=('Segoe UI', 16, 'bold'), 
                               bg=color, fg='white')
        header_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Task count badge - smaller and more compact
        count_label = tk.Label(header_content, text="0", 
                              font=('Segoe UI', 10, 'bold'),
                              bg='white', fg=color,
                              width=2, height=1, padx=2, pady=1)
        count_label.pack(side=tk.RIGHT, anchor=tk.E, padx=(5, 0))
        
        # Store count label reference
        if not hasattr(self, 'count_labels'):
            self.count_labels = {}
        self.count_labels[status] = count_label
        
        # Tasks container with modern styling
        tasks_container = tk.Frame(column_frame, bg='#f8f9fa', relief=tk.FLAT, bd=0)
        tasks_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas and scrollbar for scrolling with modern styling
        canvas = tk.Canvas(tasks_container, bg='#f8f9fa', highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(tasks_container, orient=tk.VERTICAL, command=canvas.yview,
                               bg='#dee2e6', troughcolor='#f8f9fa', width=12)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        # Configure scrolling
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<MouseWheel>", on_mouse_wheel)
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Configure canvas window width
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width-25)
        canvas.bind("<Configure>", configure_canvas_width)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=15)
        
        # Store column references
        if not hasattr(self, 'columns'):
            self.columns = {}
        self.columns[status] = {
            'frame': scrollable_frame,
            'canvas': canvas,
            'color': color
        }
    
    def show_add_dialog(self):
        """Show a modern dialog for adding new tasks"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Task")
        dialog.geometry("500x250")
        dialog.configure(bg='#ecf0f1')
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set dialog icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "project-icon.ico")
            if os.path.exists(icon_path):
                dialog.iconbitmap(icon_path)
            elif os.path.exists("project-icon.ico"):
                dialog.iconbitmap("project-icon.ico")
        except Exception:
            pass
        
        # Center the dialog relative to parent window
        dialog.update_idletasks()
        parent_x = self.root.winfo_x()
        parent_y = self.root.winfo_y()
        parent_width = self.root.winfo_width()
        parent_height = self.root.winfo_height()
        x = parent_x + (parent_width // 2) - (500 // 2)
        y = parent_y + (parent_height // 2) - (250 // 2)
        dialog.geometry(f"500x250+{x}+{y}")
        
        # Main container with proper padding
        main_frame = tk.Frame(dialog, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="➕ Create New Task", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(pady=(0, 25))
        
        # Task title input
        title_input_label = tk.Label(main_frame, text="Task Title:", 
                              font=('Segoe UI', 12, 'bold'), 
                              bg='#ecf0f1', fg='#34495e')
        title_input_label.pack(anchor=tk.W, pady=(0, 8))
        
        task_title_entry = tk.Entry(main_frame, font=('Segoe UI', 12), 
                             relief=tk.FLAT, bd=0,
                             bg='white', fg='#2c3e50', insertbackground='#2c3e50')
        task_title_entry.pack(fill=tk.X, pady=(0, 30), ipady=8)
        task_title_entry.focus_set()
        
        # Button frame - FIXED: Ensure this is visible
        button_frame = tk.Frame(main_frame, bg='#ecf0f1')
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        def add_task():
            title = task_title_entry.get().strip()
            if title:
                task_item = {
                    'id': len(self.tasks) + 1,
                    'title': title,
                    'status': 'pending',
                    'created': datetime.now().strftime('%b %d, %Y - %I:%M%p'),
                    'modified': datetime.now().strftime('%b %d, %Y - %I:%M%p')
                }
                self.tasks.append(task_item)
                self.refresh_task_board()
                self.save_tasks()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter a task title!")
        
        def cancel():
            dialog.destroy()
        
        # Buttons with better styling
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                              command=cancel,
                              bg='#95a5a6', fg='white', 
                              font=('Segoe UI', 12, 'bold'),
                              relief=tk.FLAT, bd=0, padx=30, pady=15,
                              cursor='hand2',
                              activebackground='#7f8c8d')
        cancel_btn.pack(side=tk.RIGHT, padx=(15, 0))
        
        add_btn = tk.Button(button_frame, text="Add Task", 
                           command=add_task,
                           bg='#3498db', fg='white', 
                           font=('Segoe UI', 12, 'bold'),
                           relief=tk.FLAT, bd=0, padx=30, pady=15,
                           cursor='hand2',
                           activebackground='#2980b9')
        add_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key to add task
        task_title_entry.bind('<Return>', lambda e: add_task())
        dialog.bind('<Escape>', lambda e: cancel())
    
    def refresh_task_board(self):
        """Refresh all task columns"""
        # Clear all columns
        for status, column in self.columns.items():
            for widget in column['frame'].winfo_children():
                widget.destroy()
        
        # Add tasks to appropriate columns
        for task in self.tasks:
            self.add_task_card(task)
        
        self.update_stats()
    
    def add_task_card(self, task):
        """Add a compact task card to the appropriate column"""
        status = task['status']
        if status not in self.columns:
            return

        frame = self.columns[status]['frame']
        color = self.columns[status]['color']
        
        # Create compact card container
        card_container = tk.Frame(frame, bg='#f8f9fa')
        card_container.pack(fill=tk.X, padx=5, pady=3)
        
        # Simple card with minimal styling
        card = tk.Frame(card_container, bg='white', relief=tk.FLAT, bd=1)
        card.pack(fill=tk.X, padx=1, pady=1)
        
        # Colored left border for status indication
        border = tk.Frame(card, bg=color, width=4)
        border.pack(side=tk.LEFT, fill=tk.Y)
        
        # Content area with task title only
        content_frame = tk.Frame(card, bg='white')
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        # Small delete button (fixed position)
        delete_btn = tk.Label(card, text="×", 
                             font=('Segoe UI', 12, 'bold'),
                             bg='white', fg='#dc3545',
                             width=2, cursor='hand2')
        delete_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Task title (main clickable area) - reduced wrap length to account for delete button
        title_label = tk.Label(content_frame, text=task['title'], 
                              font=('Segoe UI', 11), 
                              bg='white', fg='#2c3e50',
                              wraplength=200, justify=tk.LEFT, anchor='w',
                              cursor='hand2')
        title_label.pack(anchor=tk.W, fill=tk.X)
        
        # Double-click to move to next status
        def on_double_click(event):
            if status == "pending":
                self.move_task(task, "in_progress")
            elif status == "in_progress":
                self.move_task(task, "done")
            elif status == "done":
                self.move_task(task, "pending")  # Cycle back to pending
        
        # Right-click for context menu (alternative to double-click)
        def show_context_menu(event):
            context_menu = tk.Menu(self.root, tearoff=0)
            
            if status == "pending":
                context_menu.add_command(label="▶️ Start Task", 
                                       command=lambda: self.move_task(task, "in_progress"))
            elif status == "in_progress":
                context_menu.add_command(label="✅ Mark Done", 
                                       command=lambda: self.move_task(task, "done"))
                context_menu.add_command(label="⬅️ Move Back", 
                                       command=lambda: self.move_task(task, "pending"))
            elif status == "done":
                context_menu.add_command(label="🔄 Reopen", 
                                       command=lambda: self.move_task(task, "pending"))
            
            context_menu.add_separator()
            context_menu.add_command(label="🗑️ Delete", 
                                   command=lambda: self.delete_task(task))
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
        
        # Bind events
        title_label.bind("<Double-Button-1>", on_double_click)
        title_label.bind("<Button-3>", show_context_menu)  # Right-click
        card.bind("<Double-Button-1>", on_double_click)
        card.bind("<Button-3>", show_context_menu)
        content_frame.bind("<Double-Button-1>", on_double_click)
        content_frame.bind("<Button-3>", show_context_menu)
        
        # Delete button click
        delete_btn.bind("<Button-1>", lambda e: self.delete_task(task))
        
        # Hover effects for better UX
        def on_enter(event):
            card.config(bg='#f8f9fa')
            content_frame.config(bg='#f8f9fa')
            title_label.config(bg='#f8f9fa')
            delete_btn.config(bg='#f8f9fa')
            
        def on_leave(event):
            card.config(bg='white')
            content_frame.config(bg='white')
            title_label.config(bg='white')
            delete_btn.config(bg='white')
        
        # Bind hover effects to all components
        for widget in [card, content_frame, title_label, delete_btn]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
    
    def move_task(self, task, new_status):
        """Move task to a different status"""
        task['status'] = new_status
        task['modified'] = datetime.now().strftime('%b %d, %Y - %I:%M%p')
        self.refresh_task_board()
        self.save_tasks()
    
    def delete_task(self, task):
        """Delete a task"""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{task['title']}'?"):
            self.tasks.remove(task)
            self.refresh_task_board()
            self.save_tasks()
    
    def update_stats(self):
        """Update statistics display and column count badges"""
        total = len(self.tasks)
        pending = len([t for t in self.tasks if t['status'] == 'pending'])
        in_progress = len([t for t in self.tasks if t['status'] == 'in_progress'])
        done = len([t for t in self.tasks if t['status'] == 'done'])
        
        # Update column count badges
        if hasattr(self, 'count_labels'):
            self.count_labels['pending'].config(text=str(pending))
            self.count_labels['in_progress'].config(text=str(in_progress))
            self.count_labels['done'].config(text=str(done))
        
        # Get current workspace name
        workspace_name = self.current_project if self.current_project else "Default"
        
        if total == 0:
            stats_text = f"📁 Workspace: {workspace_name} | No tasks yet - click 'New Task' to get started! 🚀 | © 2025 Gwen Balajediong"
        else:
            completion_rate = (done / total) * 100 if total > 0 else 0
            stats_text = f"📁 {workspace_name} | 📊 {total} total tasks | 📋 {pending} pending | ⚡ {in_progress} in progress | ✅ {done} done | {completion_rate:.0f}% complete | © 2025 Gwen Balajediong"
        
        self.stats_label.config(text=stats_text)
    
    def refresh_project_dropdown(self):
        """Update the project dropdown with current projects"""
        self.project_dropdown['values'] = list(self.projects.keys())
        
    def load_projects(self):
        """Load project configurations from JSON"""
        try:
            if os.path.exists(self.projects_file):
                with open(self.projects_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.projects = data.get('projects', {})
                    self.current_project = data.get('current_project', 'Default')
                    
                    # Ensure we have at least a default project
                    if not self.projects:
                        default_file = os.path.join(self.get_documents_path(), 'project_tasks.json')
                        self.projects['Default'] = {'file': default_file}
                        
            else:
                # Create default project structure
                default_file = os.path.join(self.get_documents_path(), 'project_tasks.json')
                self.projects = {'Default': {'file': default_file}}
                self.current_project = 'Default'
                self.save_projects()
                
        except Exception as e:
            print(f"Error loading projects: {e}")
            default_file = os.path.join(self.get_documents_path(), 'project_tasks.json')
            self.projects = {'Default': {'file': default_file}}
            self.current_project = 'Default'

    def save_projects(self):
        """Save project configurations to JSON"""
        try:
            data = {
                'projects': self.projects,
                'current_project': self.current_project
            }
            with open(self.projects_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving projects: {e}")

    def on_project_change(self, event):
        """Handle project selection change"""
        new_project = self.project_var.get()
        if new_project != self.current_project:
            # Save current project's tasks
            self.save_tasks()
            
            # Switch to new project
            self.current_project = new_project
            self.save_projects()
            
            # Prompt user to restart
            tk.messagebox.showinfo("Project Changed", 
                                 f"Switched to project '{new_project}'.\n\nPlease restart the application to see the new project's tasks.")
            
    def refresh_columns(self):
        """Refresh all column displays with current tasks"""
        for column in ['todo', 'progress', 'done']:
            # Clear ALL widgets in the column, not just those with task_id
            for widget in self.columns[column]['frame'].winfo_children():
                widget.destroy()
            
            # Repopulate with current tasks
            column_tasks = [task for task in self.tasks if task['status'] == column]
            for task in column_tasks:
                self.add_task_card(task, column)
        
        # Update statistics
        self.update_stats()
        
        # Force UI update
        self.root.update_idletasks()

    def reload_application(self):
        """Reload the entire application for better readability after project changes"""
        # Load tasks from the current project
        self.load_tasks()
        
        # Clear all existing content
        for column in ['todo', 'progress', 'done']:
            for widget in self.columns[column]['frame'].winfo_children():
                widget.destroy()
        
        # Refresh all displays
        self.refresh_columns()
        
        # Update window title to show current project
        project_name = self.current_project if self.current_project else "Default"
        self.root.title(f"Project Task Manager - {project_name}")

    def create_new_project(self):
        """Create a new project workspace"""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Project Workspace")
        dialog.geometry("400x200")
        dialog.configure(bg='#2c3e50')
        # Try to set icon, but don't fail if it doesn't exist
        try:
            dialog.iconbitmap(os.path.join(os.path.dirname(__file__), 'project_icon.ico'))
        except:
            pass
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(main_frame, text="Create New Project", 
                font=('Segoe UI', 14, 'bold'), 
                bg='#2c3e50', fg='#ecf0f1').pack(pady=(0, 15))
        
        # Project name input
        tk.Label(main_frame, text="Project Name:", 
                font=('Segoe UI', 10), 
                bg='#2c3e50', fg='#ecf0f1').pack(anchor=tk.W, pady=(0, 5))
        
        name_entry = tk.Entry(main_frame, font=('Segoe UI', 10), width=35)
        name_entry.pack(fill=tk.X, pady=(0, 15))
        name_entry.focus()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(fill=tk.X)
        
        def create_project():
            project_name = name_entry.get().strip()
            if project_name and project_name not in self.projects:
                # Create unique filename for project in Documents/GwenProject/
                filename = f"project_{project_name.lower().replace(' ', '_')}.json"
                full_path = os.path.join(self.get_documents_path(), filename)
                self.projects[project_name] = {'file': full_path}
                self.save_projects()
                
                # Switch to new project
                self.project_var.set(project_name)
                self.current_project = project_name
                
                # Close dialog first
                dialog.destroy()
                
                # Show success message
                tk.messagebox.showinfo("Project Created", 
                                     f"Project '{project_name}' created successfully!\n\nPlease restart the application to switch to the new project.")
                
            elif project_name in self.projects:
                tk.messagebox.showerror("Error", f"Project '{project_name}' already exists!")
            else:
                tk.messagebox.showerror("Error", "Please enter a project name!")
        
        def cancel():
            dialog.destroy()
        
        tk.Button(button_frame, text="Create", command=create_project,
                 bg='#27ae60', fg='white', font=('Segoe UI', 10, 'bold'),
                 relief=tk.FLAT, bd=0, padx=20, pady=8,
                 cursor='hand2', activebackground='#229954').pack(side=tk.RIGHT, padx=(5, 0))
        
        tk.Button(button_frame, text="Cancel", command=cancel,
                 bg='#95a5a6', fg='white', font=('Segoe UI', 10),
                 relief=tk.FLAT, bd=0, padx=20, pady=8,
                 cursor='hand2', activebackground='#7f8c8d').pack(side=tk.RIGHT)
        
        # Bind Enter key to create
        name_entry.bind('<Return>', lambda e: create_project())

    def manage_projects(self):
        """Manage existing projects"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Projects")
        dialog.geometry("500x400")
        dialog.configure(bg='#2c3e50')
        # Try to set icon, but don't fail if it doesn't exist
        try:
            dialog.iconbitmap(os.path.join(os.path.dirname(__file__), 'project_icon.ico'))
        except:
            pass
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(main_frame, text="Project Workspaces", 
                font=('Segoe UI', 14, 'bold'), 
                bg='#2c3e50', fg='#ecf0f1').pack(pady=(0, 15))
        
        # Projects list
        list_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.SUNKEN, bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Scrollable listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        projects_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                     bg='#34495e', fg='#ecf0f1',
                                     font=('Segoe UI', 10),
                                     selectbackground='#8e44ad',
                                     relief=tk.FLAT, bd=0)
        projects_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=projects_listbox.yview)
        
        # Populate projects list
        for project in self.projects.keys():
            status = " (Current)" if project == self.current_project else ""
            projects_listbox.insert(tk.END, f"{project}{status}")
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(fill=tk.X)
        
        def rename_project():
            selection = projects_listbox.curselection()
            if not selection:
                tk.messagebox.showwarning("Warning", "Please select a project to rename!")
                return
                
            old_name = list(self.projects.keys())[selection[0]]
            if old_name == 'Default':
                tk.messagebox.showwarning("Warning", "Cannot rename the Default project!")
                return
                
            new_name = tk.simpledialog.askstring("Rename Project", 
                                                f"Enter new name for '{old_name}':",
                                                initialvalue=old_name)
            if new_name and new_name != old_name and new_name not in self.projects:
                self.projects[new_name] = self.projects.pop(old_name)
                if self.current_project == old_name:
                    self.current_project = new_name
                self.save_projects()
                self.refresh_project_dropdown()
                self.project_var.set(self.current_project)
                
                # Reload application for better readability
                self.reload_application()
                
                dialog.destroy()
            elif new_name in self.projects:
                tk.messagebox.showerror("Error", f"Project '{new_name}' already exists!")
        
        def delete_project():
            selection = projects_listbox.curselection()
            if not selection:
                tk.messagebox.showwarning("Warning", "Please select a project to delete!")
                return
                
            project_name = list(self.projects.keys())[selection[0]]
            if project_name == 'Default':
                tk.messagebox.showwarning("Warning", "Cannot delete the Default project!")
                return
                
            if len(self.projects) <= 1:
                tk.messagebox.showwarning("Warning", "Cannot delete the last project!")
                return
                
            if tk.messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete project '{project_name}'?\n\nThis will permanently delete all tasks in this project!"):
                # Delete project file if it exists
                project_file = self.projects[project_name]['file']
                if os.path.exists(project_file):
                    try:
                        os.remove(project_file)
                    except:
                        pass
                
                # Remove from projects
                del self.projects[project_name]
                
                # Switch to Default if current project was deleted
                if self.current_project == project_name:
                    self.current_project = 'Default'
                
                self.save_projects()
                
                # Close dialog first
                dialog.destroy()
                
                # Show success message
                tk.messagebox.showinfo("Project Deleted", 
                                     f"Project '{project_name}' deleted successfully!\n\nPlease restart the application to see the changes.")
        
        def close_dialog():
            dialog.destroy()
        
        tk.Button(button_frame, text="Rename", command=rename_project,
                 bg='#f39c12', fg='white', font=('Segoe UI', 10),
                 relief=tk.FLAT, bd=0, padx=15, pady=8,
                 cursor='hand2', activebackground='#e67e22').pack(side=tk.LEFT)
        
        tk.Button(button_frame, text="Delete", command=delete_project,
                 bg='#e74c3c', fg='white', font=('Segoe UI', 10),
                 relief=tk.FLAT, bd=0, padx=15, pady=8,
                 cursor='hand2', activebackground='#c0392b').pack(side=tk.LEFT, padx=(5, 0))
        
        tk.Button(button_frame, text="Close", command=close_dialog,
                 bg='#95a5a6', fg='white', font=('Segoe UI', 10),
                 relief=tk.FLAT, bd=0, padx=20, pady=8,
                 cursor='hand2', activebackground='#7f8c8d').pack(side=tk.RIGHT)
    
    def load_tasks(self):
        """Load tasks from current project file"""
        # Get the current project's data file
        default_file = os.path.join(self.get_documents_path(), 'project_tasks.json')
        self.data_file = self.projects.get(self.current_project, {}).get('file', default_file)
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")
    
    def on_closing(self):
        """Handle window closing"""
        self.save_tasks()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ProjectTaskApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
