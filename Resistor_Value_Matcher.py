import tkinter as tk
from tkinter import scrolledtext, messagebox

def get_e24_resistors():
    E24_base = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
    values = [round(r * 10**e, 2) for e in range(-1, 7) for r in E24_base]
    return sorted(set(v for v in values if 0.1 <= v <= 10_000_000))


def get_e96_resistors():
    E96_base = [1.00,1.02,1.05,1.07,1.10,1.13,1.15,1.18,1.21,1.24,1.27,1.30,
                1.33,1.37,1.40,1.43,1.47,1.50,1.54,1.58,1.62,1.65,1.69,1.74,
                1.78,1.82,1.87,1.91,1.96,2.00,2.05,2.10,2.15,2.21,2.26,2.32,
                2.37,2.43,2.49,2.55,2.61,2.67,2.74,2.80,2.87,2.94,3.01,3.09,
                3.16,3.24,3.32,3.40,3.48,3.57,3.65,3.74,3.83,3.92,4.02,4.12,
                4.22,4.32,4.42,4.53,4.64,4.75,4.87,4.99,5.11,5.23,5.36,5.49,
                5.62,5.76,5.90,6.04,6.19,6.34,6.49,6.65,6.81,6.98,7.15,7.32,
                7.50,7.68,7.87,8.06,8.25,8.45,8.66,8.87,9.09,9.31,9.53,9.76]
    values = [round(v * 10**e, 3) for v in E96_base for e in range(-1, 7)]
    return [r for r in values if 0.1 <= r <= 10_000_000]


def get_default_custom_resistors():
    return """1, 10, 22, 47, 100, 150, 220, 470, 1000, 1200, 1800, 2000, 2200,
2400, 2700, 3300, 3900, 4700, 5600,6800, 8200, 9100, 10000, 15000, 20000, 22000, 27000, 
33000, 39000, 47000, 100000, 200000, 220000, 330000, 470000, 510000, 1000000"""


# ==================== Calculation Functions ====================
def series(r1, r2):
    return r1 + r2


def parallel(r1, r2):
    return (r1 * r2) / (r1 + r2)


def parse_custom_resistors(custom_str):
    # Parse comma-separated resistor values from string
    try:
        resistors = []
        for part in custom_str.replace('\n', ',').split(','):
            part = part.strip()
            if part:
                resistors.append(float(part))
        return sorted(set(resistors))
    except ValueError as e:
        raise ValueError(f"Invalid resistor value format: {e}")


def parse_targets(targets_str):
    # Parse comma-separated target values from string
    try:
        targets = []
        for part in targets_str.replace('\n', ',').split(','):
            part = part.strip()
            if part:
                targets.append(float(part))
        return targets
    except ValueError as e:
        raise ValueError(f"Invalid target value format: {e}")


def find_best(target, resistors):
    # Find best match for a single target value 
    best = None
    best_error = float('inf')
    best_type = ""
    best_pair = ()
    
    # Single resistor
    for r in resistors:
        err_single = abs(r - target) / target
        if err_single < best_error:
            best_error = err_single
            best = r
            best_type = "single"
            best_pair = (r,)
    
    # Series and parallel combinations
    for i, r1 in enumerate(resistors):
        for r2 in resistors[i:]:  # Only check each pair once (since series is commutative)
            # Series
            s_val = series(r1, r2)
            err_s = abs(s_val - target) / target
            if err_s < best_error:
                best_error = err_s
                best = s_val
                best_type = "series"
                best_pair = (r1, r2)
            
            # Parallel
            if r1 != 0 and r2 != 0:
                p_val = parallel(r1, r2)
                err_p = abs(p_val - target) / target
                if err_p < best_error:
                    best_error = err_p
                    best = p_val
                    best_type = "parallel"
                    best_pair = (r1, r2)
    
    return best, best_error, best_type, best_pair


