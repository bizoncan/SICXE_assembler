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

sym_tab_t=[]
lit_tab_names = []
lit_hex_value=0
lit_len=0
lit_tab = {}
labels = []
adres = 0
baslangic=0
cnt=0
brk = False
for code in codes:
    label, opcode, operand=parse_line(code)
    if opcode == "START":
        if operand == None:
            baslangic=0
            adres = baslangic
            print(opcode + " "+hex(adres))
        else:
            brk=True
            baslangic = int(code[code.index(opcode)+1], 16)           
            adres = baslangic        
            print(opcode + " "+hex(adres))
    if label not in sym_tab_t and label != None:
        sym_tab_t.append(hex(adres)[2:])
        sym_tab_t.append(label)
        
    elif label in sym_tab_t and label is not None:
        print(label)  
        print("HATA: Bu sembol, sembol tablosunda zaten var.")

    if operand !=None :
        if operand[0]=="=":
            if operand[1] == "C":
                if operand not in lit_tab_names:
                    lit_tab_names.append(operand)                
            elif operand[1] == "X":
                if operand not in lit_tab_names:
                    lit_tab_names.append(operand)   
            else:
                print("Hatali tuslama")
    if opcode == "LTORG":
        for lits in lit_tab_names:
            if lits[1] == "C":
                value = lits[3:-1]
                lit_hex_value_tab= [hex(ord(i))[2:] for i in value]
                lit_hex_value="".join(lit_hex_value_tab)
                lit_len = int(len(lit_hex_value)/2)             
                lit_temp_degerler = [lit_hex_value,hex(adres)[2:],lit_len]
                lit_tab[lits]   = lit_temp_degerler 
                adres = lit_len + adres       
            elif lits[1] == "X":
                lit_hex_value = lits[3:-1]
                lit_len = int(len(lit_hex_value)/2)       
                lit_temp_degerler = [lit_hex_value,hex(adres)[2:],lit_len]
                lit_tab[lits]   = lit_temp_degerler 
                adres = lit_len + adres 
        lit_tab_names=[]
    if opcode == "ORG":

        if operand == None:
            pass
        else:
            if operand in sym_tab_t:
                adres =int(sym_tab_t[sym_tab_t.index(operand)-1],16)    
            else:
                adres= int(operand,16)
    if opcode == "WORD":
        adres += 3
    elif opcode == "RESW":
        adres += 3 * int(operand)
    elif opcode == "RESB":
        adres += int(operand)
    elif opcode == "BYTE":
        if operand[:2] == "C'":
            adres=adres+len(operand[2:-1])
        elif operand[:2] == "X'":
            adres=adres+int(len(operand[2:-1])/2)        
    if (opcode in opcodeTable or opcode[0]=="+") and opcode != "START":
        if opcode in opcodeTable:
            if opcodeTable[opcode][1] == "3/4":
                #print(opcode + " "+hex(adres))
                adres += 3
            elif opcodeTable[opcode][1] == "2":
                #print(opcode + " "+hex(adres))
                adres += 2
            elif opcodeTable[opcode][1] == "1":
                #print(opcode + " "+hex(adres))
                adres += 1       
        elif opcode[0]=="+":
            #print(opcode + " "+hex(adres))
            adres += 4
    else:
        if opcode != "START" and opcode !="ORG" and opcode !="LTORG":

            print("HATA: Bu komut, komut tablosunda yok.")
    if opcode == "END" and len(lit_tab_names) !=0:
        for lits in lit_tab_names:
            if lits[1] == "C":
                value = lits[3:-1]
                lit_hex_value_tab= [hex(ord(i))[2:] for i in value]
                lit_hex_value="".join(lit_hex_value_tab)
                lit_len = int(len(lit_hex_value)/2)             
                lit_temp_degerler = [lit_hex_value,hex(adres)[2:],lit_len]
                lit_tab[lits]   = lit_temp_degerler 
                adres = lit_len + adres       
            elif lits[1] == "X":
                lit_hex_value = lits[3:-1]
                lit_len = int(len(lit_hex_value)/2)       
                lit_temp_degerler = [lit_hex_value,hex(adres)[2:],lit_len]
                lit_tab[lits]   = lit_temp_degerler 
                adres = lit_len + adres 
        lit_tab_names=[]
sym_tab=[]
index = 0
for _ in range(int(len(sym_tab_t)/2)):
    satir = []
    for _ in range(2):
        satir.append(sym_tab_t[index])
        index += 1
    sym_tab.append(satir)
print(sym_tab)
for key, value in lit_tab.items():
    print(key, ":", value)