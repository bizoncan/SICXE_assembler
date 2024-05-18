with open("object_code.txt", "r") as dosya:
    object_code = []
    for o_code in dosya:
        kelimeler = o_code.strip().split()       
        object_code.append(kelimeler)  
with open("mod_kaydi.txt", "r") as dosya:
    mod_kaydi = []
    for kayit in dosya:
        mod_kaydi.append(kayit)  
with open("ORNEKKOD2.txt", "r") as dosya:
    codes = []
    for code in dosya:
        kelimeler = code.strip().split() 
        codes.append(kelimeler)  
print(object_code)
print(codes)
print(mod_kaydi)
