#!/usr/bin/env python3
"""
KaliGPT GUI - Modern Web-based Interface
AI-Powered Penetration Testing Assistant
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import queue
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.ai_engine import AIEngine
except ImportError:
    AIEngine = None

from payloads.generator import PayloadGenerator

try:
    from reporting.report_builder import ReportBuilder as ReportGenerator
except ImportError:
    ReportGenerator = None

from models.model_selector import ModelSelector


class KaliGPTGUI:
    """Modern GUI for KaliGPT"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 KaliGPT - AI-Powered Penetration Testing Assistant")
        self.root.geometry("1400x900")
        
        # Color scheme - Kali Linux inspired
        self.colors = {
            'bg': '#0d1117',
            'bg_light': '#161b22',
            'bg_card': '#1c2128',
            'accent': '#00d9ff',
            'accent_dark': '#00a8cc',
            'text': '#e6edf3',
            'text_dim': '#8b949e',
            'success': '#3fb950',
            'warning': '#f0883e',
            'error': '#f85149',
            'border': '#30363d'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg'])
        
        # Initialize components
        self.ai_engine = None
        self.payload_generator = None
        self.report_generator = ReportGenerator()
        self.command_history = []
        self.current_session = {
            'commands': [],
            'outputs': [],
            'recommendations': [],
            'payloads': []
        }
        
        # Thread-safe queue for AI responses
        self.response_queue = queue.Queue()
        
        # Create UI
        self.create_menu()
        self.create_header()
        self.create_main_layout()
        self.create_status_bar()
        
        # Start checking for AI responses
        self.check_response_queue()
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root, bg=self.colors['bg_light'], fg=self.colors['text'])
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['bg_light'], fg=self.colors['text'])
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Session", command=self.new_session)
        file_menu.add_command(label="Save Session", command=self.save_session)
        file_menu.add_command(label="Load Session", command=self.load_session)
        file_menu.add_separator()
        file_menu.add_command(label="Export Report", command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['bg_light'], fg=self.colors['text'])
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Payload Generator", command=self.open_payload_generator)
        tools_menu.add_command(label="Template Browser", command=self.open_template_browser)
        tools_menu.add_separator()
        tools_menu.add_command(label="Settings", command=self.open_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['bg_light'], fg=self.colors['text'])
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_docs)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_header(self):
        """Create header with logo and title"""
        header_frame = tk.Frame(self.root, bg=self.colors['bg'], height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Logo (if exists)
        logo_path = Path(__file__).parent.parent / "public" / "Untitled design.png"
        if logo_path.exists():
            try:
                from PIL import Image, ImageTk
                img = Image.open(logo_path)
                img = img.resize((60, 60), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                logo_label = tk.Label(header_frame, image=self.logo_img, bg=self.colors['bg'])
                logo_label.pack(side=tk.LEFT, padx=(0, 15))
            except:
                pass
        
        # Title
        title_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        title_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(
            title_frame,
            text="🔒 KaliGPT",
            font=("Helvetica", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(
            title_frame,
            text="AI-Powered Penetration Testing Assistant",
            font=("Helvetica", 11),
            bg=self.colors['bg'],
            fg=self.colors['text_dim']
        )
        subtitle_label.pack(anchor=tk.W)
        
    def create_main_layout(self):
        """Create main application layout"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - AI Configuration & Controls
        left_panel = tk.Frame(main_container, bg=self.colors['bg_card'], width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_ai_config_panel(left_panel)
        self.create_quick_actions_panel(left_panel)
        
        # Right panel - Main workspace
        right_panel = tk.Frame(main_container, bg=self.colors['bg'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Notebook for tabs
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Custom.TNotebook', background=self.colors['bg'], borderwidth=0)
        style.configure('Custom.TNotebook.Tab', 
                       background=self.colors['bg_light'],
                       foreground=self.colors['text'],
                       padding=[20, 10])
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', self.colors['bg_card'])],
                 foreground=[('selected', self.colors['accent'])])
        
        self.notebook = ttk.Notebook(right_panel, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_terminal_tab()
        self.create_payload_tab()
        self.create_analysis_tab()
        self.create_report_tab()
        
    def create_ai_config_panel(self, parent):
        """Create AI configuration panel"""
        # Panel header
        header = tk.Label(
            parent,
            text="⚙️ AI Configuration",
            font=("Helvetica", 13, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text'],
            anchor=tk.W
        )
        header.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        # Model selection
        model_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        model_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(
            model_frame,
            text="AI Model:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_dim'],
            font=("Helvetica", 9)
        ).pack(anchor=tk.W)
        
        self.model_var = tk.StringVar(value="gpt-5.1")
        model_selector = ModelSelector()
        models = model_selector.list_available_models()
        
        self.model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=models,
            state='readonly',
            width=30
        )
        self.model_combo.pack(fill=tk.X, pady=(5, 0))
        
        # Connect button
        connect_btn = tk.Button(
            parent,
            text="🔌 Connect to AI",
            command=self.connect_ai,
            bg=self.colors['accent'],
            fg='white',
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10
        )
        connect_btn.pack(fill=tk.X, padx=15, pady=10)
        
        # Status indicator
        self.ai_status_label = tk.Label(
            parent,
            text="⚫ Disconnected",
            bg=self.colors['bg_card'],
            fg=self.colors['text_dim'],
            font=("Helvetica", 9)
        )
        self.ai_status_label.pack(padx=15, pady=(0, 15))
        
    def create_quick_actions_panel(self, parent):
        """Create quick actions panel"""
        # Separator
        separator = tk.Frame(parent, bg=self.colors['border'], height=1)
        separator.pack(fill=tk.X, padx=15, pady=15)
        
        # Panel header
        header = tk.Label(
            parent,
            text="⚡ Quick Actions",
            font=("Helvetica", 13, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text'],
            anchor=tk.W
        )
        header.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # Quick action buttons
        actions = [
            ("🔍 Analyze Output", self.quick_analyze),
            ("💉 Generate Payload", self.quick_payload),
            ("📝 Get Recommendation", self.quick_recommend),
            ("📊 Generate Report", self.quick_report),
        ]
        
        for text, command in actions:
            btn = tk.Button(
                parent,
                text=text,
                command=command,
                bg=self.colors['bg_light'],
                fg=self.colors['text'],
                font=("Helvetica", 9),
                relief=tk.FLAT,
                cursor='hand2',
                anchor=tk.W,
                padx=15,
                pady=8
            )
            btn.pack(fill=tk.X, padx=15, pady=2)
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors['border']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors['bg_light']))
        
    def create_terminal_tab(self):
        """Create terminal/command tab"""
        tab = tk.Frame(self.notebook, bg=self.colors['bg_card'])
        self.notebook.add(tab, text="Terminal")
        
        # Input section
        input_frame = tk.Frame(tab, bg=self.colors['bg_card'])
        input_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(
            input_frame,
            text="Command Output / Analysis Input:",
            bg=self.colors['bg_card'],
            fg=self.colors['text'],
            font=("Helvetica", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.command_input = scrolledtext.ScrolledText(
            input_frame,
            height=10,
            bg=self.colors['bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['accent'],
            font=("Consolas", 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.command_input.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = tk.Frame(tab, bg=self.colors['bg_card'])
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        tk.Button(
            btn_frame,
            text="🤖 Analyze with AI",
            command=self.analyze_command,
            bg=self.colors['accent'],
            fg='white',
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            btn_frame,
            text="🗑️ Clear",
            command=lambda: self.command_input.delete(1.0, tk.END),
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            font=("Helvetica", 10),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=8
        ).pack(side=tk.LEFT)
        
        # Output section
        tk.Label(
            tab,
            text="AI Analysis & Recommendations:",
            bg=self.colors['bg_card'],
            fg=self.colors['text'],
            font=("Helvetica", 10, "bold")
        ).pack(anchor=tk.W, padx=15, pady=(0, 5))
        
        self.ai_output = scrolledtext.ScrolledText(
            tab,
            height=15,
            bg=self.colors['bg'],
            fg=self.colors['success'],
            font=("Consolas", 10),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.ai_output.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
    def create_payload_tab(self):
        """Create payload generation tab"""
        tab = tk.Frame(self.notebook, bg=self.colors['bg_card'])
        self.notebook.add(tab, text="Payloads")
        
        # Two column layout
        left_col = tk.Frame(tab, bg=self.colors['bg_card'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Payload type selection
        tk.Label(
            left_col,
            text="Payload Type:",
            bg=self.colors['bg_card'],
            fg=self.colors['text'],
            font=("Helvetica", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.payload_type_var = tk.StringVar(value="sqli")
        payload_types = ["sqli", "xss", "reverse_shells", "webshells", "privesc", "wordlists"]
        
        payload_type_combo = ttk.Combobox(
            left_col,
            textvariable=self.payload_type_var,
            values=payload_types,
            state='readonly'
        )
        payload_type_combo.pack(fill=tk.X, pady=(0, 15))
        payload_type_combo.bind('<<ComboboxSelected>>', self.update_template_list)
        
        # Template selection
        tk.Label(
            left_col,
            text="Template:",
            bg=self.colors['bg_card'],
            fg=self.colors['text'],
            font=("Helvetica", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(
            left_col,
            textvariable=self.template_var,
            state='readonly'
        )
        self.template_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Variables section
        tk.Label(
            left_col,
            text="Variables (JSON format):",
            bg=self.colors['bg_card'],
            fg=self.colors['text'],
            font=("Helvetica", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.payload_vars = scrolledtext.ScrolledText(
            left_col,
            height=8,
            bg=self.colors['bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['accent'],
            font=("Consolas", 9),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.payload_vars.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        self.payload_vars.insert(1.0, '{\n  "ATTACKER_IP": "10.10.14.5",\n  "ATTACKER_PORT": "4444"\n}')
        
        # Generate button
        tk.Button(
            left_col,
            text="🚀 Generate Payload",
            command=self.generate_payload,
            bg=self.colors['accent'],
            fg='white',
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10
        ).pack(fill=tk.X)
        
        # Right column - Output
        right_col = tk.Frame(tab, bg=self.colors['bg_card'])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15), pady=15)
        
        tk.Label(
            right_col,
            text="Generated Payload:",
            bg=self.colors['bg_card'],
            fg=self.colors['text'],
            font=("Helvetica", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.payload_output = scrolledtext.ScrolledText(
            right_col,
            bg=self.colors['bg'],
            fg=self.colors['warning'],
            font=("Consolas", 9),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.payload_output.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Copy button
        tk.Button(
            right_col,
            text="📋 Copy to Clipboard",
            command=self.copy_payload,
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            font=("Helvetica", 9),
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=8
        ).pack(fill=tk.X)
        
        # Initialize template list
        self.update_template_list()
        
    def create_analysis_tab(self):
        """Create analysis history tab"""
        tab = tk.Frame(self.notebook, bg=self.colors['bg_card'])
        self.notebook.add(tab, text="Analysis History")
        
        # History list
        tk.Label(
            tab,
            text="Session History:",
            bg=self.colors['bg_card'],
            fg=self.colors['text'],
            font=("Helvetica", 10, "bold")
        ).pack(anchor=tk.W, padx=15, pady=(15, 5))
        
        self.history_text = scrolledtext.ScrolledText(
            tab,
            bg=self.colors['bg'],
            fg=self.colors['text'],
            font=("Consolas", 9),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
    def create_report_tab(self):
        """Create report generation tab"""
        tab = tk.Frame(self.notebook, bg=self.colors['bg_card'])
        self.notebook.add(tab, text="Report")
        
        # Report format selection
        format_frame = tk.Frame(tab, bg=self.colors['bg_card'])
        format_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(
            format_frame,
            text="Report Format:",
            bg=self.colors['bg_card'],
            fg=self.colors['text'],
            font=("Helvetica", 10, "bold")
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.report_format_var = tk.StringVar(value="markdown")
        formats = ["markdown", "html", "json"]
        
        for fmt in formats:
            tk.Radiobutton(
                format_frame,
                text=fmt.upper(),
                variable=self.report_format_var,
                value=fmt,
                bg=self.colors['bg_card'],
                fg=self.colors['text'],
                selectcolor=self.colors['accent'],
                activebackground=self.colors['bg_card'],
                activeforeground=self.colors['accent']
            ).pack(side=tk.LEFT, padx=5)
        
        # Report preview
        tk.Label(
            tab,
            text="Report Preview:",
            bg=self.colors['bg_card'],
            fg=self.colors['text'],
            font=("Helvetica", 10, "bold")
        ).pack(anchor=tk.W, padx=15, pady=(0, 5))
        
        self.report_preview = scrolledtext.ScrolledText(
            tab,
            bg=self.colors['bg'],
            fg=self.colors['text'],
            font=("Consolas", 9),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.report_preview.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Buttons
        btn_frame = tk.Frame(tab, bg=self.colors['bg_card'])
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        tk.Button(
            btn_frame,
            text="🔄 Generate Preview",
            command=self.preview_report,
            bg=self.colors['accent'],
            fg='white',
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            btn_frame,
            text="💾 Save Report",
            command=self.export_report,
            bg=self.colors['success'],
            fg='white',
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=8
        ).pack(side=tk.LEFT)
        
    def create_status_bar(self):
        """Create status bar"""
        status_bar = tk.Frame(self.root, bg=self.colors['bg_light'], height=30)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_bar,
            text="Ready",
            bg=self.colors['bg_light'],
            fg=self.colors['text_dim'],
            font=("Helvetica", 9),
            anchor=tk.W,
            padx=20
        )
        self.status_label.pack(fill=tk.X)
        
    def connect_ai(self):
        """Connect to AI engine"""
        try:
            self.update_status("Connecting to AI engine...")
            model = self.model_var.get()
            
            # Initialize AI engine in a thread
            def init_ai():
                try:
                    self.ai_engine = AIEngine(model=model)
                    self.payload_generator = PayloadGenerator(self.ai_engine)
                    self.response_queue.put(('ai_connected', True))
                except Exception as e:
                    self.response_queue.put(('ai_error', str(e)))
            
            threading.Thread(target=init_ai, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            self.update_status("Connection failed")
            
    def analyze_command(self):
        """Analyze command output with AI"""
        if not self.ai_engine:
            messagebox.showwarning("AI Not Connected", "Please connect to an AI model first.")
            return
        
        command_output = self.command_input.get(1.0, tk.END).strip()
        if not command_output:
            messagebox.showwarning("No Input", "Please enter command output to analyze.")
            return
        
        self.update_status("Analyzing with AI...")
        
        # Analyze in thread
        def analyze():
            try:
                prompt = f"""Analyze this penetration testing command output and provide:
1. What was discovered
2. Security implications
3. Next recommended steps
4. Potential vulnerabilities

Output:
{command_output}
"""
                response = self.ai_engine.analyze(prompt)
                self.response_queue.put(('analysis', response))
                
                # Add to history
                self.current_session['commands'].append(command_output)
                self.current_session['outputs'].append(response)
                
            except Exception as e:
                self.response_queue.put(('error', str(e)))
        
        threading.Thread(target=analyze, daemon=True).start()
        
    def generate_payload(self):
        """Generate payload from template"""
        if not self.payload_generator:
            messagebox.showwarning("Not Ready", "Please connect to AI first.")
            return
        
        try:
            import json
            payload_type = self.payload_type_var.get()
            template = self.template_var.get()
            variables_json = self.payload_vars.get(1.0, tk.END).strip()
            
            if not template:
                messagebox.showwarning("No Template", "Please select a template.")
                return
            
            variables = json.loads(variables_json)
            
            self.update_status("Generating payload...")
            
            payload = self.payload_generator.get_from_template(
                payload_type, template, variables
            )
            
            self.payload_output.config(state=tk.NORMAL)
            self.payload_output.delete(1.0, tk.END)
            self.payload_output.insert(1.0, payload)
            self.payload_output.config(state=tk.DISABLED)
            
            self.current_session['payloads'].append({
                'type': payload_type,
                'template': template,
                'payload': payload
            })
            
            self.update_status("Payload generated successfully")
            
        except json.JSONDecodeError:
            messagebox.showerror("JSON Error", "Invalid JSON format in variables.")
        except Exception as e:
            messagebox.showerror("Generation Error", f"Failed to generate payload: {str(e)}")
            
    def update_template_list(self, event=None):
        """Update template list based on payload type"""
        if not self.payload_generator:
            self.payload_generator = PayloadGenerator()
        
        try:
            templates = self.payload_generator.list_templates()
            payload_type = self.payload_type_var.get()
            
            if payload_type in templates:
                self.template_combo['values'] = templates[payload_type]
                if templates[payload_type]:
                    self.template_combo.current(0)
        except Exception as e:
            print(f"Error updating templates: {e}")
            
    def copy_payload(self):
        """Copy payload to clipboard"""
        payload = self.payload_output.get(1.0, tk.END).strip()
        if payload:
            self.root.clipboard_clear()
            self.root.clipboard_append(payload)
            self.update_status("Payload copied to clipboard")
        
    def preview_report(self):
        """Generate report preview"""
        try:
            fmt = self.report_format_var.get()
            
            # Generate report from current session
            report_data = {
                'target': 'Target System',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'findings': self.current_session['outputs'],
                'payloads': self.current_session['payloads']
            }
            
            if fmt == 'markdown':
                report = self.report_generator.generate_markdown(report_data)
            elif fmt == 'html':
                report = self.report_generator.generate_html(report_data)
            else:
                import json
                report = json.dumps(report_data, indent=2)
            
            self.report_preview.config(state=tk.NORMAL)
            self.report_preview.delete(1.0, tk.END)
            self.report_preview.insert(1.0, report)
            self.report_preview.config(state=tk.DISABLED)
            
            self.update_status("Report preview generated")
            
        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to generate report: {str(e)}")
            
    def check_response_queue(self):
        """Check for AI responses in queue"""
        try:
            while True:
                msg_type, data = self.response_queue.get_nowait()
                
                if msg_type == 'ai_connected':
                    self.ai_status_label.config(text="🟢 Connected", fg=self.colors['success'])
                    self.update_status(f"Connected to {self.model_var.get()}")
                    messagebox.showinfo("Success", "Successfully connected to AI engine!")
                    
                elif msg_type == 'ai_error':
                    self.ai_status_label.config(text="🔴 Error", fg=self.colors['error'])
                    self.update_status("Connection failed")
                    messagebox.showerror("Error", f"AI Connection Error: {data}")
                    
                elif msg_type == 'analysis':
                    self.ai_output.config(state=tk.NORMAL)
                    self.ai_output.insert(tk.END, f"\n{'='*80}\n")
                    self.ai_output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] AI Analysis:\n\n")
                    self.ai_output.insert(tk.END, data)
                    self.ai_output.insert(tk.END, f"\n{'='*80}\n")
                    self.ai_output.config(state=tk.DISABLED)
                    self.ai_output.see(tk.END)
                    
                    # Update history
                    self.update_history()
                    self.update_status("Analysis complete")
                    
                elif msg_type == 'error':
                    messagebox.showerror("Error", f"An error occurred: {data}")
                    self.update_status("Error occurred")
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_response_queue)
        
    def update_history(self):
        """Update analysis history"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        for i, (cmd, output) in enumerate(zip(
            self.current_session['commands'],
            self.current_session['outputs']
        ), 1):
            self.history_text.insert(tk.END, f"[Entry {i}]\n")
            self.history_text.insert(tk.END, f"Input:\n{cmd[:200]}...\n\n")
            self.history_text.insert(tk.END, f"Analysis:\n{output[:300]}...\n\n")
            self.history_text.insert(tk.END, "="*80 + "\n\n")
        
        self.history_text.config(state=tk.DISABLED)
        
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    # Quick action methods
    def quick_analyze(self):
        self.notebook.select(0)
        self.analyze_command()
        
    def quick_payload(self):
        self.notebook.select(1)
        
    def quick_recommend(self):
        self.notebook.select(0)
        if self.ai_engine:
            self.command_input.delete(1.0, tk.END)
            self.command_input.insert(1.0, "What should I do next in my penetration test?")
            self.analyze_command()
        
    def quick_report(self):
        self.notebook.select(3)
        self.preview_report()
        
    # Menu methods
    def new_session(self):
        if messagebox.askyesno("New Session", "Start a new session? Current progress will be lost."):
            self.current_session = {
                'commands': [],
                'outputs': [],
                'recommendations': [],
                'payloads': []
            }
            self.command_input.delete(1.0, tk.END)
            self.ai_output.config(state=tk.NORMAL)
            self.ai_output.delete(1.0, tk.END)
            self.ai_output.config(state=tk.DISABLED)
            self.update_history()
            self.update_status("New session started")
            
    def save_session(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            import json
            with open(filename, 'w') as f:
                json.dump(self.current_session, f, indent=2)
            self.update_status(f"Session saved to {filename}")
            
    def load_session(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            import json
            with open(filename, 'r') as f:
                self.current_session = json.load(f)
            self.update_history()
            self.update_status(f"Session loaded from {filename}")
            
    def export_report(self):
        fmt = self.report_format_var.get()
        ext = {'markdown': '.md', 'html': '.html', 'json': '.json'}[fmt]
        
        filename = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[(f"{fmt.upper()} files", f"*{ext}"), ("All files", "*.*")]
        )
        
        if filename:
            report = self.report_preview.get(1.0, tk.END)
            with open(filename, 'w') as f:
                f.write(report)
            self.update_status(f"Report exported to {filename}")
            messagebox.showinfo("Success", f"Report saved to {filename}")
            
    def open_payload_generator(self):
        self.notebook.select(1)
        
    def open_template_browser(self):
        # TODO: Implement template browser window
        messagebox.showinfo("Template Browser", "Template browser coming soon!")
        
    def open_settings(self):
        # TODO: Implement settings window
        messagebox.showinfo("Settings", "Settings panel coming soon!")
        
    def show_docs(self):
        import webbrowser
        webbrowser.open("https://github.com/yashab-cyber/KaliGpt/docs")
        
    def show_about(self):
        about_text = """
🔒 KaliGPT v1.1.0

AI-Powered Penetration Testing Assistant

Developed for ethical hackers and security professionals.

Features:
• Multi-model AI support (GPT-5, Gemini 3, Claude)
• Intelligent payload generation
• Real-time analysis
• Automated reporting

GitHub: https://github.com/yashab-cyber/KaliGpt

Licensed under MIT
"""
        messagebox.showinfo("About KaliGPT", about_text)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = KaliGPTGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
