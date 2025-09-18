"""
Todo List Manager - Single Column Task Manager
Copyright (c) 2025 Gwen Balajediong
All rights reserved.

A modern todo list application with beautiful card-based interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import subprocess
import sys
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Todo List Manager - by Gwen Balajediong")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)
        self.root.minsize(700, 600)  # Adjusted for single column layout
        
        # Set window icon for taskbar
        self.set_window_icon()
        
        # Center the main window on screen
        self.center_window(800, 700)
        
        # Configure style
        self.setup_styles()
        
        # File to store todos in Documents/GwenProject/
        self.data_file = os.path.join(self.get_documents_path(), "todos.json")
        
        # Todo list data
        self.todos = self.load_todos()
        
        # Setup the UI
        self.setup_ui()
        
        # Load existing todos
        self.refresh_todo_list()
        
        # Bind window close event to save data
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set icon again after window is fully loaded (for taskbar)
        self.root.after(100, self.refresh_taskbar_icon)
    
    def set_window_icon(self):
        """Set window icon for taskbar and title bar"""
        try:
            # Try to load the icon file if it exists
            icon_path = os.path.join(os.path.dirname(__file__), "todo-icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                # Additional method to force taskbar icon update
                self.root.iconbitmap(default=icon_path)
            else:
                # Fallback - try in current directory
                if os.path.exists("todo-icon.ico"):
                    self.root.iconbitmap("todo-icon.ico")
                    self.root.iconbitmap(default="todo-icon.ico")
            
            # Force icon refresh for taskbar (Windows-specific)
            try:
                # This helps Windows recognize the icon change
                self.root.wm_iconbitmap(icon_path if os.path.exists(icon_path) else "todo-icon.ico")
            except:
                pass
                
        except Exception:
            # If icon loading fails, continue without custom icon
            pass
    
    def get_documents_path(self):
        """Get the path to the GwenProject directory in Documents"""
        documents_path = os.path.expanduser("~/Documents/GwenProject")
        os.makedirs(documents_path, exist_ok=True)
        return documents_path
    
    def refresh_taskbar_icon(self):
        """Force refresh of taskbar icon after window is fully loaded"""
        try:
            # Try to refresh the icon for the taskbar
            icon_path = os.path.join(os.path.dirname(__file__), "todo-icon.ico")
            if os.path.exists(icon_path):
                # Force update the window icon
                self.root.iconbitmap(icon_path)
                self.root.wm_iconbitmap(icon_path)
            elif os.path.exists("todo-icon.ico"):
                self.root.iconbitmap("todo-icon.ico")
                self.root.wm_iconbitmap("todo-icon.ico")
        except Exception:
            pass
    
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
                       background="#3498db", 
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
        
        # Header section (matching notes.py style)
        header_frame = tk.Frame(main_container, bg='#8e44ad', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title container in header
        title_container = tk.Frame(header_frame, bg='#8e44ad')
        title_container.pack(expand=True, fill=tk.BOTH, padx=30, pady=15)
        
        title_label = tk.Label(title_container, text="📋 Todo Tasks", 
                              font=('Segoe UI', 28, 'bold'), 
                              bg='#8e44ad', fg='#ecf0f1')
        title_label.pack(side=tk.LEFT, anchor=tk.W)
        
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
        
        # Single-column task board (like notes.py but with one column)
        board_frame = tk.Frame(content_frame, bg='#ecf0f1')
        board_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Create single column for all tasks
        self.create_task_column(board_frame)
    
    def create_task_column(self, parent):
        """Create a single column for all tasks (like notes.py)"""
        # Column container with shadow effect
        column_frame = tk.Frame(parent, bg='#ecf0f1', width=700)
        column_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        column_frame.pack_propagate(False)
        
        # Column header with gradient effect (using blue theme for todos)
        header_frame = tk.Frame(column_frame, bg='#3498db', height=70)
        header_frame.pack(fill=tk.X, pady=(0, 0))
        header_frame.pack_propagate(False)
        
        # Header content with icon and count
        header_content = tk.Frame(header_frame, bg='#3498db')
        header_content.pack(expand=True, fill=tk.BOTH, padx=20, pady=15)
        
        header_label = tk.Label(header_content, text="📋 All Tasks", 
                               font=('Segoe UI', 16, 'bold'), 
                               bg='#3498db', fg='white')
        header_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Task count badge
        self.count_label = tk.Label(header_content, text="0", 
                              font=('Segoe UI', 10, 'bold'),
                              bg='white', fg='#3498db',
                              width=2, height=1, padx=2, pady=1)
        self.count_label.pack(side=tk.RIGHT, anchor=tk.E, padx=(5, 0))
        
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
            # Make sure we can scroll regardless of focus
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        
        def on_frame_click(event):
            # Give focus to the canvas area for better scrolling
            canvas.focus_set()
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<MouseWheel>", on_mouse_wheel)
        
        # Bind mouse wheel to main window and all child widgets for better scrolling
        def bind_mousewheel_recursive(widget):
            widget.bind("<MouseWheel>", on_mouse_wheel)
            for child in widget.winfo_children():
                bind_mousewheel_recursive(child)
        
        # Apply mousewheel binding to the entire application
        self.root.bind("<MouseWheel>", on_mouse_wheel)
        bind_mousewheel_recursive(self.root)
        
        # Bind click events to help with focus
        canvas.bind("<Button-1>", on_frame_click)
        scrollable_frame.bind("<Button-1>", on_frame_click)
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Configure canvas window width
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width-25)
        canvas.bind("<Configure>", configure_canvas_width)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=15)
        
        # Store column references
        self.tasks_frame = scrollable_frame
        self.canvas = canvas
    
    def add_task_card(self, task):
        """Add a compact task card (like notes.py but for todos)"""
        frame = self.tasks_frame
        color = "#27ae60" if task['completed'] else "#3498db"
        
        # Create compact card container
        card_container = tk.Frame(frame, bg='#f8f9fa')
        card_container.pack(fill=tk.X, padx=10, pady=8)
        
        # Main card with modern styling
        card = tk.Frame(card_container, bg='white', relief=tk.FLAT, bd=0)
        card.pack(fill=tk.X, padx=2, pady=2)
        
        # Top accent bar
        accent_bar = tk.Frame(card, bg=color, height=4)
        accent_bar.pack(fill=tk.X)
        
        # Content area
        content_frame = tk.Frame(card, bg='white')
        content_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Task title with status indicator
        status_prefix = "✅" if task['completed'] else "⭕"
        title_text = f"{status_prefix} {task['task']}"
        if task['completed']:
            title_font = ('Segoe UI', 12, 'overstrike')
            title_color = '#6c757d'
        else:
            title_font = ('Segoe UI', 12, 'bold')
            title_color = '#2c3e50'
            
        title_label = tk.Label(content_frame, text=title_text, 
                              font=title_font, 
                              bg='white', fg=title_color,
                              wraplength=500, justify=tk.LEFT, anchor='w')
        title_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Task date with icon
        date_label = tk.Label(content_frame, text=f"📅 {task['created']}", 
                             font=('Segoe UI', 9), 
                             bg='white', fg='#6c757d')
        date_label.pack(anchor=tk.W, pady=(0, 12))
        
        # Action buttons with modern styling
        button_frame = tk.Frame(content_frame, bg='white')
        button_frame.pack(fill=tk.X)
        
        # Toggle complete button
        if task['completed']:
            toggle_btn = tk.Button(button_frame, text="Reopen", 
                                 command=lambda: self.toggle_task_complete(task),
                                 bg='#17a2b8', fg='white', font=('Segoe UI', 9, 'bold'),
                                 relief=tk.FLAT, bd=0, padx=12, pady=6,
                                 cursor='hand2', activebackground='#138496')
        else:
            toggle_btn = tk.Button(button_frame, text="Complete", 
                                 command=lambda: self.toggle_task_complete(task),
                                 bg='#27ae60', fg='white', font=('Segoe UI', 9, 'bold'),
                                 relief=tk.FLAT, bd=0, padx=12, pady=6,
                                 cursor='hand2', activebackground='#229954')
        toggle_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Edit button
        edit_btn = tk.Button(button_frame, text="Edit", 
                           command=lambda: self.edit_task(task),
                           bg='#f39c12', fg='white', font=('Segoe UI', 9, 'bold'),
                           relief=tk.FLAT, bd=0, padx=12, pady=6,
                           cursor='hand2', activebackground='#e67e22')
        edit_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Delete button
        delete_btn = tk.Button(button_frame, text="×", 
                             command=lambda: self.delete_task(task),
                             bg='#dc3545', fg='white', font=('Segoe UI', 12, 'bold'),
                             relief=tk.FLAT, bd=0, width=3, height=1,
                             cursor='hand2', activebackground='#c82333')
        delete_btn.pack(side=tk.RIGHT)
    
    def show_add_dialog(self):
        """Show a modern dialog for adding new tasks"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Task")
        dialog.geometry("450x280")
        dialog.configure(bg='#ecf0f1')
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set dialog icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "todo-icon.ico")
            if os.path.exists(icon_path):
                dialog.iconbitmap(icon_path)
            elif os.path.exists("todo-icon.ico"):
                dialog.iconbitmap("todo-icon.ico")
        except Exception:
            pass
        
        # Center the dialog relative to parent window
        dialog.update_idletasks()
        parent_x = self.root.winfo_x()
        parent_y = self.root.winfo_y()
        parent_width = self.root.winfo_width()
        parent_height = self.root.winfo_height()
        x = parent_x + (parent_width // 2) - (450 // 2)
        y = parent_y + (parent_height // 2) - (250 // 2)
        dialog.geometry(f"450x250+{x}+{y}")
        
        # Main container
        main_frame = tk.Frame(dialog, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="➕ Create New Task", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Input section
        input_label = tk.Label(main_frame, text="Task Description:", 
                              font=('Segoe UI', 11, 'bold'), 
                              bg='#ecf0f1', fg='#34495e')
        input_label.pack(anchor=tk.W, pady=(0, 5))
        
        task_entry = tk.Entry(main_frame, font=('Segoe UI', 12), 
                             width=40, relief=tk.FLAT, bd=8,
                             bg='white', fg='#2c3e50')
        task_entry.pack(fill=tk.X, pady=(0, 20))
        task_entry.focus_set()
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#ecf0f1')
        button_frame.pack(fill=tk.X)
        
        def add_task():
            task = task_entry.get().strip()
            if task:
                todo_item = {
                    'id': len(self.todos) + 1,
                    'task': task,
                    'completed': False,
                    'created': datetime.now().strftime('%b %d, %Y - %I:%M%p')
                }
                self.todos.append(todo_item)
                self.refresh_todo_list()
                self.save_todos()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter a task description!")
        
        def cancel():
            dialog.destroy()
        
        # Buttons
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                              command=cancel,
                              bg='#95a5a6', fg='white', 
                              font=('Segoe UI', 11, 'bold'),
                              relief=tk.FLAT, bd=0, padx=25, pady=12,
                              cursor='hand2')
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        add_btn = tk.Button(button_frame, text="Add Task", 
                           command=add_task,
                           bg='#3498db', fg='white', 
                           font=('Segoe UI', 11, 'bold'),
                           relief=tk.FLAT, bd=0, padx=25, pady=12,
                           cursor='hand2')
        add_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key to add task
        task_entry.bind('<Return>', lambda e: add_task())
        dialog.bind('<Escape>', lambda e: cancel())
    
    def add_todo(self):
        # This method is now replaced by show_add_dialog
        self.show_add_dialog()
    
    def refresh_todo_list(self):
        """Refresh all task cards"""
        # Clear existing cards
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        
        # Sort todos: incomplete first, then completed
        sorted_todos = sorted(self.todos, key=lambda x: (x['completed'], x['created']))
        
        # Add todos as cards
        for todo in sorted_todos:
            self.add_task_card(todo)
        
        self.update_stats()
    
    def update_stats(self):
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo['completed'])
        pending = total - completed
        
        # Update task count badge
        if hasattr(self, 'count_label'):
            self.count_label.config(text=str(total))
        
        if total == 0:
            stats_text = "No tasks yet - click 'New Task' to get started! 🚀 | © 2025 Gwen Balajediong"
        else:
            completion_rate = (completed / total) * 100 if total > 0 else 0
            stats_text = f"📊 {total} total tasks | ✅ {completed} completed | ⏳ {pending} pending | {completion_rate:.0f}% done | © 2025 Gwen Balajediong"
        
        self.stats_label.config(text=stats_text)
    
    def toggle_task_complete(self, task):
        """Toggle task completion status"""
        task['completed'] = not task['completed']
        self.refresh_todo_list()
        self.save_todos()
    
    def edit_task(self, task):
        """Edit a task (using existing edit dialog)"""
        # Use the existing edit dialog by temporarily setting selection
        self.selected_task = task
        self.edit_todo()
    
    def delete_task(self, task):
        """Delete a task"""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this task?\n\n'{task['task']}'"):
            self.todos.remove(task)
            self.refresh_todo_list()
            self.save_todos()
    
    def get_selected_todo(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task!")
            return None
        
        todo_id = int(selection[0])
        return next((todo for todo in self.todos if todo['id'] == todo_id), None)
    
    def toggle_complete(self):
        todo = self.get_selected_todo()
        if todo:
            todo['completed'] = not todo['completed']
            self.refresh_todo_list()
            self.save_todos()
    
    def edit_todo(self):
        # Check if we have a selected task from card click
        if hasattr(self, 'selected_task') and self.selected_task:
            todo = self.selected_task
            # Clear the selected task reference
            del self.selected_task
        else:
            messagebox.showwarning("Warning", "No task selected for editing!")
            return
        
        # Create modern edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task")
        dialog.geometry("450x280")
        dialog.configure(bg='#ecf0f1')
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set dialog icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "todo-icon.ico")
            if os.path.exists(icon_path):
                dialog.iconbitmap(icon_path)
            elif os.path.exists("todo-icon.ico"):
                dialog.iconbitmap("todo-icon.ico")
        except Exception:
            pass
        
        # Center the dialog relative to parent window
        dialog.update_idletasks()
        parent_x = self.root.winfo_x()
        parent_y = self.root.winfo_y()
        parent_width = self.root.winfo_width()
        parent_height = self.root.winfo_height()
        x = parent_x + (parent_width // 2) - (450 // 2)
        y = parent_y + (parent_height // 2) - (280 // 2)
        dialog.geometry(f"450x250+{x}+{y}")

        # Main container
        main_frame = tk.Frame(dialog, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="✏️ Edit Task", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Input section
        input_label = tk.Label(main_frame, text="Task Description:", 
                              font=('Segoe UI', 11, 'bold'), 
                              bg='#ecf0f1', fg='#34495e')
        input_label.pack(anchor=tk.W, pady=(0, 5))
        
        task_entry = tk.Entry(main_frame, font=('Segoe UI', 12), 
                             width=40, relief=tk.FLAT, bd=8,
                             bg='white', fg='#2c3e50')
        task_entry.pack(fill=tk.X, pady=(0, 20))
        task_entry.insert(0, todo['task'])
        task_entry.focus_set()
        task_entry.select_range(0, tk.END)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#ecf0f1')
        button_frame.pack(fill=tk.X)
        
        def save_changes():
            new_task = task_entry.get().strip()
            if new_task:
                todo['task'] = new_task
                self.refresh_todo_list()
                self.save_todos()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter a task description!")
        
        def cancel():
            dialog.destroy()
        
        # Buttons
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                              command=cancel,
                              bg='#95a5a6', fg='white', 
                              font=('Segoe UI', 11, 'bold'),
                              relief=tk.FLAT, bd=0, padx=25, pady=12,
                              cursor='hand2')
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        save_btn = tk.Button(button_frame, text="Save Changes", 
                           command=save_changes,
                           bg='#f39c12', fg='white', 
                           font=('Segoe UI', 11, 'bold'),
                           relief=tk.FLAT, bd=0, padx=25, pady=12,
                           cursor='hand2')
        save_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key to save changes
        task_entry.bind('<Return>', lambda e: save_changes())
        dialog.bind('<Escape>', lambda e: cancel())
    
    def delete_todo(self):
        todo = self.get_selected_todo()
        if todo:
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this task?\n\n'{todo['task']}'"):
                self.todos.remove(todo)
                self.refresh_todo_list()
                self.save_todos()
    
    def load_todos(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_todos(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save todos: {str(e)}")
    
    def on_closing(self):
        self.save_todos()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()