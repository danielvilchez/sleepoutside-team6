import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import traceback


class DirectoryTreeGenerator:
    """Main class for directory tree generation with GUI."""

    def __init__(self, root):
        self.root = root
        self.root.title("Directory Tree Generator")
        self.root.geometry("1000x700")

        # Configuration Variables
        self.selected_directory = tk.StringVar(value=os.getcwd())
        self.max_depth = tk.IntVar(value=5)
        self.max_folders = tk.IntVar(value=10)
        self.max_files = tk.IntVar(value=20)
        self.max_name_length = tk.IntVar(value=50)
        self.ignored_dirs = []
        self.current_font_size = 10

        # Statistics
        self.total_folders = 0
        self.total_files = 0

        # Vertical Selection
        self.vertical_selection_mode = False
        self.vertical_start_pos = None

        # Colors for depth levels
        self.level_colors = [
            '#1a4d2e',  # Level 0 - Dark Green
            '#2c5f8d',  # Level 1 - Dark Blue
            '#6b4c9a',  # Level 2 - Dark Purple
            '#8b4513',  # Level 3 - Dark Brown
            '#b8860b',  # Level 4 - Dark Goldenrod
            '#2f4f4f',  # Level 5 - Dark Slate Gray
        ]

        # Setup Theme
        self.setup_dark_theme()

        # Create Interface
        try:
            self.create_widgets()
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Startup Error", f"Interface initialization failed:\n{e}")
            raise

    def setup_dark_theme(self):
        """Sets up the dark theme colors."""
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#e0e0e0',
            'input_bg': '#2d2d2d',
            'button_bg': '#3a3a3a',
            'button_hover': '#4a4a4a',
            'accent': '#007acc',
            'border': '#404040'
        }

        try:
            self.root.configure(bg=self.colors['bg'])
        except Exception:
            pass

        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('Dark.TFrame', background=self.colors['bg'])
        style.configure('Dark.TLabel', background=self.colors['bg'], foreground=self.colors['fg'], font=('Segoe UI', 9))
        style.configure('Dark.TLabelframe', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('Dark.TLabelframe.Label', background=self.colors['bg'], foreground=self.colors['fg'])

    def create_widgets(self):
        """Creates all UI widgets."""
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # MAIN FRAME
        main_frame = ttk.Frame(self.root, style='Dark.TFrame', padding=10)
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Status Bar (Fixed at bottom)
        self.create_status_bar(self.root)

        # Sections
        self.create_directory_section(main_frame)
        self.create_config_section(main_frame)
        self.create_ignored_dirs_section(main_frame)
        
        # New: Toolbar containing Actions AND Zoom
        self.create_toolbar(main_frame)
        
        # Tree Display (Expanded)
        self.create_tree_display(main_frame)

    def create_directory_section(self, parent):
        """Directory selection section."""
        dir_frame = ttk.Frame(parent, style='Dark.TFrame')
        dir_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(dir_frame, text="Directory:", style='Dark.TLabel', width=10).pack(side=tk.LEFT)

        dir_entry = tk.Entry(dir_frame, textvariable=self.selected_directory,
                             bg=self.colors['input_bg'], fg=self.colors['fg'],
                             insertbackground=self.colors['fg'], relief='flat', 
                             borderwidth=1, font=('Segoe UI', 9))
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(dir_frame, text="Browse", command=self.browse_directory,
                  bg=self.colors['button_bg'], fg=self.colors['fg'],
                  relief='flat', cursor='hand2', padx=10, pady=2, 
                  font=('Segoe UI', 9)).pack(side=tk.LEFT)

    def create_config_section(self, parent):
        """Configuration section - Single Line."""
        config_frame = ttk.LabelFrame(parent, text="Settings", style='Dark.TFrame')
        config_frame.pack(fill=tk.X, pady=(0, 5))

        inner = ttk.Frame(config_frame, style='Dark.TFrame')
        inner.pack(fill=tk.X, padx=5, pady=5)

        configs = [
            ("Max Depth:", self.max_depth, 1, 20),
            ("Max Folders:", self.max_folders, 1, 100),
            ("Max Files:", self.max_files, 1, 200),
            ("Name Length:", self.max_name_length, 10, 200)
        ]

        for i, (label_text, var, min_val, max_val) in enumerate(configs):
            frame = ttk.Frame(inner, style='Dark.TFrame')
            frame.grid(row=0, column=i, sticky='ew', padx=10) 
            
            ttk.Label(frame, text=label_text, style='Dark.TLabel').pack(side=tk.LEFT, padx=(0, 5))
            
            tk.Spinbox(frame, from_=min_val, to=max_val, textvariable=var, width=5,
                       bg=self.colors['input_bg'], fg=self.colors['fg'],
                       buttonbackground=self.colors['button_bg'],
                       relief='flat', borderwidth=1, font=('Segoe UI', 9)).pack(side=tk.LEFT)

            inner.columnconfigure(i, weight=1)

    def create_ignored_dirs_section(self, parent):
        """Ignored directories section."""
        ignored_frame = ttk.LabelFrame(parent, text="Ignored Directories", style='Dark.TFrame')
        ignored_frame.pack(fill=tk.X, pady=(0, 5))

        input_frame = ttk.Frame(ignored_frame, style='Dark.TFrame')
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.ignored_entry = tk.Entry(input_frame, bg=self.colors['input_bg'],
                                      fg=self.colors['fg'], insertbackground=self.colors['fg'],
                                      relief='flat', borderwidth=1, font=('Segoe UI', 9))
        self.ignored_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        tk.Button(input_frame, text="Add", command=self.add_ignored_dir,
                  bg=self.colors['button_bg'], fg=self.colors['fg'],
                  relief='flat', cursor='hand2', padx=10, pady=2, 
                  font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(input_frame, text="Browse", command=self.browse_ignored_dir,
                  bg=self.colors['button_bg'], fg=self.colors['fg'],
                  relief='flat', cursor='hand2', padx=10, pady=2,
                  font=('Segoe UI', 9)).pack(side=tk.LEFT)

        list_frame = ttk.Frame(ignored_frame, style='Dark.TFrame')
        list_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        scrollbar = tk.Scrollbar(list_frame, bg=self.colors['bg'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.ignored_listbox = tk.Listbox(list_frame, bg=self.colors['input_bg'],
                                          fg=self.colors['fg'], selectbackground=self.colors['accent'],
                                          relief='flat', borderwidth=1, height=3,
                                          yscrollcommand=scrollbar.set, font=('Segoe UI', 9))
        self.ignored_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scrollbar.config(command=self.ignored_listbox.yview)

        tk.Button(ignored_frame, text="Remove Selected", command=self.remove_ignored_dir,
                  bg=self.colors['button_bg'], fg=self.colors['fg'],
                  relief='flat', cursor='hand2', padx=10, pady=2,
                  font=('Segoe UI', 8)).pack(pady=(0, 5))

        default_ignored = [
            '.git', 'node_modules', '__pycache__', '.venv', 'venv', '.idea',
            'dist', 'build', '.next', '.nuxt', 'out', 'target', 'bin', 'obj',
            '.gradle', '.maven', '.dart_tool', 'vendor', 'coverage', '.pytest_cache',
            '.mypy_cache', '.tox', '.sass-cache', '.parcel-cache', '.cache',
            'logs', 'temp', 'tmp', '.DS_Store', 'Thumbs.db', '.vscode', '.vs'
        ]

        for dir_name in default_ignored:
            self.ignored_dirs.append(dir_name)
            self.ignored_listbox.insert(tk.END, dir_name)

    def create_toolbar(self, parent):
        """
        Creates a single horizontal toolbar for Actions and Zoom controls.
        """
        toolbar_frame = ttk.Frame(parent, style='Dark.TFrame')
        toolbar_frame.pack(fill=tk.X, pady=(5, 5))

        # --- Left Side: Action Buttons ---
        
        # Compact buttons (smaller pady/padx)
        tk.Button(toolbar_frame, text="Generate Tree", command=self.generate_tree,
                  bg=self.colors['accent'], fg='white', relief='flat', cursor='hand2',
                  padx=10, pady=4, font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(toolbar_frame, text="Copy to Clipboard", command=self.copy_to_clipboard,
                  bg=self.colors['button_bg'], fg=self.colors['fg'],
                  relief='flat', cursor='hand2', padx=10, pady=4,
                  font=('Segoe UI', 9)).pack(side=tk.LEFT)

        # --- Spacer to push zoom to the right ---
        # If you want Zoom immediately next to Copy, remove this Frame.
        # But for UI balance, pushing it to the right is usually cleaner.
        spacer = ttk.Frame(toolbar_frame, style='Dark.TFrame')
        spacer.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # --- Right Side: Zoom Controls ---

        ttk.Label(toolbar_frame, text="Zoom:", style='Dark.TLabel').pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(toolbar_frame, text="−", command=self.zoom_out,
                  bg=self.colors['button_bg'], fg=self.colors['fg'],
                  relief='flat', cursor='hand2', width=3, pady=1,
                  font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 2))

        tk.Button(toolbar_frame, text="+", command=self.zoom_in,
                  bg=self.colors['button_bg'], fg=self.colors['fg'],
                  relief='flat', cursor='hand2', width=3, pady=1,
                  font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT)

    def create_tree_display(self, parent):
        """Tree display area - No LabelFrame title, maximized space."""
        # Using a simple Frame instead of LabelFrame to remove the text/border title
        display_frame = ttk.Frame(parent, style='Dark.TFrame')
        display_frame.pack(fill=tk.BOTH, expand=True)

        # Text area container
        text_container = ttk.Frame(display_frame, style='Dark.TFrame')
        text_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        text_container.grid_rowconfigure(0, weight=1)
        text_container.grid_columnconfigure(0, weight=1)

        self.tree_display = tk.Text(text_container, bg=self.colors['input_bg'],
                                    fg=self.colors['fg'], insertbackground=self.colors['fg'],
                                    relief='flat', borderwidth=1,
                                    font=('Consolas', self.current_font_size),
                                    wrap=tk.NONE, undo=True, maxundo=-1)

        v_scrollbar = tk.Scrollbar(text_container, orient=tk.VERTICAL, command=self.tree_display.yview)
        h_scrollbar = tk.Scrollbar(text_container, orient=tk.HORIZONTAL, command=self.tree_display.xview)
        self.tree_display.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.tree_display.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        # Bindings
        self.tree_display.bind('<Control-z>', self.safe_undo)
        self.tree_display.bind('<Control-y>', self.safe_redo)
        self.tree_display.bind('<KeyPress-Alt_L>', self.start_vertical_selection)
        self.tree_display.bind('<KeyRelease-Alt_L>', self.end_vertical_selection)
        self.tree_display.bind('<Button-1>', self.handle_click)
        self.tree_display.bind('<B1-Motion>', self.handle_drag)
        self.tree_display.bind('<<Modified>>', self.update_status)

        self.setup_text_tags()

    def safe_undo(self, event=None):
        try:
            self.tree_display.edit_undo()
        except tk.TclError:
            pass
        return "break"

    def safe_redo(self, event=None):
        try:
            self.tree_display.edit_redo()
        except tk.TclError:
            pass
        return "break"

    def create_status_bar(self, parent):
        """Status bar."""
        status_frame = tk.Frame(parent, bg=self.colors['input_bg'], relief='flat', borderwidth=1)

        if parent == self.root:
            try:
                status_frame.grid(row=1, column=0, sticky='ew', pady=(3, 0))
            except Exception:
                status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(3, 0))
        else:
            status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(3, 0))

        # Status Labels
        self.status_folders = tk.Label(status_frame, text="Folders: 0",
                                       bg=self.colors['input_bg'], fg=self.colors['fg'],
                                       font=('Segoe UI', 9), anchor='w', padx=10)
        self.status_folders.pack(side=tk.LEFT)

        tk.Label(status_frame, text="|", bg=self.colors['input_bg'],
                 fg=self.colors['border'], font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)

        self.status_files = tk.Label(status_frame, text="Files: 0",
                                     bg=self.colors['input_bg'], fg=self.colors['fg'],
                                     font=('Segoe UI', 9), anchor='w', padx=10)
        self.status_files.pack(side=tk.LEFT)

        tk.Label(status_frame, text="|", bg=self.colors['input_bg'],
                 fg=self.colors['border'], font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)

        self.status_lines = tk.Label(status_frame, text="Lines: 0",
                                     bg=self.colors['input_bg'], fg=self.colors['fg'],
                                     font=('Segoe UI', 9), anchor='w', padx=10)
        self.status_lines.pack(side=tk.LEFT)

        tk.Label(status_frame, text="|", bg=self.colors['input_bg'],
                 fg=self.colors['border'], font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)

        self.status_chars = tk.Label(status_frame, text="Chars: 0",
                                     bg=self.colors['input_bg'], fg=self.colors['fg'],
                                     font=('Segoe UI', 9), anchor='w', padx=10)
        self.status_chars.pack(side=tk.LEFT)

    def update_status(self, event=None):
        try:
            if not hasattr(self, 'status_folders'):
                return

            content = self.tree_display.get(1.0, tk.END)
            lines = content.count('\n')
            chars = len(content) - 1

            self.status_folders.config(text=f"Folders: {self.total_folders}")
            self.status_files.config(text=f"Files: {self.total_files}")
            self.status_lines.config(text=f"Lines: {lines}")
            self.status_chars.config(text=f"Chars: {chars}")

            try:
                self.tree_display.edit_modified(False)
            except Exception:
                pass
        except Exception:
            pass

    def start_vertical_selection(self, event):
        self.vertical_selection_mode = True
        self.vertical_start_pos = self.tree_display.index(tk.INSERT)

    def end_vertical_selection(self, event):
        self.vertical_selection_mode = False
        self.vertical_start_pos = None

    def handle_click(self, event):
        if self.vertical_selection_mode:
            self.vertical_start_pos = self.tree_display.index(f"@{event.x},{event.y}")
            return "break"

    def handle_drag(self, event):
        if self.vertical_selection_mode and self.vertical_start_pos:
            current_pos = self.tree_display.index(f"@{event.x},{event.y}")
            self.select_vertical_block(self.vertical_start_pos, current_pos)
            return "break"

    def select_vertical_block(self, start, end):
        try:
            start_line, start_col = map(int, start.split('.'))
            end_line, end_col = map(int, end.split('.'))

            if start_line > end_line:
                start_line, end_line = end_line, start_line
            if start_col > end_col:
                start_col, end_col = end_col, start_col

            self.tree_display.tag_remove('sel', '1.0', tk.END)
            for line in range(start_line, end_line + 1):
                sel_start = f"{line}.{start_col}"
                sel_end = f"{line}.{end_col}"
                self.tree_display.tag_add('sel', sel_start, sel_end)
        except Exception:
            pass

    def setup_text_tags(self):
        for i, color in enumerate(self.level_colors):
            self.tree_display.tag_configure(f'folder_level_{i}',
                                            background=color, foreground='white',
                                            font=('Consolas', self.current_font_size, 'bold'))
            self.tree_display.tag_configure(f'line_level_{i}',
                                            foreground=color,
                                            font=('Consolas', self.current_font_size, 'bold'))
        self.tree_display.tag_configure('file', foreground=self.colors['fg'])

    def zoom_in(self):
        if self.current_font_size < 20:
            self.current_font_size += 1
            self.update_font_size()

    def zoom_out(self):
        if self.current_font_size > 6:
            self.current_font_size -= 1
            self.update_font_size()

    def update_font_size(self):
        self.tree_display.config(font=('Consolas', self.current_font_size))
        for i in range(len(self.level_colors)):
            self.tree_display.tag_configure(f'folder_level_{i}',
                                            font=('Consolas', self.current_font_size, 'bold'))
            self.tree_display.tag_configure(f'line_level_{i}',
                                            font=('Consolas', self.current_font_size, 'bold'))

    def browse_directory(self):
        directory = filedialog.askdirectory(title="Select Directory")
        if directory:
            self.selected_directory.set(directory)

    def browse_ignored_dir(self):
        directory = filedialog.askdirectory(title="Select Directory to Ignore")
        if directory:
            dir_name = os.path.basename(directory)
            self.ignored_entry.delete(0, tk.END)
            self.ignored_entry.insert(0, dir_name)

    def add_ignored_dir(self):
        dir_name = self.ignored_entry.get().strip()
        if dir_name and dir_name not in self.ignored_dirs:
            self.ignored_dirs.append(dir_name)
            self.ignored_listbox.insert(tk.END, dir_name)
            self.ignored_entry.delete(0, tk.END)

    def remove_ignored_dir(self):
        selection = self.ignored_listbox.curselection()
        if selection:
            index = selection[0]
            dir_name = self.ignored_listbox.get(index)
            self.ignored_dirs.remove(dir_name)
            self.ignored_listbox.delete(index)

    def truncate_name(self, name: str) -> str:
        max_len = self.max_name_length.get()
        return name[:max_len - 3] + "..." if len(name) > max_len else name

    def insert_colored_text(self, text: str, tag: str):
        self.tree_display.insert(tk.END, text, tag)

    def generate_tree_structure(self, path: str, prefix_marks: list = None, current_depth: int = 0):
        """
        Generates tree structure.
        """
        if prefix_marks is None:
            prefix_marks = []

        if current_depth > self.max_depth.get():
            return

        level_idx = current_depth % len(self.level_colors)

        try:
            entries = []
            with os.scandir(path) as it:
                for entry in it:
                    entries.append(entry)

            folders = [e for e in entries if e.is_dir()]
            files = [e for e in entries if e.is_file()]

            folders = folders[:self.max_folders.get()]
            files = files[:self.max_files.get()]

            folders.sort(key=lambda x: x.name.lower())
            files.sort(key=lambda x: x.name.lower())

            self.total_folders += len(folders)
            self.total_files += len(files)

            def insert_prefix(marks):
                for j, mark in enumerate(marks):
                    col_level = (j + 1) % len(self.level_colors)
                    text = "│   " if mark else "    "
                    self.insert_colored_text(text, f'line_level_{col_level}')

            # Process Folders
            for i, folder in enumerate(folders):
                is_last_folder = (i == len(folders) - 1) and len(files) == 0
                connector = "└── " if is_last_folder else "├── "

                insert_prefix(prefix_marks)
                self.insert_colored_text(connector, f'line_level_{level_idx}')

                folder_name = self.truncate_name(folder.name) + "/"
                self.insert_colored_text(folder_name, f'folder_level_{level_idx}')
                self.insert_colored_text("\n", 'file')

                child_marks = prefix_marks + ([not is_last_folder])

                # Ignored Folder
                if folder.name in self.ignored_dirs:
                    insert_prefix(child_marks)
                    next_level_idx = (current_depth + 1) % len(self.level_colors)
                    self.insert_colored_text("└── [...]\n", f'line_level_{next_level_idx}')
                    continue

                try:
                    self.generate_tree_structure(
                        folder.path,
                        child_marks,
                        current_depth + 1
                    )
                except PermissionError:
                    next_level_idx = (current_depth + 1) % len(self.level_colors)
                    insert_prefix(child_marks)
                    self.insert_colored_text("[Access Denied]\n", 'file')

            # Process Files
            for i, file in enumerate(files):
                is_last = i == len(files) - 1
                connector = "└── " if is_last else "├── "

                insert_prefix(prefix_marks)
                self.insert_colored_text(connector, f'line_level_{level_idx}')

                file_name = self.truncate_name(file.name)
                self.insert_colored_text(file_name + "\n", 'file')

        except PermissionError:
            insert_prefix(prefix_marks)
            self.insert_colored_text(f"[Access Denied]\n", 'file')
        except Exception as e:
            insert_prefix(prefix_marks)
            self.insert_colored_text(f"[Error: {str(e)}]\n", 'file')

    def generate_tree(self):
        """Generates the directory tree."""
        directory = self.selected_directory.get()

        if not directory or not os.path.exists(directory) or not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid Directory.")
            return

        try:
            self.tree_display.delete(1.0, tk.END)
        except Exception:
            pass
        self.total_folders = 0
        self.total_files = 0

        try:
            header = f"Tree generated for: {directory}\n\n"
            self.insert_colored_text(header, 'file')

            root_name = os.path.basename(directory) + "/\n"
            self.insert_colored_text(root_name, 'folder_level_0')
            self.total_folders += 1

            self.generate_tree_structure(directory, [], 1)
            self.update_status()

        except Exception as e:
            messagebox.showerror("Error", f"Tree generation failed: {str(e)}")

    def copy_to_clipboard(self):
        """Copies content to clipboard."""
        try:
            content = self.tree_display.get(1.0, tk.END).strip()
        except Exception:
            content = ''

        if not content:
            messagebox.showwarning("Warning", "Nothing to copy.")
            return

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            # messagebox.showinfo("Success", "Copied to clipboard!")
        except Exception:
            print("Failed to copy to clipboard.")


def main():
    try:
        root = tk.Tk()
        app = DirectoryTreeGenerator(root)
        root.mainloop()
    except Exception as e:
        try:
            tk.Tk().withdraw()
            messagebox.showerror("Fatal Error", f"Application failed: {e}")
        except Exception:
            print("Fatal error on startup:", e)
        raise


if __name__ == "__main__":
    main()