# ==================== GUI Application ====================
class ResistorMatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resistor Value Matcher")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(4, weight=1)  # Output area expands
        self.root.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        # ===== Resistor Set Selection =====
        row = 0
        frame_set = tk.LabelFrame(self.root, text="Resistor Set", padx=10, pady=5)
        frame_set.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        frame_set.grid_columnconfigure(1, weight=1)
        
        self.resistor_var = tk.StringVar(value="E24")
        
        tk.Radiobutton(frame_set, text="E24 (5%)", variable=self.resistor_var, 
                       value="E24", command=self.on_resistor_set_changed).grid(row=0, column=0, padx=5, sticky="w")
        tk.Radiobutton(frame_set, text="E96 (1%)", variable=self.resistor_var, 
                       value="E96", command=self.on_resistor_set_changed).grid(row=0, column=1, padx=5, sticky="w")
        tk.Radiobutton(frame_set, text="Custom", variable=self.resistor_var, 
                       value="custom", command=self.on_resistor_set_changed).grid(row=0, column=2, padx=5, sticky="w")
        
        # ===== Custom Resistor Input (initially hidden) =====
        self.custom_frame = tk.LabelFrame(self.root, text="Custom Resistors (comma-separated)", padx=10, pady=5)
        self.custom_frame.grid(row=row+1, column=0, padx=10, pady=5, sticky="ew")
        self.custom_frame.grid_columnconfigure(0, weight=1)
        
        self.custom_text = tk.Text(self.custom_frame, height=5, wrap=tk.WORD, font=("Consolas", 10))
        self.custom_text.grid(row=0, column=0, sticky="ew")
        
        # Scrollbar for custom text
        scroll_custom = tk.Scrollbar(self.custom_frame, command=self.custom_text.yview)
        scroll_custom.grid(row=0, column=1, sticky="ns")
        self.custom_text.config(yscrollcommand=scroll_custom.set)
        
        # Insert default custom values
        self.custom_text.insert("1.0", get_default_custom_resistors())
        
        # Initially hide custom frame (not needed when E24 is selected)
        self.custom_frame.grid_remove()
        
        # ===== Target Resistors Input =====
        row = 2
        frame_target = tk.LabelFrame(self.root, text="Target Resistors (comma-separated, e.g., 1000, 2200, 4700)", padx=10, pady=5)
        frame_target.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        frame_target.grid_columnconfigure(0, weight=1)
        
        self.target_text = tk.Text(frame_target, height=4, wrap=tk.WORD, font=("Consolas", 10))
        self.target_text.grid(row=0, column=0, sticky="ew")
        
        # Scrollbar for target text
        scroll_target = tk.Scrollbar(frame_target, command=self.target_text.yview)
        scroll_target.grid(row=0, column=1, sticky="ns")
        self.target_text.config(yscrollcommand=scroll_target.set)
        
        # Insert default targets
        default_targets = "144700, 72300, 36200, 18100, 9050, 4520, 2260, 1130, 565, 10.001"
        self.target_text.insert("1.0", default_targets)
        
        # ===== Calculate Button =====
        row = 3
        frame_button = tk.Frame(self.root)
        frame_button.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
        
        self.calc_button = tk.Button(frame_button, text="Calculate", command=self.calculate, 
                                      bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=20, pady=5)
        self.calc_button.pack()
        
        # ===== Output Area =====
        row = 4
        frame_output = tk.LabelFrame(self.root, text="Results", padx=10, pady=5)
        frame_output.grid(row=row, column=0, padx=10, pady=5, sticky="nsew")
        frame_output.grid_columnconfigure(0, weight=1)
        frame_output.grid_rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(frame_output, wrap=tk.WORD, font=("Consolas", 10))
        self.output_text.grid(row=0, column=0, sticky="nsew")
        
        # Configure output text colors
        self.output_text.tag_config("error", foreground="red")
        self.output_text.tag_config("header", foreground="blue", font=("Consolas", 11, "bold"))
        self.output_text.tag_config("success", foreground="green")
        
        # Set initial focus to calculate button
        self.calc_button.focus_set()
        
    def on_resistor_set_changed(self):
        # """Handle resistor set selection change"""
        if self.resistor_var.get() == "custom":
            self.custom_frame.grid()
        else:
            self.custom_frame.grid_remove()
    
    def get_resistor_list(self):
        # """Get resistor list based on current selection"""
        set_type = self.resistor_var.get()
        
        if set_type == "E24":
            return get_e24_resistors()
        elif set_type == "E96":
            return get_e96_resistors()
        else:  # custom
            custom_str = self.custom_text.get("1.0", tk.END).strip()
            if not custom_str:
                raise ValueError("Custom resistor list cannot be empty")
            return parse_custom_resistors(custom_str)
    
    def calculate(self):
        # """Main calculation routine"""
        # Clear output
        self.output_text.delete("1.0", tk.END)
        
        try:
            # Get resistor list
            resistors = self.get_resistor_list()
            self.output_text.insert(tk.END, f"Resistor set: {self.resistor_var.get()}", "header")
            self.output_text.insert(tk.END, f" (Total: {len(resistors)} values)\n\n")
            
            # Parse targets
            targets_str = self.target_text.get("1.0", tk.END).strip()
            if not targets_str:
                raise ValueError("Target resistors cannot be empty")
            
            targets = parse_targets(targets_str)
            self.output_text.insert(tk.END, f"Number of targets: {len(targets)}\n")
            self.output_text.insert(tk.END, "="*60 + "\n\n")
            
            # Calculate for each target
            for i, target in enumerate(targets, start=1):
                best_val, error, typ, pair = find_best(target, resistors)
                
                self.output_text.insert(tk.END, f"[{i}] Target: {target:.6f} Ohm\n")
                
                if typ == "single":
                    self.output_text.insert(tk.END, f"    Best: {pair[0]} Ohm (single)\n")
                elif typ == "series":
                    self.output_text.insert(tk.END, f"    Best: {pair[0]} + {pair[1]} = {best_val:.6f} Ohm (series)\n")
                else:  # parallel
                    self.output_text.insert(tk.END, f"    Best: {pair[0]} // {pair[1]} = {best_val:.6f} Ohm (parallel)\n")
                
                # Format error with color
                error_pct = error * 100
                if error_pct < 0.1:
                    self.output_text.insert(tk.END, f"    Error: {error_pct:.4f}%\n\n", "success")
                else:
                    self.output_text.insert(tk.END, f"    Error: {error_pct:.4f}%\n\n")
            
            self.output_text.insert(tk.END, "="*60 + "\n")
            self.output_text.insert(tk.END, "Calculation completed.", "header")
            
        except ValueError as e:
            self.output_text.insert(tk.END, f"ERROR: {str(e)}\n", "error")
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            self.output_text.insert(tk.END, f"Unexpected error: {str(e)}\n", "error")
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")


# ==================== Main Entry Point ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = ResistorMatcherApp(root)
    root.mainloop()