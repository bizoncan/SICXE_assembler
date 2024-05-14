def parse_line(parts):
    if len(parts) == 3:
        label, opcode, operand = parts
        return label, opcode, operand
    elif len(parts) == 2:
        opcode, operand = parts
        return None, opcode, operand
        
    elif len(parts) == 1:
        opcode = parts[0]
        return None, opcode, None
    else:
        print("Hatalı satır:", line)
        return None, None, None
def pc_adres(adres, sym_adres):
    sym_adres = int(sym_adres,16)
    if -2048<=sym_adres-adres <= 2047:
        return True
    else:
        return False
def base_adres(adres,sym_adres):
    sym_adres = int(sym_adres,16)
    if 0<=sym_adres-adres <= 4095:
        return True
    else:
        return False
def birlestir(str1,str2):
    birlesmis_liste = str1 + str2
    birlesmis_string = ''.join(birlesmis_liste)
    return birlesmis_string
def fix_format4(str1):
    while len(str1) < 5 :
        str1=birlestir("0",str1)
    return str1
def fix_format3(str1):
    while len(str1) < 3 :
        str1=birlestir("0",str1)
    return str1
with open("OpcodeTable.txt", "r") as dosya:
    opcodeTable = {}
    for satir  in dosya:
        opcode, hexcode, form = satir.split()
        opcodeTable[opcode] = hexcode, form
        
with open("denemekod.txt", "r") as dosya:
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

object_code= []
for code in codes:
    label, opcode, operand=parse_line(code)
    print(opcode)
    if opcode == "START":
        
        if operand == None:
            baslangic=0
            adres = baslangic
            print(opcode + " "+hex(adres))
        else:
            brk=True
            baslangic = int(operand, 16)           
            adres = baslangic        
            print(opcode + " "+hex(adres))
    object_code_curr="0"
    if opcode[0] == "+":
        if operand[0] == "@":
            object_code_curr = int(opcodeTable[(opcode[1:])][0],16) + 2
            object_code_curr = hex(object_code_curr)[2:]
            object_code_curr=birlestir(object_code_curr,"1")
            object_code_curr=birlestir(object_code_curr,fix_format4(symtab[operand[1:]][0]))
        elif operand[0] == "#":
            object_code_curr = int(opcodeTable[(opcode[1:])][0],16) + 1
            object_code_curr = hex(object_code_curr)[2:]
            object_code_curr=birlestir(object_code_curr,"1")
            object_code_curr=birlestir(object_code_curr,fix_format4(symtab[operand[1:]][0]))
        elif operand[-2:] == ",X":
            object_code_curr = int(opcodeTable[(opcode[1:])][0],16) + 3
            object_code_curr = hex(object_code_curr)[2:]
            object_code_curr=birlestir(object_code_curr,"9")
            object_code_curr=birlestir(object_code_curr,fix_format4(symtab[operand[1:-2]][0]))
        else:
            object_code_curr = int(opcodeTable[(opcode[1:])][0],16) + 3
            object_code_curr = hex(object_code_curr)[2:]
            object_code_curr=birlestir(object_code_curr,"1")
            object_code_curr=birlestir(object_code_curr,fix_format4(symtab[operand][0]))
        adres = adres + 4 
    if opcode in opcodeTable:
        
        if operand[0] == "@":
            if operand in symtab:
                if pc_adres(adres,symtab[operand[1:]][0]):
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 2
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"2")                 
                    next_adres=adres + 3
                    object_code_curr=birlestir(object_code_curr,fix_format3(hex(int(symtab[operand[1:]][0],16)-next_adres)[2:]))
                elif base_adres(adres,symtab[operand[1:]][0]):
                    object_code_curr = int(opcodeTable[(opcode[1:])][0],16) + 2
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"4")                 
                    next_adres=adres + 3
                    object_code_curr=birlestir(object_code_curr,fix_format3(hex(int(symtab[operand[1:]][0],16)-next_adres)[2:]))
            else:
                object_code_curr = int(opcodeTable[(opcode)][0],16) + 2
                object_code_curr = hex(object_code_curr)[2:]
                object_code_curr=birlestir(object_code_curr,"0")                 
                object_code_curr=birlestir(object_code_curr,fix_format3(operand[1:]))
        elif operand[0] == "#":
            
            if operand[1:] in symtab:
                print(adres)
                if pc_adres(adres,symtab[operand[1:]][0]):
                    
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 1
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"2")                 
                    next_adres=adres + 3
                    object_code_curr=birlestir(object_code_curr,fix_format3(hex(int(symtab[operand[1:]][0],16)-next_adres)[2:]))
                elif base_adres(adres,symtab[operand[1:]][0]):
                    print("pipi")
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 1
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"4")                 
                    next_adres=adres + 3
                    object_code_curr=birlestir(object_code_curr,fix_format3(hex(int(symtab[operand[1:]][0],16)-next_adres)[2:]))
            else:
                
                object_code_curr = int(opcodeTable[(opcode)][0],16) + 1
                object_code_curr = hex(object_code_curr)[2:]
                object_code_curr=birlestir(object_code_curr,"0")                 
                object_code_curr=birlestir(object_code_curr,fix_format3(operand[1:]))
            
            
            
            
            
            
            
            
            
            
            
            
    if object_code_curr != "0":
        object_code.append(object_code_curr)
    
            

print(object_code) 
            
            
            
            
            