#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Rotator — Batch rotate all pages of a PDF file
https://github.com/YOUR_USERNAME/pdf-rotator
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

try:
    import fitz
    PYMUPDF_OK = True
except ImportError:
    PYMUPDF_OK = False

C = {
    "bg":     "#1a1208",
    "bg2":    "#221a0e",
    "bg3":    "#2c2010",
    "border": "#4a3820",
    "sepia":  "#c8a96e",
    "text":   "#e8d8b0",
    "accent": "#8b2e0a",
}


class PDFRotator:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Rotator")
        self.root.geometry("520x500")
        self.root.minsize(480, 480)
        self.root.resizable(True, True)
        self.root.configure(bg=C["bg"])

        self.pdf_path = tk.StringVar()
        self.rotation = tk.IntVar(value=90)

        self._build_ui()

        if not PYMUPDF_OK:
            messagebox.showerror(
                "Missing dependency",
                "PyMuPDF is not installed.\n\n"
                "Please run:\n  pip install PyMuPDF"
            )
            self.root.destroy()

    def _build_ui(self):
        # ── Header ────────────────────────────
        hdr = tk.Frame(self.root, bg=C["bg2"], height=100)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="🔄", bg=C["bg2"], fg=C["sepia"],
                 font=("Georgia", 28)).pack(side="left", padx=20, pady=16)

        hf = tk.Frame(hdr, bg=C["bg2"])
        hf.pack(side="left", pady=16)
        tk.Label(hf, text="PDF Rotator",
                 bg=C["bg2"], fg=C["text"],
                 font=("Georgia", 18, "bold")).pack(anchor="w")
        tk.Label(hf, text="Rotate all pages of a PDF in one click",
                 bg=C["bg2"], fg=C["sepia"],
                 font=("Georgia", 10, "italic")).pack(anchor="w", pady=(2, 0))
        tk.Label(hf, text="Requires Python 3.10+  ·  pip install PyMuPDF",
                 bg=C["bg2"], fg="#4a3820",
                 font=("Georgia", 9)).pack(anchor="w")

        tk.Frame(self.root, bg=C["border"], height=1).pack(fill="x")

        # ── Main area ─────────────────────────
        main = tk.Frame(self.root, bg=C["bg"])
        main.pack(fill="both", expand=True, padx=25, pady=20)

        # Step 1 — choose file
        tk.Label(main, text="1.  Choose a PDF file:",
                 bg=C["bg"], fg=C["sepia"],
                 font=("Georgia", 11, "bold")).pack(anchor="w", pady=(0, 8))

        file_frame = tk.Frame(main, bg=C["bg3"])
        file_frame.pack(fill="x", pady=(0, 10))
        self.file_label = tk.Label(file_frame,
                                    text="No file selected",
                                    bg=C["bg3"], fg="#7a6040",
                                    font=("Georgia", 10),
                                    anchor="w", padx=12, pady=10)
        self.file_label.pack(fill="x")

        tk.Button(main, text="📂  Browse PDF…",
                  bg=C["bg3"], fg=C["text"],
                  activebackground=C["border"],
                  relief="flat", bd=0,
                  font=("Georgia", 11),
                  padx=15, pady=8,
                  cursor="hand2",
                  command=self._choose_file).pack(anchor="w", pady=(0, 22))

        # Step 2 — choose rotation
        tk.Label(main, text="2.  Choose rotation direction:",
                 bg=C["bg"], fg=C["sepia"],
                 font=("Georgia", 11, "bold")).pack(anchor="w", pady=(0, 10))

        rot_frame = tk.Frame(main, bg=C["bg"])
        rot_frame.pack(anchor="w", pady=(0, 22))

        rotations = [
            ( 90, "↻  90° clockwise          (fix text rotated left  ←)"),
            (-90, "↺  90° counter-clockwise  (fix text rotated right →)"),
            (180, "↻↻  180°  (flip upside-down)"),
        ]
        for deg, label in rotations:
            tk.Radiobutton(rot_frame, text=label,
                            variable=self.rotation, value=deg,
                            bg=C["bg"], fg=C["text"],
                            selectcolor=C["bg3"],
                            activebackground=C["bg"],
                            activeforeground=C["sepia"],
                            font=("Georgia", 10)).pack(anchor="w", pady=3)

        # Step 3 — rotate button
        tk.Label(main, text="3.  Save rotated PDF:",
                 bg=C["bg"], fg=C["sepia"],
                 font=("Georgia", 11, "bold")).pack(anchor="w", pady=(0, 8))

        tk.Button(main, text="🔄  Rotate & Save",
                  bg=C["accent"], fg="#f0e0c0",
                  activebackground="#c04020",
                  activeforeground="#ffffff",
                  relief="flat", bd=0,
                  font=("Georgia", 12, "bold"),
                  padx=20, pady=12,
                  cursor="hand2",
                  command=self._rotate).pack(fill="x", pady=(0, 10))

        tk.Label(main,
                 text="Output file will be saved as  original_name_rotated.pdf",
                 bg=C["bg"], fg="#7a6040",
                 font=("Georgia", 9, "italic")).pack(anchor="w")

    def _choose_file(self):
        path = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if path:
            self.pdf_path.set(path)
            self.file_label.configure(text=Path(path).name, fg=C["text"])

    def _rotate(self):
        if not self.pdf_path.get():
            messagebox.showwarning("No file selected",
                                   "Please choose a PDF file first.")
            return

        src_path = Path(self.pdf_path.get())
        dst_path = src_path.parent / f"{src_path.stem}_rotated.pdf"
        rotation = self.rotation.get()

        try:
            doc = fitz.open(str(src_path))
            for page in doc:
                page.set_rotation(rotation)
            page_count = len(doc)
            doc.save(str(dst_path))
            doc.close()

            messagebox.showinfo(
                "Done!",
                f"PDF rotated successfully!\n\n"
                f"Saved as:\n{dst_path.name}\n\n"
                f"Pages processed: {page_count}"
            )

            # Reset
            self.pdf_path.set("")
            self.file_label.configure(text="No file selected", fg="#7a6040")

        except Exception as e:
            messagebox.showerror("Error",
                f"Could not rotate PDF:\n\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap("icon.ico")
    except Exception:
        pass
    PDFRotator(root)
    root.mainloop()
