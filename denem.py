my_string = "MERHABA"

# Her bir karakterin ASCII kodunu alarak hex tabanında temsil eden stringlere dönüştürün
hex_codes = [hex(ord(char))[2:] for char in my_string]
print(hex_codes)
# Hexadecimal stringi birleştirin
hexadecimal_str= "".join(hex_codes)

# Hexadecimal stringi yazdırın
print("ASCII kodları (hexadecimal):", hexadecimal_str)
