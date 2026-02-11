import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import subprocess
import os
import sys
import json
import threading
import time
from datetime import datetime
from pathlib import Path

class Translator:
    """Klasa do zarządzania tłumaczeniami"""
    
    def __init__(self, app_folder):
        self.app_folder = app_folder
        self.config_file = os.path.join(app_folder, "miniconda_navigator_config.json")
        self.language = "en"  # Domyślny język
        self.default_folder = app_folder  # Domyślny folder skryptów
        self.translations = {}
        self.load_config()
        self.load_languages()
    
    def load_config(self):
        """Załaduj konfigurację z pliku"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'language' in config:
                        self.language = config['language']
                    if 'default_folder' in config and os.path.exists(config['default_folder']):
                        self.default_folder = config['default_folder']
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def save_config(self):
        """Zapisz konfigurację do pliku"""
        try:
            config = {
                'language': self.language,
                'default_folder': self.default_folder,
                'last_used': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def set_default_folder(self, folder_path):
        """Ustaw domyślny folder i zapisz do konfiguracji"""
        if os.path.exists(folder_path):
            self.default_folder = folder_path
            self.save_config()
            return True
        return False
    
    def load_languages(self):
        """Załaduj wszystkie dostępne języki"""
        self.languages = {}
        
        # Domyślne tłumaczenie angielskie (wbudowane)
        self.languages['en'] = self.get_default_english()
        
        # Szukaj plików językowych
        for file in os.listdir(self.app_folder):
            if file.startswith('lang_') and file.endswith('.json'):
                lang_code = file[5:-5]  # Wyciągnij kod języka
                try:
                    with open(os.path.join(self.app_folder, file), 'r', encoding='utf-8') as f:
                        self.languages[lang_code] = json.load(f)
                except Exception as e:
                    print(f"Error loading language {lang_code}: {e}")
        
        # Sprawdź czy wybrany język istnieje
        if self.language not in self.languages:
            self.language = "en"
        self.translations = self.languages[self.language]
    
    def get_default_english(self):
        """Zwróć domyślne tłumaczenie angielskie"""
        return {
            # Main window
            "window_title": "MiniConda Navigator v2.5",
            "status_ready": "Ready",
            "environment": "Environment",
            "language_label": "Language:",
            
            # Menu
            "menu_file": "File",
            "menu_open_terminal": "Open Terminal",
            "menu_open_folder": "Open Folder",
            "menu_exit": "Exit",
            
            "menu_environment": "Environment",
            "menu_activate": "Activate Environment",
            "menu_deactivate": "Deactivate",
            "menu_export": "Export Environment",
            "menu_import": "Import Environment",
            
            "menu_packages": "Packages",
            "menu_update_pip": "Update pip",
            "menu_update_conda": "Update conda",
            "menu_clean_cache": "Clear Cache",
            
            "menu_tools": "Tools",
            "menu_search_py": "Search all .py files",
            "menu_set_default": "Set default folder",
            "menu_manage_repos": "Manage repositories",
            
            # Environment section
            "env_section": "Environments",
            "env_name": "Name",
            "env_python": "Python",
            "btn_refresh": "Refresh",
            "btn_new": "New",
            "btn_terminal": "Terminal",
            "btn_delete": "Delete",
            
            # Package section
            "pkg_section": "Package Management",
            "pkg_install": "Install",
            "pkg_uninstall": "Uninstall",
            "pkg_search": "Search",
            
            # Script section
            "script_section": "Python Scripts",
            "folder_label": "Folder:",
            "btn_browse": "Browse",
            "btn_new_script": "New Script",
            "btn_edit": "Edit",
            "btn_run": "▶ Run",
            "btn_stop": "■ Stop",
            "btn_restart": "↻ Restart",
            
            # Terminal section
            "terminal_section": "Terminal & Commands",
            "output_tab": "Script Output",
            "commands_tab": "Environment Commands",
            "command_label": "Command:",
            "btn_execute": "Execute",
            "quick_label": "Quick:",
            
            # Dialogs
            "dialog_warning": "Warning",
            "dialog_info": "Info",
            "dialog_confirm": "Confirm",
            "dialog_error": "Error",
            
            # Status messages
            "status_loaded_envs": "Loaded {count} environments",
            "status_error_load_envs": "Error loading environments",
            "status_timeout": "Timeout loading environments",
            "status_env_selected": "Selected: {env}",
            "status_terminal_opened": "Terminal opened for: {env}",
            "status_activated": "Environment {env} activated",
            "status_deactivated": "Environment deactivated",
            "status_packages_loaded": "Loaded {count} packages",
            "status_scripts_found": "Found {count} scripts in: {folder}",
            "status_script_created": "Created: {filename}",
            "status_script_completed": "Script completed",
            "status_script_stopped": "Script stopped",
            "status_default_set": "Default folder set: {folder}",
            "status_command_executed": "Command executed: {cmd}",
            "status_command_error": "Command error: {cmd}",
            
            # Questions
            "question_use_pip": "Use pip?\n(Yes - pip, No - conda)",
            "question_uninstall_pkg": "Uninstall package '{pkg}'?",
            "question_uninstall_env": "Delete environment '{env}'?",
            
            # Input dialogs
            "input_install_pkg": "Enter package name for '{env}':",
            "input_search_pkg": "Enter package name:",
            "input_new_env": "Environment name:",
            "input_python_version": "Python version (e.g., 3.9):",
            "input_env_name": "Enter name for new environment:",
            
            # Errors
            "error_select_env": "Select environment",
            "error_select_pkg": "Select package",
            "error_select_script": "Select script to edit",
            "error_select_script_run": "Select script to run",
            "error_folder_not_exist": "Folder does not exist",
            "error_no_base_delete": "Cannot delete 'base' environment",
            
            # Quick commands
            "quick_pip_list": "pip list",
            "quick_conda_list": "conda list",
            "quick_pip_install": "pip install ",
            "quick_conda_install": "conda install ",
            "quick_pip_uninstall": "pip uninstall ",
            "quick_conda_update": "conda update --all",
            
            # Script template
            "script_comment_created": "Script created: {datetime}",
            "script_comment_env": "Environment: {env}",
            "script_main_function": "Main program function",
            "script_hello": "Hello from Python!",
            "script_running": "Script is running correctly!",
            
            # Command results
            "command_success": "✅ Command completed successfully",
            "command_error": "❌ Error (code: {code})",
            "command_exception": "🔥 Exception: {error}",
            
            # Other
            "packages_count": "Packages ({count}):",
            "folder_contents": "📂 Folder: {folder}",
            "no_py_files": "📭 No .py files in this folder",
            "check_folder": "Check: {folder}",
            "found_py_files": "✅ Found {count} .py files",
            "search_completed": "✅ Search completed",
            "search_error": "❌ Error: {error}",
        }
    
    def set_language(self, lang_code):
        """Ustaw język i zapisz do konfiguracji"""
        if lang_code in self.languages:
            self.language = lang_code
            self.translations = self.languages[lang_code]
            self.save_config()  # Zapisz wybór języka
            return True
        else:
            # Fallback to English
            self.language = "en"
            self.translations = self.languages['en']
            self.save_config()
            return False
    
    def get(self, key, **kwargs):
        """Pobierz przetłumaczone słowo/zdanie"""
        if key in self.translations:
            text = self.translations[key]
            if kwargs:
                try:
                    text = text.format(**kwargs)
                except:
                    pass
            return text
        else:
            # Fallback to English if key not found
            if key in self.languages['en']:
                text = self.languages['en'][key]
                if kwargs:
                    try:
                        text = text.format(**kwargs)
                    except:
                        pass
                return text
            return key  # Return key if not found anywhere

class MiniCondaNavigator:
    def __init__(self, root):
        self.root = root
        self.translator = Translator(os.path.dirname(os.path.abspath(__file__)))
        
        # Zmienne
        self.current_env = "base"
        self.current_script = None
        self.current_process = None
        self.script_folder = self.translator.default_folder
        self.env_terminals = {}  # Słownik dla terminali środowisk
        
        # Store UI widgets for translation updates
        self.ui_widgets = {}
        
        # UI
        self.setup_ui()
        
        # Inicjalizacja
        self.refresh_environments()
        self.refresh_scripts()
        
    def setup_ui(self):
        # Główny kontener
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # TOP BAR z wyborem języka
        top_bar = ttk.Frame(main_container)
        top_bar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(top_bar, text="🐍 MiniConda Navigator", 
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        # Wybór języka
        lang_frame = ttk.Frame(top_bar)
        lang_frame.pack(side=tk.RIGHT, padx=10)
        
        # Label dla języka
        lang_label = ttk.Label(lang_frame, text=self.translator.get("language_label"))
        lang_label.pack(side=tk.LEFT, padx=(0, 5))
        self.ui_widgets['lang_label'] = lang_label
        
        # Ustaw aktualny język z konfiguracji
        self.lang_var = tk.StringVar(value=self.translator.language)
        self.lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, 
                                      values=list(self.translator.languages.keys()),
                                      state="readonly", width=10)
        self.lang_combo.pack(side=tk.LEFT)
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        
        self.env_label = ttk.Label(top_bar, text=f"{self.translator.get('environment')}: base", 
                                  font=("Arial", 10))
        self.env_label.pack(side=tk.RIGHT, padx=10)
        self.ui_widgets['env_label'] = self.env_label
        
        # GŁÓWNA ZAWARTOŚĆ
        content = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        content.pack(fill=tk.BOTH, expand=True)
        
        # LEWA PANEL - ŚRODOWISKA + PAKIETY
        left_panel = ttk.PanedWindow(content, orient=tk.VERTICAL)
        content.add(left_panel, weight=1)
        
        # ŚRODOWISKA
        env_frame = ttk.LabelFrame(left_panel, text=self.translator.get("env_section"), padding=10)
        left_panel.add(env_frame, weight=1)
        self.ui_widgets['env_frame'] = env_frame
        
        # Treeview środowisk
        self.env_tree = ttk.Treeview(env_frame, columns=("python",), show="tree", height=10)
        self.env_tree.pack(fill=tk.BOTH, expand=True)
        
        self.env_tree.heading("#0", text=self.translator.get("env_name"))
        self.env_tree.heading("python", text=self.translator.get("env_python"))
        
        self.env_tree.bind("<<TreeviewSelect>>", self.on_env_select)
        self.env_tree.bind("<Double-1>", lambda e: self.open_env_terminal())
        
        # Przyciski środowisk
        env_btn_frame = ttk.Frame(env_frame)
        env_btn_frame.pack(fill=tk.X, pady=5)
        
        env_buttons = [
            ("btn_refresh_env", self.translator.get("btn_refresh"), self.refresh_environments, None),
            ("btn_new_env", self.translator.get("btn_new"), self.create_env, None),
            ("btn_terminal_env", self.translator.get("btn_terminal"), self.open_env_terminal, "Info.TButton"),
            ("btn_delete_env", self.translator.get("btn_delete"), self.delete_env, "Danger.TButton"),
        ]
        
        for widget_id, text, command, style in env_buttons:
            btn = ttk.Button(env_btn_frame, text=text, command=command, style=style)
            btn.pack(side=tk.LEFT, padx=2)
            self.ui_widgets[widget_id] = btn
        
        # PAKIETY
        pkg_frame = ttk.LabelFrame(left_panel, text=self.translator.get("pkg_section"), padding=10)
        left_panel.add(pkg_frame, weight=1)
        self.ui_widgets['pkg_frame'] = pkg_frame
        
        # Lista pakietów
        pkg_list_frame = ttk.Frame(pkg_frame)
        pkg_list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        pkg_scrollbar = ttk.Scrollbar(pkg_list_frame)
        pkg_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.pkg_listbox = tk.Listbox(
            pkg_list_frame,
            yscrollcommand=pkg_scrollbar.set,
            font=("Consolas", 9),
            height=8
        )
        self.pkg_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pkg_scrollbar.config(command=self.pkg_listbox.yview)
        
        # Przyciski pakietów
        pkg_btn_frame = ttk.Frame(pkg_frame)
        pkg_btn_frame.pack(fill=tk.X)
        
        pkg_buttons = [
            ("btn_refresh_pkg", self.translator.get("btn_refresh"), self.refresh_packages, None),
            ("btn_install_pkg", self.translator.get("pkg_install"), self.install_package, "Success.TButton"),
            ("btn_uninstall_pkg", self.translator.get("pkg_uninstall"), self.uninstall_package, "Danger.TButton"),
            ("btn_search_pkg", self.translator.get("pkg_search"), self.search_package, None),
        ]
        
        for widget_id, text, command, style in pkg_buttons:
            btn = ttk.Button(pkg_btn_frame, text=text, command=command, style=style)
            btn.pack(side=tk.LEFT, padx=2)
            self.ui_widgets[widget_id] = btn
        
        # PRAWA PANEL
        right_panel = ttk.PanedWindow(content, orient=tk.VERTICAL)
        content.add(right_panel, weight=2)
        
        # SKRYPTY
        script_frame = ttk.LabelFrame(right_panel, text=self.translator.get("script_section"), padding=10)
        right_panel.add(script_frame, weight=1)
        self.ui_widgets['script_frame'] = script_frame
        
        # Ścieżka i przeglądanie
        path_frame = ttk.Frame(script_frame)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        folder_label = ttk.Label(path_frame, text=self.translator.get("folder_label"))
        folder_label.pack(side=tk.LEFT)
        self.ui_widgets['folder_label'] = folder_label
        
         # Ustaw folder ze zmiennej script_folder (która jest z konfiguracji)
        self.path_var = tk.StringVar(value=self.script_folder)
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=60)
        path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(path_frame, text="🔄", 
                  command=self.refresh_scripts,
                  width=3).pack(side=tk.LEFT, padx=2)
        
        browse_btn = ttk.Button(path_frame, text=self.translator.get("btn_browse"), 
                  command=self.browse_folder)
        browse_btn.pack(side=tk.LEFT, padx=2)
        self.ui_widgets['browse_btn'] = browse_btn
        
        # Lista skryptów
        list_frame = ttk.Frame(script_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.script_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10),
            bg="#f0f0f0",
            selectbackground="#007acc",
            selectforeground="white",
            height=8
        )
        self.script_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.script_listbox.yview)
        
        self.script_listbox.bind("<<ListboxSelect>>", self.on_script_select)
        self.script_listbox.bind("<Double-Button-1>", lambda e: self.run_script())
        
        # Przyciski skryptów
        script_btn_frame = ttk.Frame(script_frame)
        script_btn_frame.pack(fill=tk.X, pady=5)
        
        new_script_btn = ttk.Button(script_btn_frame, text=self.translator.get("btn_new_script"), 
                  command=self.create_script)
        new_script_btn.pack(side=tk.LEFT, padx=2)
        self.ui_widgets['new_script_btn'] = new_script_btn
        
        edit_script_btn = ttk.Button(script_btn_frame, text=self.translator.get("btn_edit"), 
                  command=self.edit_script)
        edit_script_btn.pack(side=tk.LEFT, padx=2)
        self.ui_widgets['edit_script_btn'] = edit_script_btn
        
        # Przyciski uruchamiania
        run_frame = ttk.Frame(script_btn_frame)
        run_frame.pack(side=tk.RIGHT)
        
        self.run_btn = ttk.Button(run_frame, text=self.translator.get("btn_run"), 
                                 command=self.run_script,
                                 style="Success.TButton")
        self.run_btn.pack(side=tk.LEFT, padx=2)
        self.ui_widgets['run_btn'] = self.run_btn
        
        self.stop_btn = ttk.Button(run_frame, text=self.translator.get("btn_stop"), 
                                  command=self.stop_script,
                                  style="Danger.TButton",
                                  state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        self.ui_widgets['stop_btn'] = self.stop_btn
        
        restart_btn = ttk.Button(run_frame, text=self.translator.get("btn_restart"), 
                  command=self.restart_script)
        restart_btn.pack(side=tk.LEFT, padx=2)
        self.ui_widgets['restart_btn'] = restart_btn
        
        # TERMINAL I KOMENDY
        terminal_frame = ttk.LabelFrame(right_panel, text=self.translator.get("terminal_section"), padding=10)
        right_panel.add(terminal_frame, weight=1)
        self.ui_widgets['terminal_frame'] = terminal_frame
        
        # Zakładki
        self.terminal_notebook = ttk.Notebook(terminal_frame)
        self.terminal_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Zakładka 1: Output skryptów
        output_tab = ttk.Frame(self.terminal_notebook)
        self.terminal_notebook.add(output_tab, text=self.translator.get("output_tab"))
        self.ui_widgets['output_tab'] = output_tab
        
        self.output_text = scrolledtext.ScrolledText(
            output_tab,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#1e1e1e",
            fg="#ffffff",
            height=10
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Zakładka 2: Komendy Conda/Pip
        cmd_tab = ttk.Frame(self.terminal_notebook)
        self.terminal_notebook.add(cmd_tab, text=self.translator.get("commands_tab"))
        self.ui_widgets['cmd_tab'] = cmd_tab
        
        # Pole na komendy
        cmd_input_frame = ttk.Frame(cmd_tab)
        cmd_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        command_label = ttk.Label(cmd_input_frame, text=self.translator.get("command_label"))
        command_label.pack(side=tk.LEFT)
        self.ui_widgets['command_label'] = command_label
        
        self.cmd_var = tk.StringVar()
        self.cmd_entry = ttk.Entry(cmd_input_frame, textvariable=self.cmd_var, width=50)
        self.cmd_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.cmd_entry.bind("<Return>", lambda e: self.execute_env_command())
        
        execute_btn = ttk.Button(cmd_input_frame, text=self.translator.get("btn_execute"), 
                  command=self.execute_env_command,
                  style="Info.TButton")
        execute_btn.pack(side=tk.LEFT)
        self.ui_widgets['execute_btn'] = execute_btn
        
        # Szybkie komendy
        quick_cmd_frame = ttk.Frame(cmd_tab)
        quick_cmd_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        quick_label = ttk.Label(quick_cmd_frame, text=self.translator.get("quick_label"))
        quick_label.pack(side=tk.LEFT)
        self.ui_widgets['quick_label'] = quick_label
        
        quick_commands = [
            ("quick_pip_list", self.translator.get("quick_pip_list"), self.translator.get("quick_pip_list")),
            ("quick_conda_list", self.translator.get("quick_conda_list"), self.translator.get("quick_conda_list")),
            ("quick_pip_install", "pip install", self.translator.get("quick_pip_install")),
            ("quick_conda_install", "conda install", self.translator.get("quick_conda_install")),
            ("quick_pip_uninstall", "pip uninstall", self.translator.get("quick_pip_uninstall")),
            ("quick_conda_update", "conda update", self.translator.get("quick_conda_update"))
        ]
        
        for widget_id, text, cmd in quick_commands:
            btn = ttk.Button(quick_cmd_frame, text=text, 
                      command=lambda c=cmd: self.insert_quick_command(c),
                      width=15)
            btn.pack(side=tk.LEFT, padx=2)
            self.ui_widgets[widget_id] = btn
        
        # Output komend
        self.cmd_output = scrolledtext.ScrolledText(
            cmd_tab,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#1e1e1e",
            fg="#ffffff",
            height=8
        )
        self.cmd_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # STATUS BAR
        status_bar = ttk.Frame(main_container, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar(value=self.translator.get("status_ready"))
        status_label = ttk.Label(status_bar, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT, padx=5)
        self.ui_widgets['status_label'] = status_label
        
        # Styl przycisków
        style = ttk.Style()
        style.configure("Success.TButton", foreground="white", background="#28a745")
        style.configure("Danger.TButton", foreground="white", background="#dc3545")
        style.configure("Info.TButton", foreground="white", background="#17a2b8")
        style.configure("Warning.TButton", foreground="white", background="#ffc107")
        
        # Menu
        self.setup_menu()
    
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.translator.get("menu_file"), menu=file_menu)
        file_menu.add_command(label=self.translator.get("menu_open_terminal"), command=self.open_terminal)
        file_menu.add_command(label=self.translator.get("menu_open_folder"), command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label=self.translator.get("menu_exit"), command=self.root.quit)
        self.ui_widgets['file_menu'] = file_menu
        
        # Environment menu
        env_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.translator.get("menu_environment"), menu=env_menu)
        env_menu.add_command(label=self.translator.get("menu_activate"), command=self.activate_env)
        env_menu.add_command(label=self.translator.get("menu_deactivate"), command=self.deactivate_env)
        env_menu.add_separator()
        env_menu.add_command(label=self.translator.get("menu_export"), command=self.export_env)
        env_menu.add_command(label=self.translator.get("menu_import"), command=self.import_env)
        self.ui_widgets['env_menu'] = env_menu
        
        # Packages menu
        pkg_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.translator.get("menu_packages"), menu=pkg_menu)
        pkg_menu.add_command(label=self.translator.get("menu_update_pip"), command=self.update_pip)
        pkg_menu.add_command(label=self.translator.get("menu_update_conda"), command=self.update_conda)
        pkg_menu.add_separator()
        pkg_menu.add_command(label=self.translator.get("menu_clean_cache"), command=self.clean_cache)
        self.ui_widgets['pkg_menu'] = pkg_menu
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.translator.get("menu_tools"), menu=tools_menu)
        tools_menu.add_command(label=self.translator.get("menu_search_py"), command=self.search_all_py)
        tools_menu.add_command(label=self.translator.get("menu_set_default"), command=self.set_default_folder)
        tools_menu.add_command(label=self.translator.get("menu_manage_repos"), command=self.manage_repos)
        self.ui_widgets['tools_menu'] = tools_menu
        
        # Store menubar reference
        self.ui_widgets['menubar'] = menubar
    
    def change_language(self, event=None):
        """Zmień język interfejsu"""
        lang_code = self.lang_var.get()
        if self.translator.set_language(lang_code):
            self.update_ui_language()
    
    def update_ui_language(self):
        """Zaktualizuj wszystkie teksty w UI"""
        # Window title
        self.root.title(self.translator.get("window_title"))
        
        # Update all widgets
        self.update_widgets_text()
        
        # Update menu
        self.setup_menu()
        
        # Update treeview headings
        self.env_tree.heading("#0", text=self.translator.get("env_name"))
        self.env_tree.heading("python", text=self.translator.get("env_python"))
        
        # Update environment label
        self.env_label.config(text=f"{self.translator.get('environment')}: {self.current_env}")
        
        # Update status
        self.status_var.set(self.translator.get("status_ready"))
    
    def update_widgets_text(self):
        """Zaktualizuj teksty wszystkich widgetów"""
        # Labels
        self.ui_widgets['lang_label'].config(text=self.translator.get("language_label"))
        self.ui_widgets['folder_label'].config(text=self.translator.get("folder_label"))
        self.ui_widgets['command_label'].config(text=self.translator.get("command_label"))
        self.ui_widgets['quick_label'].config(text=self.translator.get("quick_label"))
        
        # Frame labels
        self.ui_widgets['env_frame'].config(text=self.translator.get("env_section"))
        self.ui_widgets['pkg_frame'].config(text=self.translator.get("pkg_section"))
        self.ui_widgets['script_frame'].config(text=self.translator.get("script_section"))
        self.ui_widgets['terminal_frame'].config(text=self.translator.get("terminal_section"))
        
        # Tab labels
        self.terminal_notebook.tab(0, text=self.translator.get("output_tab"))
        self.terminal_notebook.tab(1, text=self.translator.get("commands_tab"))
        
        # Environment buttons
        self.ui_widgets['btn_refresh_env'].config(text=self.translator.get("btn_refresh"))
        self.ui_widgets['btn_new_env'].config(text=self.translator.get("btn_new"))
        self.ui_widgets['btn_terminal_env'].config(text=self.translator.get("btn_terminal"))
        self.ui_widgets['btn_delete_env'].config(text=self.translator.get("btn_delete"))
        
        # Package buttons
        self.ui_widgets['btn_refresh_pkg'].config(text=self.translator.get("btn_refresh"))
        self.ui_widgets['btn_install_pkg'].config(text=self.translator.get("pkg_install"))
        self.ui_widgets['btn_uninstall_pkg'].config(text=self.translator.get("pkg_uninstall"))
        self.ui_widgets['btn_search_pkg'].config(text=self.translator.get("pkg_search"))
        
        # Script buttons
        self.ui_widgets['browse_btn'].config(text=self.translator.get("btn_browse"))
        self.ui_widgets['new_script_btn'].config(text=self.translator.get("btn_new_script"))
        self.ui_widgets['edit_script_btn'].config(text=self.translator.get("btn_edit"))
        self.ui_widgets['run_btn'].config(text=self.translator.get("btn_run"))
        self.ui_widgets['stop_btn'].config(text=self.translator.get("btn_stop"))
        self.ui_widgets['restart_btn'].config(text=self.translator.get("btn_restart"))
        
        # Command buttons
        self.ui_widgets['execute_btn'].config(text=self.translator.get("btn_execute"))
        
        # Quick command buttons
        self.ui_widgets['quick_pip_list'].config(text=self.translator.get("quick_pip_list"))
        self.ui_widgets['quick_conda_list'].config(text=self.translator.get("quick_conda_list"))
        self.ui_widgets['quick_pip_install'].config(text="pip install")
        self.ui_widgets['quick_conda_install'].config(text="conda install")
        self.ui_widgets['quick_pip_uninstall'].config(text="pip uninstall")
        self.ui_widgets['quick_conda_update'].config(text="conda update")
    
    # ========== FUNKCJE ŚRODOWISK ==========
    
    def refresh_environments(self):
        """Odśwież listę środowisk Conda"""
        for item in self.env_tree.get_children():
            self.env_tree.delete(item)
        
        try:
            result = subprocess.run(
                ["conda", "env", "list"],
                capture_output=True,
                text=True,
                shell=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        parts = line.split()
                        if len(parts) >= 1:
                            env_name = parts[0]
                            
                            if line.strip().startswith('*'):
                                env_name = f"{env_name} ★"
                                self.current_env = parts[0].replace('*', '')
                                self.env_label.config(text=f"{self.translator.get('environment')}: {self.current_env}")
                            
                            self.env_tree.insert("", "end", text=env_name, values=("Python",))
                
                count = len(self.env_tree.get_children())
                self.show_status(self.translator.get("status_loaded_envs", count=count))
                self.refresh_packages()  # Odśwież pakiety dla aktualnego środowiska
                
            else:
                self.show_status(self.translator.get("status_error_load_envs"), error=True)
                
        except subprocess.TimeoutExpired:
            self.show_status(self.translator.get("status_timeout"), error=True)
        except Exception as e:
            self.show_status(f"{self.translator.get('dialog_error')}: {str(e)}", error=True)
    
    def on_env_select(self, event):
        """Obsługa wyboru środowiska"""
        selection = self.env_tree.selection()
        if selection:
            env_name = self.env_tree.item(selection[0], "text")
            env_name = env_name.replace(" ★", "").strip()
            self.current_env = env_name
            self.env_label.config(text=f"{self.translator.get('environment')}: {env_name}")
            self.show_status(self.translator.get("status_env_selected", env=env_name))
            self.refresh_packages()
    
    def open_env_terminal(self):
        """Otwórz terminal dla wybranego środowiska"""
        if not self.current_env:
            messagebox.showwarning(
                self.translator.get("dialog_warning"),
                self.translator.get("error_select_env")
            )
            return
        
        try:
            cmd = f'start cmd /k "conda activate {self.current_env} && title Terminal: {self.current_env} && echo Environment: {self.current_env} && echo."'
            subprocess.Popen(cmd, shell=True)
            self.show_status(self.translator.get("status_terminal_opened", env=self.current_env))
            
            if self.current_env not in self.env_terminals:
                self.env_terminals[self.current_env] = []
                
        except Exception as e:
            self.show_status(f"{self.translator.get('dialog_error')}: {str(e)}", error=True)
    
    def activate_env(self):
        """Aktywuj wybrane środowisko w bieżącym terminalu"""
        if not self.current_env:
            return
        
        cmd = f"conda activate {self.current_env}"
        self.insert_quick_command(cmd)
        self.show_status(self.translator.get("status_activated", env=self.current_env))
    
    def deactivate_env(self):
        """Dezaktywuj środowisko"""
        self.insert_quick_command("conda deactivate")
        self.show_status(self.translator.get("status_deactivated"))
    
    def export_env(self):
        """Eksportuj środowisko do pliku YAML"""
        if not self.current_env:
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".yml",
            filetypes=[("YAML files", "*.yml"), ("All files", "*.*")],
            initialfile=f"{self.current_env}_environment.yml",
            title=self.translator.get("menu_export")
        )
        
        if filename:
            cmd = f'conda env export -n {self.current_env} > "{filename}"'
            self.execute_env_command_custom(cmd, f"Export environment {self.current_env}")
    
    def import_env(self):
        """Importuj środowisko z pliku YAML"""
        filename = filedialog.askopenfilename(
            filetypes=[("YAML files", "*.yml"), ("All files", "*.*")],
            title=self.translator.get("menu_import")
        )
        
        if filename:
            env_name = simpledialog.askstring(
                self.translator.get("dialog_confirm"),
                self.translator.get("input_env_name")
            )
            if env_name:
                cmd = f'conda env create -n {env_name} -f "{filename}"'
                self.execute_env_command_custom(cmd, f"Import environment from {filename}")
    
    # ========== FUNKCJE PAKIETÓW ==========
    
    def refresh_packages(self):
        """Odśwież listę pakietów w środowisku"""
        self.pkg_listbox.delete(0, tk.END)
        
        if not self.current_env:
            self.pkg_listbox.insert(tk.END, self.translator.get("error_select_env"))
            return
        
        try:
            conda_cmd = f"conda list -n {self.current_env}"
            result = subprocess.run(
                conda_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                pkg_count = 0
                
                for line in lines[2:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 3:
                            pkg_name = parts[0]
                            pkg_version = parts[1]
                            self.pkg_listbox.insert(tk.END, f"{pkg_name}=={pkg_version}")
                            pkg_count += 1
                
                self.pkg_listbox.insert(0, self.translator.get("packages_count", count=pkg_count))
                self.show_status(self.translator.get("status_packages_loaded", count=pkg_count))
            else:
                self.pkg_listbox.insert(tk.END, self.translator.get("status_error_load_envs"))
                
        except Exception as e:
            self.pkg_listbox.insert(tk.END, f"{self.translator.get('dialog_error')}: {str(e)}")
    
    def install_package(self):
        """Zainstaluj pakiet w środowisku"""
        if not self.current_env:
            messagebox.showwarning(
                self.translator.get("dialog_warning"),
                self.translator.get("error_select_env")
            )
            return
        
        package = simpledialog.askstring(
            self.translator.get("pkg_install"),
            self.translator.get("input_install_pkg", env=self.current_env)
        )
        if package:
            choice = messagebox.askyesno(
                self.translator.get("dialog_confirm"),
                self.translator.get("question_use_pip")
            )
            
            if choice:
                cmd = f"pip install {package}"
            else:
                cmd = f"conda install -n {self.current_env} {package} -y"
            
            self.execute_env_command_custom(cmd, f"Install package: {package}")
    
    def uninstall_package(self):
        """Odinstaluj pakiet ze środowiska"""
        if not self.current_env:
            messagebox.showwarning(
                self.translator.get("dialog_warning"),
                self.translator.get("error_select_env")
            )
            return
        
        selection = self.pkg_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                self.translator.get("dialog_warning"),
                self.translator.get("error_select_pkg")
            )
            return
        
        pkg_line = self.pkg_listbox.get(selection[0])
        if "==" in pkg_line:
            pkg_name = pkg_line.split("==")[0]
        else:
            pkg_name = pkg_line
        
        if messagebox.askyesno(
            self.translator.get("dialog_confirm"),
            self.translator.get("question_uninstall_pkg", pkg=pkg_name)
        ):
            choice = messagebox.askyesno(
                self.translator.get("dialog_confirm"),
                self.translator.get("question_use_pip")
            )
            
            if choice:
                cmd = f"pip uninstall {pkg_name} -y"
            else:
                cmd = f"conda remove -n {self.current_env} {pkg_name} -y"
            
            self.execute_env_command_custom(cmd, f"Remove package: {pkg_name}")
    
    def search_package(self):
        """Wyszukaj pakiet w repozytoriach"""
        package = simpledialog.askstring(
            self.translator.get("pkg_search"),
            self.translator.get("input_search_pkg")
        )
        if package:
            cmd = f"conda search {package}"
            self.execute_env_command_custom(cmd, f"Search package: {package}")
    
    def update_pip(self):
        """Zaktualizuj pip w środowisku"""
        if not self.current_env:
            return
        
        cmd = f"python -m pip install --upgrade pip"
        self.execute_env_command_custom(cmd, "Update pip")
    
    def update_conda(self):
        """Zaktualizuj conda"""
        cmd = "conda update conda -y"
        self.execute_env_command_custom(cmd, "Update conda")
    
    def clean_cache(self):
        """Wyczyść cache conda"""
        cmd = "conda clean --all -y"
        self.execute_env_command_custom(cmd, "Clear cache")
    
    def manage_repos(self):
        """Zarządzaj repozytoriami pip"""
        dialog = tk.Toplevel(self.root)
        dialog.title(self.translator.get("menu_manage_repos"))
        dialog.geometry("600x400")
        
        text = scrolledtext.ScrolledText(dialog, font=("Consolas", 9))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, "Current pip repositories:\n")
        text.insert(tk.END, "="*50 + "\n")
        
        try:
            result = subprocess.run(
                "pip config list",
                shell=True,
                capture_output=True,
                text=True
            )
            text.insert(tk.END, result.stdout)
        except Exception as e:
            text.insert(tk.END, f"Error: {str(e)}\n")
        
        text.insert(tk.END, "\n" + "="*50 + "\n")
        text.insert(tk.END, "Example commands:\n")
        text.insert(tk.END, "pip config list\n")
        text.insert(tk.END, "pip config set global.index-url https://pypi.org/simple\n")
        text.insert(tk.END, "pip config set global.trusted-host pypi.org\n")
    
    # ========== FUNKCJE KOMEND ==========
    
    def insert_quick_command(self, command):
        """Wstaw szybką komendę do pola"""
        self.cmd_var.set(command)
        self.cmd_entry.focus()
        self.cmd_entry.icursor(tk.END)
    
    def execute_env_command(self):
        """Wykonaj komendę w środowisku"""
        command = self.cmd_var.get().strip()
        if not command:
            return
        
        if not self.current_env:
            messagebox.showwarning(
                self.translator.get("dialog_warning"),
                self.translator.get("error_select_env")
            )
            return
        
        self.cmd_output.insert(tk.END, f"\n$ {self.current_env}> {command}\n")
        self.cmd_output.insert(tk.END, "-"*60 + "\n")
        self.cmd_output.see(tk.END)
        
        full_cmd = f'conda activate {self.current_env} && {command}'
        
        thread = threading.Thread(target=self.run_env_command, args=(full_cmd, command))
        thread.daemon = True
        thread.start()
        
        self.cmd_var.set("")
    
    def execute_env_command_custom(self, command, description=""):
        """Wykonaj komendę z opisem"""
        if description:
            self.cmd_output.insert(tk.END, f"\n▶ {description}\n")
        
        self.insert_quick_command(command)
        self.execute_env_command()
    
    def run_env_command(self, full_cmd, original_cmd):
        """Uruchom komendę środowiska"""
        try:
            process = subprocess.Popen(
                f'cmd /c "{full_cmd}"',
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.cmd_output.insert(tk.END, line)
                    self.cmd_output.see(tk.END)
                    self.root.update()
            
            process.stdout.close()
            return_code = process.wait()
            
            self.cmd_output.insert(tk.END, f"\n{'='*60}\n")
            if return_code == 0:
                self.cmd_output.insert(tk.END, f"{self.translator.get('command_success')}\n")
                self.show_status(self.translator.get("status_command_executed", cmd=original_cmd[:30]))
                
                if any(x in original_cmd for x in ["install", "remove", "uninstall"]):
                    self.root.after(1000, self.refresh_packages)
                    
            else:
                self.cmd_output.insert(tk.END, self.translator.get("command_error", code=return_code) + "\n")
                self.show_status(self.translator.get("status_command_error", cmd=original_cmd[:30]), error=True)
            
        except Exception as e:
            self.cmd_output.insert(tk.END, self.translator.get("command_exception", error=str(e)) + "\n")
            self.show_status(f"{self.translator.get('dialog_error')}: {str(e)}", error=True)
        
        self.cmd_output.insert(tk.END, "\n")
    
    # ========== FUNKCJE SKRYPTÓW ==========
    
    def browse_folder(self):
        """Wybierz folder ze skryptami"""
        folder = filedialog.askdirectory(
            title=self.translator.get("btn_browse") + " " + self.translator.get("script_section"),
            initialdir=self.path_var.get()
        )
        if folder:
            self.path_var.set(folder)
            self.script_folder = folder
            self.refresh_scripts()
    
    def open_folder(self):
        """Otwórz folder w eksploratorze"""
        folder = self.path_var.get()
        if os.path.exists(folder):
            os.startfile(folder)
    
    def refresh_scripts(self):
        """Odśwież listę skryptów"""
        self.script_listbox.delete(0, tk.END)
        folder = self.path_var.get()
        
        # SPRAWDŹ CZY FOLDER ISTNIEJE
        if not folder or not os.path.exists(folder):
            # Jeśli folder z pola tekstowego nie istnieje, użyj domyślnego
            folder = self.script_folder
            self.path_var.set(folder)  # Zaktualizuj pole tekstowe
            
            # Sprawdź czy domyślny folder też istnieje
            if not os.path.exists(folder):
                # Jeśli żaden folder nie istnieje, pokaż błąd
                self.script_listbox.insert(tk.END, f"❌ {self.translator.get('error_folder_not_exist')}")
                self.script_listbox.insert(tk.END, f"Folder: {folder}")
                self.show_status(self.translator.get("error_folder_not_exist"), error=True)
                return
        
        # TERAZ SPRÓBUJ ZAŁADOWAĆ SKRYPTY
        try:
            self.script_listbox.insert(tk.END, self.translator.get("folder_contents", folder=folder))
            self.script_listbox.insert(tk.END, "-" * 50)
            
            all_scripts = []
            py_count = 0
            
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith('.py'):
                        full_path = os.path.join(root, file)
                        
                        if root == folder:
                            display = f"📄 {file}"
                        else:
                            rel_path = os.path.relpath(root, folder)
                            display = f"📁 {rel_path}/{file}"
                        
                        all_scripts.append((display, full_path))
                        py_count += 1
            
            if py_count == 0:
                self.script_listbox.insert(tk.END, f"📭 {self.translator.get('no_py_files')}")
                self.script_listbox.insert(tk.END, self.translator.get("check_folder", folder=folder))
            else:
                all_scripts.sort(key=lambda x: x[0].lower())
                
                for display, full_path in all_scripts:
                    self.script_listbox.insert(tk.END, display)
                
                self.script_listbox.insert(tk.END, "-" * 50)
                self.script_listbox.insert(tk.END, self.translator.get("found_py_files", count=py_count))
            
            self.show_status(self.translator.get("status_scripts_found", count=py_count, folder=os.path.basename(folder)))
            
        except Exception as e:
            self.script_listbox.insert(tk.END, f"❌ {self.translator.get('dialog_error')}: {str(e)}")
            self.show_status(f"{self.translator.get('dialog_error')}: {str(e)}", error=True)
        
    
    def search_all_py(self):
        """Wyszukaj wszystkie pliki .py"""
        folder = self.path_var.get()
        if not os.path.exists(folder):
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(self.translator.get("menu_search_py"))
        dialog.geometry("800x600")
        
        text = scrolledtext.ScrolledText(dialog, font=("Consolas", 9))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, f"Searching .py files in: {folder}\n")
        text.insert(tk.END, "="*80 + "\n\n")
        
        try:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith('.py'):
                        full_path = os.path.join(root, file)
                        size = os.path.getsize(full_path)
                        rel_path = os.path.relpath(full_path, folder)
                        
                        text.insert(tk.END, f"📄 {rel_path}\n")
                        text.insert(tk.END, f"   Path: {full_path}\n")
                        text.insert(tk.END, f"   Size: {size:,} bytes\n")
                        text.insert(tk.END, "-"*40 + "\n")
            
            text.insert(tk.END, f"\n{self.translator.get('search_completed')}\n")
            
        except Exception as e:
            text.insert(tk.END, f"\n{self.translator.get('search_error', error=str(e))}\n")
    
    def on_script_select(self, event):
        """Obsługa wyboru skryptu"""
        selection = self.script_listbox.curselection()
        if selection:
            selected_text = self.script_listbox.get(selection[0])
            
            if any(marker in selected_text for marker in ["📂", "📭", "✅", "❌", "-", "="]):
                self.current_script = None
                return
            
            if "📄 " in selected_text:
                filename = selected_text.replace("📄 ", "")
                self.current_script = os.path.join(self.path_var.get(), filename)
            elif "📁 " in selected_text:
                path_part = selected_text.replace("📁 ", "")
                self.current_script = os.path.join(self.path_var.get(), path_part)
            else:
                self.current_script = os.path.join(self.path_var.get(), selected_text)
            
            self.show_status(f"Selected: {os.path.basename(self.current_script)}")
    
    def create_script(self):
        """Utwórz nowy skrypt"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
            initialdir=self.path_var.get(),
            title=self.translator.get("btn_new_script")
        )
        
        if filename:
            template = f'''# -*- coding: utf-8 -*-
"""
{self.translator.get('script_comment_created', datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}
{self.translator.get('script_comment_env', env=self.current_env)}
"""

def main():
    """{self.translator.get('script_main_function')}"""
    print("{self.translator.get('script_hello')}")
    print(f"Environment: {self.current_env}")
    print("{self.translator.get('script_running')}")
    
    # Add your code here
    for i in range(5):
        print(f"Number: {{i}}")

if __name__ == "__main__":
    main()
'''
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(template)
                
                self.refresh_scripts()
                self.show_status(self.translator.get("status_script_created", filename=os.path.basename(filename)))
                
                for i in range(self.script_listbox.size()):
                    if os.path.basename(filename) in self.script_listbox.get(i):
                        self.script_listbox.selection_clear(0, tk.END)
                        self.script_listbox.selection_set(i)
                        self.script_listbox.see(i)
                        self.on_script_select(None)
                        break
                        
            except Exception as e:
                self.show_status(f"Creation error: {str(e)}", error=True)
    
    def edit_script(self):
        """Edytuj skrypt"""
        if not self.current_script or not os.path.exists(self.current_script):
            messagebox.showwarning(
                self.translator.get("dialog_warning"),
                self.translator.get("error_select_script")
            )
            return
        
        try:
            os.startfile(self.current_script)
        except:
            subprocess.run(["notepad", self.current_script], shell=True)
    
    def run_script(self):
        """Uruchom skrypt"""
        if not self.current_script or not os.path.exists(self.current_script):
            messagebox.showwarning(
                self.translator.get("dialog_warning"),
                self.translator.get("error_select_script_run")
            )
            return
        
        self.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        thread = threading.Thread(target=self.execute_script)
        thread.daemon = True
        thread.start()
    
    def execute_script(self):
        """Wykonaj skrypt"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"\n{'='*60}\n")
        self.output_text.insert(tk.END, f"▶ [{timestamp}] Running: {os.path.basename(self.current_script)}\n")
        self.output_text.insert(tk.END, f"   Environment: {self.current_env}\n")
        self.output_text.insert(tk.END, f"   Path: {self.current_script}\n")
        self.output_text.insert(tk.END, f"{'='*60}\n\n")
        self.output_text.see(tk.END)
        
        try:
            activate_cmd = f"conda activate {self.current_env} && "
            python_cmd = f'python "{self.current_script}"'
            full_cmd = f'cmd /c "{activate_cmd}{python_cmd}"'
            
            self.current_process = subprocess.Popen(
                full_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            for line in iter(self.current_process.stdout.readline, ''):
                if line:
                    self.output_text.insert(tk.END, line)
                    self.output_text.see(tk.END)
                    self.root.update()
            
            self.current_process.stdout.close()
            return_code = self.current_process.wait()
            
            if return_code == 0:
                self.output_text.insert(tk.END, f"\n✅ {self.translator.get('status_script_completed')}\n")
                self.show_status(self.translator.get("status_script_completed"))
            else:
                self.output_text.insert(tk.END, self.translator.get("command_error", code=return_code) + "\n")
                self.show_status(f"Error (code: {return_code})", error=True)
            
        except Exception as e:
            self.output_text.insert(tk.END, self.translator.get("command_exception", error=str(e)) + "\n")
            self.show_status(f"Error: {str(e)}", error=True)
        
        finally:
            self.output_text.insert(tk.END, f"{'='*60}\n\n")
            self.output_text.see(tk.END)
            
            self.run_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.current_process = None
    
    def stop_script(self):
        """Zatrzymaj skrypt"""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.output_text.insert(tk.END, f"\n⏹️ {self.translator.get('status_script_stopped')}\n")
                self.show_status(self.translator.get("status_script_stopped"))
            except:
                pass
            
            self.run_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def restart_script(self):
        """Uruchom ponownie skrypt"""
        if self.current_script and os.path.exists(self.current_script):
            self.run_script()
        else:
            messagebox.showinfo(
                self.translator.get("dialog_info"),
                "Run the script first"
            )
    
    def open_terminal(self):
        """Otwórz terminal"""
        try:
            cmd = f'start cmd /k "conda activate {self.current_env} && title Terminal: {self.current_env}"'
            subprocess.Popen(cmd, shell=True)
            self.show_status(self.translator.get("menu_open_terminal"))
        except Exception as e:
            self.show_status(f"{self.translator.get('dialog_error')}: {str(e)}", error=True)
    
    def set_default_folder(self):
        """Ustaw domyślny folder i zapisz do konfiguracji"""
        folder = self.path_var.get()
        if os.path.exists(folder):
            # Ustaw w aplikacji
            self.script_folder = folder
            self.path_var.set(folder)
            
            # Zapisz do konfiguracji
            if self.translator.set_default_folder(folder):
                self.show_status(self.translator.get("status_default_set", folder=folder))
                # Odśwież listę skryptów w nowym folderze
                self.refresh_scripts()
            else:
                self.show_status("Failed to save default folder", error=True)
        else:
            self.show_status("Folder does not exist", error=True)
    
    def create_env(self):
        """Utwórz środowisko"""
        name = simpledialog.askstring(
            self.translator.get("btn_new"),
            self.translator.get("input_new_env")
        )
        if name:
            version = simpledialog.askstring(
                self.translator.get("input_python_version"),
                self.translator.get("input_python_version"),
                initialvalue="3.9"
            )
            if version:
                cmd = f"conda create -n {name} python={version} -y"
                self.execute_env_command_custom(cmd, f"Create environment '{name}'")
    
    def delete_env(self):
        """Usuń środowisko"""
        selection = self.env_tree.selection()
        if not selection:
            return
        
        env_name = self.env_tree.item(selection[0], "text")
        env_name = env_name.replace(" ★", "").strip()
        
        if env_name == "base":
            messagebox.showwarning(
                self.translator.get("dialog_warning"),
                self.translator.get("error_no_base_delete")
            )
            return
        
        if messagebox.askyesno(
            self.translator.get("dialog_confirm"),
            self.translator.get("question_uninstall_env", env=env_name)
        ):
            cmd = f"conda remove -n {env_name} --all -y"
            self.execute_env_command_custom(cmd, f"Delete environment '{env_name}'")
    
    def show_status(self, message, error=False):
        """Pokaż status"""
        if error:
            self.status_var.set(f"❌ {message}")
        else:
            self.status_var.set(f"✓ {message}")

def main():
    root = tk.Tk()
    app = MiniCondaNavigator(root)
    root.mainloop()

if __name__ == "__main__":
    main()