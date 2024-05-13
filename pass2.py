def parse_line(parts):
    if len(parts) == 3:
        label, opcode, operand = parts
        return label, opcode, operand
    elif len(parts) == 2:
        if "START" in parts:
            label,opcode=parts
            return label, opcode, None
        else:
            opcode, operand = parts
            return None, opcode, operand
        
    elif len(parts) == 1:
        opcode = parts[0]
        return None, opcode, None
    else:
        print("Hatalı satır:", line)
        return None, None, None
def pc_adres(adres, sym_adres):
    adres = int(adres,16)
    sym_adres = int(sym_adres,16)
    if -2048<=sym_adres-adres <= 2047:
        return True
    else:
        return False
def base_adres(adres,sym_adres):
    adres = int(adres,16)
    sym_adres = int(sym_adres,16)
    if 0<=sym_adres-adres <= 4095:
        return True
    else:
        return False
with open("OpcodeTable.txt", "r") as dosya:
    opcodeTable = {}
    for satir  in dosya:
        opcode, hexcode, form = satir.split()
        opcodeTable[opcode] = hexcode, form
        
with open("OrnekKod.txt", "r") as dosya:
    codes = []
    for code in dosya:
        kelimeler = code.strip().split() 
        codes.append(kelimeler)  
with open("symtab.txt", "r") as dosya:
    symtab = {}
    for satir  in dosya:
        sym_adres, label_name, block_num, label_type = satir.split()
        symtab[label_name] = sym_adres, block_num, label_type
with open("lit_tab.txt", "r") as dosya:
    lit_tab = {}
    for satir  in dosya:
        
        lit_name,hex_value, lit_adres, lenght, block_number = satir.split()
        lit_tab[lit_name] = hex_value, lit_adres,lenght ,block_number
with open("block_tab.txt", "r") as dosya:
    block_tab = {}
    for satir  in dosya:
        try:
            block_name, block_name,starting_adres, block_num, lenght = satir.split()
        except ValueError:
            block_name=" "
            starting_adres, block_num, lenght = satir.split()
        block_tab[block_name] = starting_adres, block_num, lenght
print(symtab)
print(lit_tab)
print(block_tab)

for code in codes:
    label, opcode, operand=parse_line(code)
    if opcode =
