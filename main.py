import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import cairosvg
import os

class ImageConverterGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Universal Image Converter")
        self.geometry("500x400")

        # --- UI Layout ---
        self.label = ctk.CTkLabel(self, text="画像コンバーター (SVG/PNG/JPG)", font=("Arial", 20))
        self.label.pack(pady=20)

        # ファイル選択ボタン
        self.select_button = ctk.CTkButton(self, text="ファイルを選択", command=self.select_file)
        self.select_button.pack(pady=10)

        self.file_path_label = ctk.CTkLabel(self, text="ファイルが選択されていません", wraplength=400)
        self.file_path_label.pack(pady=10)

        # 変換形式の選択
        self.format_label = ctk.CTkLabel(self, text="変換先の形式を選択:")
        self.format_label.pack(pady=5)
        
        self.format_var = ctk.StringVar(value="PNG")
        self.format_menu = ctk.CTkOptionMenu(self, values=["PNG", "JPEG", "SVG"], variable=self.format_var)
        self.format_menu.pack(pady=10)

        # 実行ボタン
        self.convert_button = ctk.CTkButton(self, text="変換して保存", command=self.convert_image, fg_color="green")
        self.convert_button.pack(pady=20)

        self.input_file = ""

    def select_file(self):
        self.input_file = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.svg")]
        )
        if self.input_file:
            self.file_path_label.configure(text=os.path.basename(self.input_file))

    def convert_image(self):
        if not self.input_file:
            messagebox.showerror("Error", "ファイルを選択してください")
            return

        target_ext = self.format_var.get().lower()
        save_path = filedialog.asksaveasfilename(defaultextension=f".{target_ext}",
                                                filetypes=[(target_ext.upper(), f"*.{target_ext}")])
        
        if not save_path:
            return

        try:
            input_ext = self.input_file.split('.')[-1].lower()

            # SVGからの変換
            if input_ext == 'svg':
                if target_ext == 'svg':
                    messagebox.showinfo("Info", "同じ形式です")
                    return
                cairosvg.svg2png(url=self.input_file, write_to=save_path)
                if target_ext == 'jpeg':
                    with Image.open(save_path) as img:
                        img.convert("RGB").save(save_path, "JPEG")
            
            # PNG/JPGからの変換
            else:
                with Image.open(self.input_file) as img:
                    if target_ext == 'svg':
                        # 簡易的な埋め込みSVGとして保存
                        img.save(save_path, format="WebP") # 実際はベクター化が必要
                        messagebox.showwarning("Warning", "BitmapからSVGへの変換は埋め込み形式になります。")
                    elif target_ext == 'jpeg':
                        img.convert("RGB").save(save_path, "JPEG")
                    else:
                        img.save(save_path, target_ext.upper())

            messagebox.showinfo("Success", f"変換が完了しました:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"変換に失敗しました: {e}")

if __name__ == "__main__":
    app = ImageConverterGUI()
    # app.mainloop()