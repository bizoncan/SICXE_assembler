import tkinter as tk
import subprocess
import os

# Dosyadan içeriği okuyup geri döndüren yardımcı bir işlev
def read_file_content(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        content = file.read()
    return content

# Çalıştırılacak fonksiyon
def run_program():
    user_input = text_area.get("1.0", tk.END).strip()
    
    with open("source_code.txt", "w", encoding="utf-8") as file:
        file.write("")
    
    # Kullanıcı girdisini "source_code.txt" dosyasına kaydet
    with open("source_code.txt", "w", encoding="utf-8") as file:
        file.write(user_input)
   
    
    subprocess.run(["python", "pass1.py"])
    
    # "pass2.py" dosyasını çalıştır
    subprocess.run(["python", "pass2.py"])
    # Dosyaların içeriğini oku
    object_program_content = read_file_content("object_program.txt")
    lit_tab_content = read_file_content("lit_tab.txt")
    symtab_content = read_file_content("symtab.txt")
    block_tab_content = read_file_content("block_tab.txt")
    object_code_content = read_file_content("object_code.txt")
    error_content = read_file_content("hata.txt")
    # Çıktı alanlarına içeriği yaz
    output_text1.config(state=tk.NORMAL)
    output_text1.delete("1.0", tk.END)
    output_text1.insert(tk.END, f"Object Program:\n{object_program_content}")
    output_text1.config(state=tk.DISABLED)
    
    output_text2.config(state=tk.NORMAL)
    output_text2.delete("1.0", tk.END)
    output_text2.insert(tk.END, f"Literal Tablosu:\n{lit_tab_content}")
    output_text2.config(state=tk.DISABLED)

    output_text3.config(state=tk.NORMAL)
    output_text3.delete("1.0", tk.END)
    output_text3.insert(tk.END, f"Sembol Tablosu:\nVALUE NAME BLOCK R/A\n{symtab_content}")
    output_text3.config(state=tk.DISABLED)

    output_text4.config(state=tk.NORMAL)
    output_text4.delete("1.0", tk.END)
    output_text4.insert(tk.END, f"Blok Tablosu:\n{block_tab_content}")
    output_text4.config(state=tk.DISABLED)

    output_text5.config(state=tk.NORMAL)
    output_text5.delete("1.0", tk.END)
    output_text5.insert(tk.END, f"Object Code:\n{object_code_content}")
    output_text5.config(state=tk.DISABLED)
    
    
    output_text6.config(state=tk.NORMAL)
    output_text6.delete("1.0", tk.END)
    output_text6.insert(tk.END, f"hata:\n{error_content}")
    output_text6.config(state=tk.DISABLED)
   
# Ana uygulama penceresi
app = tk.Tk()
app.title("SIC/XE ASSEMBLER")
app.geometry("1280x720")  # Pencere boyutunu ayarla
app.config(bg="darkgray")

# Üstteki çok satırlı metin giriş alanı
text_area = tk.Text(app, height=10, width=120)
text_area.pack(pady=10)

# Ortadaki "Çalıştır" butonu
run_button = tk.Button(app, text="Çalıştır", command=run_program)
run_button.pack(pady=10)

# Ana çıktı alanı
output_frame1 = tk.Frame(app)
output_frame1.pack(pady=10)
output_text1 = tk.Text(output_frame1, width=120, height=5, bg="lightgray", state=tk.DISABLED)
scrollbar1 = tk.Scrollbar(output_frame1, command=output_text1.yview)
output_text1.config(yscrollcommand=scrollbar1.set)
output_text1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

# Üç küçük çıktı alanı
small_output_frame = tk.Frame(app)
small_output_frame.pack()

output_frame2 = tk.Frame(small_output_frame)
output_frame2.pack(side=tk.LEFT, padx=5, pady=5)
output_text2 = tk.Text(output_frame2, width=40, height=5, bg="lightgray", state=tk.DISABLED)
scrollbar2 = tk.Scrollbar(output_frame2, command=output_text2.yview)
output_text2.config(yscrollcommand=scrollbar2.set)
output_text2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

output_frame3 = tk.Frame(small_output_frame)
output_frame3.pack(side=tk.LEFT, padx=5, pady=5)
output_text3 = tk.Text(output_frame3, width=40, height=5, bg="lightgray", state=tk.DISABLED)
scrollbar3 = tk.Scrollbar(output_frame3, command=output_text3.yview)
output_text3.config(yscrollcommand=scrollbar3.set)
output_text3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar3.pack(side=tk.RIGHT, fill=tk.Y)

output_frame4 = tk.Frame(small_output_frame)
output_frame4.pack(side=tk.LEFT, padx=5, pady=5)
output_text4 = tk.Text(output_frame4, width=40, height=5, bg="lightgray", state=tk.DISABLED)
scrollbar4 = tk.Scrollbar(output_frame4, command=output_text4.yview)
output_text4.config(yscrollcommand=scrollbar4.set)
output_text4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar4.pack(side=tk.RIGHT, fill=tk.Y)

# Büyük çıktı alanı
output_frame5 = tk.Frame(app)
output_frame5.pack(pady=10)
output_text5 = tk.Text(output_frame5, width=120, height=10, bg="lightgray", state=tk.DISABLED)
scrollbar5 = tk.Scrollbar(output_frame5, command=output_text5.yview)
output_text5.config(yscrollcommand=scrollbar5.set)
output_text5.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar5.pack(side=tk.RIGHT, fill=tk.Y)

# Hata çıktısı alanı
output_frame6 = tk.Frame(app)
output_frame6.pack(pady=10)
output_text6 = tk.Text(output_frame6, width=120, height=5, bg="lightgray", state=tk.DISABLED)
scrollbar6 = tk.Scrollbar(output_frame6, command=output_text6.yview)
output_text6.config(yscrollcommand=scrollbar6.set)
output_text6.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar6.pack(side=tk.RIGHT, fill=tk.Y)

# Uygulama döngüsü
app.mainloop()



