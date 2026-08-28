import tkinter as tk
from tkinter import filedialog, messagebox
import analyzer  # This connects your GUI to your engine!

def select_and_analyze():
    """Opens a file explorer, selects an image, and runs the forensic engine."""
    # 1. Open the file dialog window
    filepath = filedialog.askopenfilename(
        title="Select Forensic Evidence",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    
    # 2. If the user selects a file (and doesn't hit cancel)
    if filepath:
        print(f"\n[+] GUI Initiated Analysis for: {filepath}")
        try:
            # 3. Pass the file directly to your analyzer script
            analyzer.analyze_image(filepath)
            
            # 4. Show a popup window confirming success
            messagebox.showinfo(
                "Analysis Complete", 
                f"Successfully extracted data from:\n{filepath}\n\nCheck terminal for raw dumps and evidence_log.csv for the ledger."
            )
        except Exception as e:
            messagebox.showerror("Engine Error", f"An error occurred: {e}")

# ==========================================
# UI DESIGN SECTION
# ==========================================

# Create the main window
root = tk.Tk()
root.title("Forensic Image Analyzer")
root.geometry("450x250")
root.configure(bg="#1e1e1e") # Dark mode background

# Add a Title Label
title_label = tk.Label(
    root, 
    text="EXIF & Metadata Extractor", 
    font=("Helvetica", 16, "bold"), 
    fg="#ffffff", 
    bg="#1e1e1e"
)
title_label.pack(pady=30)

# Add the "Select Evidence" Button
scan_btn = tk.Button(
    root, 
    text="Select Image Evidence", 
    font=("Helvetica", 12, "bold"), 
    bg="#007acc", 
    fg="white", 
    padx=20, 
    pady=10,
    command=select_and_analyze
)
scan_btn.pack(pady=10)

# Add a small footer label
footer_label = tk.Label(
    root, 
    text="Output logged to evidence_log.csv", 
    font=("Helvetica", 9, "italic"), 
    fg="#888888", 
    bg="#1e1e1e"
)
footer_label.pack(side="bottom", pady=20)

# Keep the window running
root.mainloop()