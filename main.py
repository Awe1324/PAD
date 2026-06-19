import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps, ImageDraw

root = tk.Tk()
root.title("Portfolio Pengguna")
root.geometry("450x600") 
root.configure(bg="#F1F5F9") 


def create_circle_image(path, size=(130, 130)):
    try:
        img = Image.open(path).convert("RGBA")
        img = img.resize(size, Image.Resampling.LANCZOS)
        
        # Membuat mask bulat sempurna dengan anti-aliasing yang halus
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        
        output = Image.new('RGBA', size, (0, 0, 0, 0))
        output.paste(img, (0, 0), mask=mask)
        
        return ImageTk.PhotoImage(output)
    except Exception as e:
        print(f"Gagal memuat foto: {e}")
        return None

# --- EFEK BAYANGAN KARTU (Subtle Shadow Effect) ---
shadow_frame = tk.Frame(root, bg="#E2E8F0")
shadow_frame.place(relx=0.5, rely=0.5, anchor="center", width=364, height=484)

# --- KARTU PROFIL UTAMA (White Premium Card) ---
main_card = tk.Frame(root, bg="white", padx=30, pady=30)
main_card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=480)

# --- FOTO PROFIL ---
photo = create_circle_image("image.jpeg") # Nama file fotomu
if photo:
    label_foto = tk.Label(main_card, image=photo, bg="white")
    label_foto.pack(pady=(10, 15))
else:
    avatar_frame = tk.Frame(main_card, bg="#EEF2F6", width=120, height=120)
    avatar_frame.pack_propagate(False)
    avatar_frame.pack(pady=(10, 15))
    tk.Label(avatar_frame, text="HM", font=("Segoe UI", 28, "bold"), fg="#6366F1", bg="#EEF2F6").place(relx=0.5, rely=0.5, anchor="center")

# --- NAMA UTAMA & BADGE UTAMA ---
tk.Label(main_card, text="Bahliul", font=("Segoe UI", 18, "bold"), fg="#0F172A", bg="white").pack()

badge = tk.Label(main_card, text="  ✓ SOFTWARE ENGINEER  ", font=("Segoe UI", 8, "bold"), fg="#4338CA", bg="#E0E7FF", pady=3)
badge.pack(pady=(5, 25))

# Garis Pembatas Minimalis (Separator)
separator = tk.Frame(main_card, bg="#F1F5F9", height=2)
separator.pack(fill="x", pady=(0, 20))

# --- INFO BIODATA GRID LAYOUT ---
info_container = tk.Frame(main_card, bg="white")
info_container.pack(fill="x")

info_data = [
    {"label": "PEKERJAAN", "val": "Programmer"},
    {"label": "LOKASI", "val": "Indonesia"},
    {"label": "HOBI", "val": "Coding & Tech"},
    {"label": "KONTAK", "val": "@ethanol"}
]

for i, data in enumerate(info_data):
    row_idx = i // 2
    col_idx = i % 2
    
    cell = tk.Frame(info_container, bg="white")
    # Bagian ini sudah diperbaiki (expand=True dihapus)
    cell.grid(row=row_idx, column=col_idx, sticky="w", padx=15, pady=10)
    
    tk.Label(cell, text=data["label"], font=("Segoe UI", 8, "bold"), fg="#94A3B8", bg="white").pack(anchor="w")
    tk.Label(cell, text=data["val"], font=("Segoe UI", 11, "bold"), fg="#334155", bg="white").pack(anchor="w", pady=(2, 0))

root.mainloop()