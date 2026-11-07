import customtkinter as ctk
import math

# 1. ATUR TEMA GLOBAL
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# ==========================================
# LOGIC LAYER (OTAK KALKULATOR)
# ==========================================
class KalkulatorEngine:
    @staticmethod
    def hitung(ekspresi: str) -> str:
        try:
            # 1. Ubah koma (UI) menjadi titik (Python)
            clean_expr = ekspresi.replace(',', '.')
            
            # 2. Merapikan operator & fungsi
            clean_expr = clean_expr.replace('×', '*').replace('÷', '/')
            clean_expr = clean_expr.replace('π', 'math.pi').replace('e', 'math.e')
            
            clean_expr = clean_expr.replace('sin(', 'math.sin(math.radians(')
            clean_expr = clean_expr.replace('cos(', 'math.cos(math.radians(')
            clean_expr = clean_expr.replace('tan(', 'math.tan(math.radians(')
            
            clean_expr = clean_expr.replace('sqrt(', 'math.sqrt(')
            clean_expr = clean_expr.replace('log(', 'math.log10(')
            clean_expr = clean_expr.replace('^', '**')

            allowed_globals = {"math": math}
            hasil = eval(clean_expr, {"__builtins__": None}, allowed_globals)
            
            if isinstance(hasil, float) and hasil.is_integer():
                hasil = int(hasil)
                
            # 3. Bulatkan hasil dan ubah titik kembali menjadi koma untuk UI
            hasil_str = str(round(hasil, 8)).replace('.', ',')
            return hasil_str
            
        except ZeroDivisionError:
            return "Error: Bagi 0"
        except Exception:
            return "Syntax Error"


# ==========================================
# UI LAYER (TAMPILAN & LAYOUT)
# ==========================================
class KalkulatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Kalkulator Saintifik")
        self.geometry("380x560")
        
        # Background utama
        self.configure(fg_color="#1e1e2e")

        self.engine = KalkulatorEngine()

        # Layar Display
        self.display = ctk.CTkEntry(
            self, 
            font=("Arial", 28, "bold"), 
            justify="right", 
            height=70,
            fg_color="#181825",
            text_color="#cdd6f4",
            border_color="#313244",
            border_width=2
        )
        self.display.pack(fill="x", padx=15, pady=(20, 10))

        # Frame Wadah Tombol
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # SUSUNAN TOMBOL SESUAI GAMBAR (Menggunakan Koma)
        self.tombol_list = [
            ['C', '(', ')', '^'],
            ['7', '8', '9', '÷'],
            ['4', '5', '6', '×'],
            ['1', '2', '3', '-'],
            ['sqrt', '0', ',', '+'],
            ['sin', 'cos', 'tan', '=']
        ]

        self.buat_tombol()

    def buat_tombol(self):
        for baris_idx, baris in enumerate(self.tombol_list):
            self.grid_frame.rowconfigure(baris_idx, weight=1)
            
            for kolom_idx, teks in enumerate(baris):
                self.grid_frame.columnconfigure(kolom_idx, weight=1)
                
                # --- SKEMA WARNA DENGAN KUNING SOFT SESUAI TAMPILAN ---
                if teks == '=':
                    bg_color = "#a6e3a1"      # Hijau Aksen
                    hover = "#94e2d5"
                    txt_color = "#11111b"
                elif teks == 'C':
                    bg_color = "#f38ba8"      # Merah Clear
                    hover = "#eb6f92"
                    txt_color = "#11111b"
                elif teks in ['÷', '×', '-', '+', '^', '(', ')']:
                    bg_color = "#89b4fa"      # Biru Operator
                    hover = "#74c7ec"
                    txt_color = "#11111b"
                else:
                    # ANGKA, KOMA, & FUNGSI SAINTIFIK -> KUNING SOFT (#f9e2af)
                    bg_color = "#f9e2af"
                    hover = "#f5e0dc"
                    txt_color = "#11111b"

                btn = ctk.CTkButton(
                    self.grid_frame,
                    text=teks,
                    font=("Arial", 16, "bold"),
                    fg_color=bg_color,
                    hover_color=hover,
                    text_color=txt_color,
                    corner_radius=10,
                    command=lambda t=teks: self.tombol_ditekan(t)
                )
                btn.grid(row=baris_idx, column=kolom_idx, padx=4, pady=4, sticky="nsew")

    def tombol_ditekan(self, nilai):
        teks_sekarang = self.display.get()

        if nilai == 'C':
            self.display.delete(0, 'end')
        elif nilai == '=':
            hasil = self.engine.hitung(teks_sekarang)
            self.display.delete(0, 'end')
            self.display.insert(0, hasil)
        elif nilai in ['sin', 'cos', 'tan', 'sqrt']:
            # Otomatis menambahkan kurung buka saat menekan fungsi saintifik
            self.display.insert('end', nilai + '(')
        else:
            self.display.insert('end', nilai)


if __name__ == "__main__":
    app = KalkulatorApp()
    app.mainloop()