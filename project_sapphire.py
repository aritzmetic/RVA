import tkinter as tk
from tkinter import ttk
import time
import threading
import random
import datetime

# --- MOVIE PROP CONFIGURATION ---
TARGET_NAME = "Tina Mercado" # The name from your script
# TARGET_NAME = "Tina Mercado" # (Or use this if you changed the character)

# --- CYBERPUNK COLOR PALETTE ---
COLOR_BG = "#020202"           # Pure Black
COLOR_PANEL = "#0b1016"        # Dark Blue-Grey
COLOR_VILLAREAL = "#00f0ff"    # Cyan (The "Good" / Winning Color)
COLOR_ALCEDO = "#ff1a1a"       # Red (The "Bad" / Losing Color)
COLOR_TEXT_MAIN = "#ffffff"
COLOR_TEXT_DIM = "#445566"
COLOR_ACCENT = "#ffd700"       # Gold/Yellow for warnings

FONT_HEADER = ("Impact", 35)
FONT_TECH = ("Consolas", 12)
FONT_NUMBERS = ("Consolas", 48, "bold")

class HighTechDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("PROJECT SAPPHIRE // COMMAND")
        self.root.configure(bg=COLOR_BG)
        
        # FULLSCREEN MODE (Press ESC to exit)
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))
        
        self.is_running = False
        self.map_blocks = [] 
        self.graph_bars = []
        
        self.setup_layout()
        self.start_animations()
        self.initial_boot_sequence()

    def setup_layout(self):
        # MAIN CONTAINER
        main = tk.Frame(self.root, bg=COLOR_BG)
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # --- HEADER ---
        header = tk.Frame(main, bg=COLOR_BG)
        header.pack(fill=tk.X, pady=(0, 20))
        
        # Spaced out cinematic title
        tk.Label(header, text="P R O J E C T   S A P P H I R E", font=FONT_HEADER, fg=COLOR_VILLAREAL, bg=COLOR_BG).pack(side=tk.LEFT)
        
        self.clock_lbl = tk.Label(header, text="00:00:00", font=("Consolas", 20), fg=COLOR_TEXT_DIM, bg=COLOR_BG)
        self.clock_lbl.pack(side=tk.RIGHT)
        
        # Decorative Header Line
        tk.Frame(header, bg=COLOR_VILLAREAL, height=3).pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        # --- CONTENT AREA (3 COLUMNS) ---
        content = tk.Frame(main, bg=COLOR_BG)
        content.pack(fill=tk.BOTH, expand=True)

        # COL 1: NETWORK TRAFFIC (Visual Noise)
        col1 = tk.Frame(content, bg=COLOR_PANEL, width=200)
        col1.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        col1.pack_propagate(False) # Force width
        
        tk.Label(col1, text="NET_TRAFFIC", font=("Consolas", 10, "bold"), fg=COLOR_TEXT_DIM, bg=COLOR_PANEL).pack(pady=10)
        self.traffic_canvas = tk.Canvas(col1, bg=COLOR_PANEL, highlightthickness=0)
        self.traffic_canvas.pack(fill=tk.BOTH, expand=True, padx=10)
        self.setup_traffic_graph() # Draw the fake graph bars

        # COL 2: THE MAP (Center Stage)
        col2 = tk.Frame(content, bg=COLOR_PANEL, highlightbackground=COLOR_VILLAREAL, highlightthickness=1)
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Map Header
        map_header = tk.Frame(col2, bg=COLOR_PANEL)
        map_header.pack(fill=tk.X, padx=15, pady=15)
        tk.Label(map_header, text="TARGET ZONE: AREA 4", font=("Consolas", 16, "bold"), fg="white", bg=COLOR_PANEL).pack(side=tk.LEFT)
        self.status_lbl = tk.Label(map_header, text="STATUS: CONTESTED", font=("Consolas", 12, "bold"), fg=COLOR_ALCEDO, bg=COLOR_PANEL)
        self.status_lbl.pack(side=tk.RIGHT)

        # The Grid Canvas
        self.map_canvas = tk.Canvas(col2, bg="#05080a", highlightthickness=0)
        self.map_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.draw_grid()

        # Percentage Overlay
        self.percent_lbl = tk.Label(col2, text="18.2%", font=FONT_NUMBERS, fg=COLOR_ALCEDO, bg=COLOR_PANEL)
        self.percent_lbl.pack(pady=(0, 10))
        tk.Label(col2, text="VILLAREAL SHARE", font=FONT_TECH, fg=COLOR_TEXT_DIM, bg=COLOR_PANEL).pack(pady=(0, 20))

        # COL 3: LOGS & ACTION
        col3 = tk.Frame(content, bg=COLOR_BG, width=400)
        col3.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        col3.pack_propagate(False)

        # Terminal
        term_frame = tk.Frame(col3, bg="black", highlightthickness=1, highlightbackground="#333")
        term_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        tk.Label(term_frame, text=">_ SYSTEM_LOG", font=("Consolas", 8), fg="#666", bg="black").pack(anchor=tk.W)
        self.log_box = tk.Text(term_frame, bg="black", fg="#00ff00", font=("Consolas", 10), bd=0, highlightthickness=0)
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # The Big Button
        self.btn_frame = tk.Frame(col3, bg=COLOR_ALCEDO, padx=2, pady=2)
        self.btn_frame.pack(fill=tk.X)
        self.action_btn = tk.Button(self.btn_frame, text="INITIATE BATCH [ENTER]", 
                                    font=("Consolas", 14, "bold"), bg="black", fg=COLOR_ALCEDO,
                                    activebackground=COLOR_ALCEDO, activeforeground="black",
                                    bd=0, cursor="hand2", command=self.start_sequence)
        self.action_btn.pack(fill=tk.BOTH, ipady=15)

        # Binds
        self.root.bind('<Return>', lambda e: self.start_sequence())

    # --- ANIMATIONS & DRAWING ---

    def setup_traffic_graph(self):
        # Create 15 vertical bars for visual noise
        w = 180
        bar_w = w / 15
        for i in range(15):
            x1 = i * bar_w
            y1 = 300 # Start at bottom
            x2 = x1 + (bar_w - 2)
            y2 = 300
            bar_id = self.traffic_canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_TEXT_DIM, outline="")
            self.graph_bars.append(bar_id)

    def draw_grid(self):
        # Draw the map squares
        rows, cols = 10, 14
        w, h = 40, 40
        gap = 4
        start_x, start_y = 20, 20
        
        self.map_blocks = []
        for r in range(rows):
            for c in range(cols):
                x1 = start_x + c * (w + gap)
                y1 = start_y + r * (h + gap)
                x2 = x1 + w
                y2 = y1 + h
                
                # Mostly Red initially
                is_hostile = random.random() > 0.18
                color = COLOR_ALCEDO if is_hostile else COLOR_VILLAREAL
                outline = "#440000" if is_hostile else "#004444"
                
                rid = self.map_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=outline, width=2)
                self.map_blocks.append({"id": rid, "hostile": is_hostile, "x": x1, "y": y1})

    def start_animations(self):
        # 1. Clock
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_lbl.config(text=now)
        
        # 2. Animate Traffic Graph (Randomly change heights)
        h = self.traffic_canvas.winfo_height()
        if h < 100: h = 300 # Fallback if not rendered yet
        
        for bar in self.graph_bars:
            new_h = random.randint(10, int(h * 0.8))
            coords = self.traffic_canvas.coords(bar)
            # coords is [x1, y1, x2, y2]. We change y1.
            self.traffic_canvas.coords(bar, coords[0], h - new_h, coords[2], h)
            # Randomly color them cyan or dim
            color = COLOR_VILLAREAL if random.random() > 0.8 else "#223344"
            self.traffic_canvas.itemconfig(bar, fill=color)

        self.root.after(100, self.start_animations) # Loop every 0.1s

    def log(self, text, alert=False):
        self.log_box.insert(tk.END, f"> {text}\n")
        if alert:
            self.log_box.tag_add("alert", "end-2l", "end-1c")
            self.log_box.tag_config("alert", foreground=COLOR_ALCEDO, background="#220000")
        self.log_box.see(tk.END)

    def initial_boot_sequence(self):
        self.log("SYSTEM BOOT_SEQ_99...")
        self.root.after(500, lambda: self.log("ENCRYPTING CONNECTION..."))
        self.root.after(1000, lambda: self.log("LOADING GEOSPATIAL DATA [AREA 4]..."))
        self.root.after(1500, lambda: self.log("WARNING: ANOMALOUS VOTER PATTERNS.", True))

    # --- THE MAIN ACTION SEQUENCE ---

    def start_sequence(self):
        if self.is_running: return
        self.is_running = True
        self.action_btn.config(text="PROCESSING...", fg="white", bg="#333")
        
        # Start the logic thread
        threading.Thread(target=self.run_logic).start()

    def run_logic(self):
        self.log("--- INITIATING PROTOCOL SOBRE ---")
        time.sleep(1)
        self.log("BYPASSING BANKING GATEWAYS...")
        time.sleep(0.5)
        self.log("INJECTING FUNDS (PHP 1,500/HEAD)...")
        time.sleep(0.5)
        
        # 1. THE SCAN EFFECT (Visual Eye Candy)
        # Create a line that moves down the map
        self.log("SCANNING RECIPIENTS...")
        
        # We need to do UI updates on the main thread
        self.root.after(0, self.animate_scan_line)

    def animate_scan_line(self):
        # Draw a cyan line
        width = self.map_canvas.winfo_width()
        scan_line = self.map_canvas.create_line(0, 0, width, 0, fill=COLOR_VILLAREAL, width=4)
        
        # Animate it moving down
        def step(y):
            if y > self.map_canvas.winfo_height():
                self.map_canvas.delete(scan_line)
                # AFTER SCAN FINISHES, START FLIPPING
                threading.Thread(target=self.run_flip_sequence).start()
                return
            
            self.map_canvas.coords(scan_line, 0, y, width, y)
            self.root.after(10, lambda: step(y + 10)) # Speed of scan
            
        step(0)

    def run_flip_sequence(self):
        # 2. THE FLIP EFFECT (Data rewriting)
        total_blocks = len(self.map_blocks)
        converted = 0
        indices = list(range(total_blocks))
        random.shuffle(indices)
        
        for i in indices:
            block = self.map_blocks[i]
            if block["hostile"]:
                time.sleep(random.uniform(0.005, 0.05)) # Fast ripples
                
                # Visual Flip to Cyan
                self.map_canvas.itemconfig(block["id"], fill=COLOR_VILLAREAL, outline="#004444")
                
                converted += 1
                
                # Math for the percentage label
                current_perc = 18.2 + (converted / total_blocks * 81.8)
                if current_perc > 100: current_perc = 100
                
                # Update UI
                self.root.after(0, lambda p=current_perc: self.update_stats(p))

        time.sleep(0.5)
        self.log("TRANSFER COMPLETE.", False)
        self.log("AREA 4 SECURED.", False)
        self.root.after(800, self.show_victory_popup)

    def update_stats(self, percent):
        self.percent_lbl.config(text=f"{percent:.1f}%", fg=COLOR_VILLAREAL)
        if percent > 60:
             self.status_lbl.config(text="STATUS: SECURING...", fg=COLOR_ACCENT)
        if percent > 95:
             self.status_lbl.config(text="STATUS: VILLAREAL DOMINANT", fg=COLOR_VILLAREAL)
             self.action_btn.config(text="OPERATION SUCCESS", bg=COLOR_VILLAREAL, fg="black")

    def show_victory_popup(self):
        top = tk.Toplevel(self.root)
        top.overrideredirect(True)
        
        # Center it
        w, h = 600, 350
        x = self.root.winfo_screenwidth() // 2 - (w // 2)
        y = self.root.winfo_screenheight() // 2 - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")
        
        top.configure(bg=COLOR_PANEL, highlightbackground=COLOR_VILLAREAL, highlightthickness=4)
        
        # Content
        tk.Label(top, text="TRANSACTION VERIFIED", font=("Impact", 28), fg=COLOR_VILLAREAL, bg=COLOR_PANEL).pack(pady=25)
        
        info_frame = tk.Frame(top, bg=COLOR_PANEL)
        info_frame.pack(fill=tk.X, padx=40)
        
        tk.Label(info_frame, text=f"RECIPIENT: {TARGET_NAME}", font=("Consolas", 18, "bold"), fg="white", bg=COLOR_PANEL).pack(anchor=tk.W)
        tk.Label(info_frame, text="AMOUNT:    PHP 1,500.00", font=("Consolas", 18), fg=COLOR_ACCENT, bg=COLOR_PANEL).pack(anchor=tk.W)
        tk.Label(info_frame, text="TAG:       MEDICAL AID / EDUCATIONAL", font=("Consolas", 12), fg=COLOR_TEXT_DIM, bg=COLOR_PANEL).pack(anchor=tk.W, pady=5)

        tk.Label(top, text="STATUS: FUNDS RELEASED", font=("Consolas", 14, "bold"), fg="#00ff00", bg=COLOR_PANEL).pack(side=tk.BOTTOM, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = HighTechDashboard(root)
    root.mainloop()