import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

class ModernRuleEngineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rule Engine Management System")
        self.root.geometry("800x700")
        self.root.minsize(600, 700)    # Reduced minimum width
        
        self.root.configure(bg="#060b28")
        
        # Create main container frame
        self.container = ttk.Frame(root)
        self.container.pack(fill="both", expand=True)
        
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(self.container, bg="#060b28")
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        
        # Create main frame inside canvas
        self.main_frame = ttk.Frame(self.canvas, padding="10")
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Configure canvas and frame behavior
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.main_frame.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f2f5")
        self.style.configure("TLabelframe", background="#f0f2f5")
        self.style.configure("TLabel", background="#f0f2f5", font=("Helvetica", 10))
        self.style.configure("TButton", padding=5, font=("Helvetica", 10))
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"), foreground="#2c3e50", background="#f0f2f5")
        
        # Create sections
        self.create_header_section()
        self.create_rule_section()
        self.create_combine_section()
        self.create_evaluate_section()
        self.create_modify_section()
        self.create_output_section()

    def _on_canvas_configure(self, event):
        # Update the canvas's scroll region and frame width when canvas is resized
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
        min_width = min(event.width, 800)  # Maximum width of 800px
        for frame in self.main_frame.winfo_children():
            if isinstance(frame, ttk.LabelFrame):
                frame.configure(width=min_width - 40)  # Account for padding

    def _on_frame_configure(self, event):
        # Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_header_section(self):
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        header = ttk.Label(header_frame, text="Rule Engine Management System", style="Header.TLabel")
        header.pack(anchor="center")

    def create_rule_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="Create New Rule", padding="10")
        frame.pack(fill="x", padx=10, pady=5)

        # Container frame for content
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="x", padx=5)

        ttk.Label(content_frame, text="Rule String:").pack(anchor="w")
        self.rule_string_entry = ttk.Entry(content_frame)
        self.rule_string_entry.pack(fill="x", pady=(5, 10))

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill="x")
        create_btn = ttk.Button(button_frame, text="Create Rule", command=self.create_rule)
        create_btn.pack(anchor="e")

    def create_combine_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="Combine Rules", padding="10")
        frame.pack(fill="x", padx=10, pady=5)

        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="x", padx=5)

        ttk.Label(content_frame, text="Rule IDs (comma-separated):").pack(anchor="w")
        self.rule_ids_entry = ttk.Entry(content_frame)
        self.rule_ids_entry.pack(fill="x", pady=(5, 10))

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill="x")
        combine_btn = ttk.Button(button_frame, text="Combine Rules", command=self.combine_rules)
        combine_btn.pack(anchor="e")

    def create_evaluate_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="Evaluate Rule", padding="10")
        frame.pack(fill="x", padx=10, pady=5)

        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="x", padx=5)

        ttk.Label(content_frame, text="Mega Rule ID:").pack(anchor="w")
        self.mega_rule_id_entry = ttk.Entry(content_frame)
        self.mega_rule_id_entry.pack(fill="x", pady=(5, 10))

        ttk.Label(content_frame, text="Data (JSON):").pack(anchor="w")
        self.data_entry = ttk.Entry(content_frame)
        self.data_entry.pack(fill="x", pady=(5, 10))

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill="x")
        evaluate_btn = ttk.Button(button_frame, text="Evaluate Rule", command=self.evaluate_rule)
        evaluate_btn.pack(anchor="e")

    def create_modify_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="Modify Rule", padding="10")
        frame.pack(fill="x", padx=10, pady=5)

        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="x", padx=5)

        ttk.Label(content_frame, text="Rule ID:").pack(anchor="w")
        self.modify_rule_id_entry = ttk.Entry(content_frame)
        self.modify_rule_id_entry.pack(fill="x", pady=(5, 10))

        ttk.Label(content_frame, text="New Rule String:").pack(anchor="w")
        self.new_rule_string_entry = ttk.Entry(content_frame)
        self.new_rule_string_entry.pack(fill="x", pady=(5, 10))

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill="x")
        modify_btn = ttk.Button(button_frame, text="Modify Rule", command=self.modify_rule)
        modify_btn.pack(anchor="e")

    def create_output_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="Output Log", padding="10")
        frame.pack(fill="x", padx=10, pady=5)

        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="x", padx=5)

        self.output_text = scrolledtext.ScrolledText(
            content_frame,
            height=8,
            font=("Courier", 10),
            wrap=tk.WORD
        )
        self.output_text.pack(fill="both", expand=True, pady=5)

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill="x")
        clear_btn = ttk.Button(
            button_frame,
            text="Clear Log",
            command=lambda: self.output_text.delete(1.0, tk.END)
        )
        clear_btn.pack(anchor="e")

    def log_output(self, message, is_error=False):
        self.output_text.insert(tk.END, f"{'ERROR: ' if is_error else ''}{message}\n")
        self.output_text.see(tk.END)

    # [Rest of the methods remain the same: create_rule, combine_rules, evaluate_rule, modify_rule]
    def create_rule(self):
        rule_string = self.rule_string_entry.get()
        try:
            response = requests.post(f"{BASE_URL}/create_rule", json={"rule_string": rule_string})
            response.raise_for_status()
            self.log_output(f"Rule created successfully: {response.json()}")
        except requests.exceptions.RequestException as e:
            self.log_output(str(e), is_error=True)

    def combine_rules(self):
        try:
            rule_ids = [int(id.strip()) for id in self.rule_ids_entry.get().split(',')]
            response = requests.post(f"{BASE_URL}/combine_rules", json={"rule_ids": rule_ids})
            response.raise_for_status()
            self.log_output(f"Rules combined successfully: {response.json()}")
        except (ValueError, requests.exceptions.RequestException) as e:
            self.log_output(str(e), is_error=True)

    def evaluate_rule(self):
        try:
            mega_rule_id = int(self.mega_rule_id_entry.get())
            data = json.loads(self.data_entry.get())
            response = requests.post(f"{BASE_URL}/evaluate_rule", json={"rule_id": mega_rule_id, "data": data})
            response.raise_for_status()
            self.log_output(f"Rule evaluation result: {response.json()}")
        except (ValueError, json.JSONDecodeError, requests.exceptions.RequestException) as e:
            self.log_output(str(e), is_error=True)

    def modify_rule(self):
        try:
            rule_id = int(self.modify_rule_id_entry.get())
            new_rule_string = self.new_rule_string_entry.get()
            response = requests.post(f"{BASE_URL}/modify_rule", json={"rule_id": rule_id, "new_rule_string": new_rule_string})
            response.raise_for_status()
            self.log_output(f"Rule modified successfully: {response.json()}")
        except (ValueError, requests.exceptions.RequestException) as e:
            self.log_output(str(e), is_error=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernRuleEngineApp(root)
    root.mainloop()


