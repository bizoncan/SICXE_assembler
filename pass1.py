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
block_table={}
current_block=0
block_adres=[]
max_len_arr=[]
lit_tab = {}
labels = []
adres = 0
baslangic=0
cnt=0
brk = False
max_len = 0
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
        block_table[""]=["",hex(baslangic)[2:],current_block]
        block_adres.append(adres)
        max_len = adres
        max_len_arr.append(block_adres[current_block])
    if label not in sym_tab_t and label != None:
        sym_tab_t.append(hex(adres)[2:])
        sym_tab_t.append(label)
        sym_tab_t.append(current_block)
       
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
                lit_temp_degerler = [lit_hex_value,hex(adres)[2:],lit_len,current_block]
                lit_tab[lits]   = lit_temp_degerler 
                adres = lit_len + adres       
            elif lits[1] == "X":
                lit_hex_value = lits[3:-1]
                lit_len = int(len(lit_hex_value)/2)       
                lit_temp_degerler = [lit_hex_value,hex(adres)[2:],lit_len,current_block]
                lit_tab[lits]   = lit_temp_degerler 
                adres = lit_len + adres 
        lit_tab_names=[]
        
    if opcode == "USE":
        
        if operand == None:
            current_block=0
            adres = block_adres[current_block]
        elif operand in block_table:
            current_block = block_table[operand][2]
            adres = block_adres[current_block]
        elif operand not in block_table:
           
            current_block = current_block  + 1
            
            block_adres.append(baslangic)
            block_table[operand]=[operand,hex(baslangic)[2:],current_block]
            adres = block_adres[current_block]
            max_len_arr.append(block_adres[current_block])
            

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
        if opcode != "START" and opcode !="ORG" and opcode !="LTORG" and opcode != "USE":
            
            print("HATA: Bu komut, komut tablosunda yok.")
    if opcode == "ORG":

        if operand == None:
            pass
        else:
            if operand in sym_tab_t:
                adres =int(sym_tab_t[sym_tab_t.index(operand)-1],16)    
            else:
                adres= int(operand,16)
    if opcode == "END" and len(lit_tab_names) !=0:
        for lits in lit_tab_names:
            if lits[1] == "C":
                value = lits[3:-1]
                lit_hex_value_tab= [hex(ord(i))[2:] for i in value]
                lit_hex_value="".join(lit_hex_value_tab)
                lit_len = int(len(lit_hex_value)/2)             
                lit_temp_degerler = [lit_hex_value,hex(adres)[2:],lit_len,current_block]
                lit_tab[lits]   = lit_temp_degerler 
                adres = lit_len + adres       
            elif lits[1] == "X":
                lit_hex_value = lits[3:-1]
                lit_len = int(len(lit_hex_value)/2)       
                lit_temp_degerler = [lit_hex_value,hex(adres)[2:],lit_len,current_block]
                lit_tab[lits]   = lit_temp_degerler 
                adres = lit_len + adres 
        lit_tab_names=[]

    block_adres[current_block] = adres
    if max_len_arr[current_block] < block_adres[current_block]:
        max_len_arr[current_block] = block_adres[current_block]
    
index=0
for key,value in block_table.items():
    block_table[key].append(hex(max_len_arr[index]-baslangic)[2:])
    index = index + 1
keys_list = list(block_table.keys())
for key,value in block_table.items():
   if key != "":
        key_index = keys_list.index(key)
        temp_key = keys_list[key_index-1]
        block_table[key][1]=hex(int(block_table[temp_key][1],16) + int(block_table[temp_key][3],16))[2:]
sym_tab=[]
index = 0
for _ in range(int(len(sym_tab_t)/3)):
    satir = []
    for _ in range(3):
        satir.append(sym_tab_t[index])
        index += 1
    sym_tab.append(satir)
for label in sym_tab:
    if label[2]==0:
        pass
    else:
        label [0] = hex(int(block_table[keys_list[label[2]]][1],16)-baslangic + int(label[0],16))[2:]
print(sym_tab)
for key, value in lit_tab.items():
    if lit_tab[key][3]==0:
        pass
    else:
        lit_tab[key][1] = hex(int(block_table[keys_list[lit_tab[key][3]]][1],16)-baslangic + int(lit_tab[key][1],16))[2:]
for key, value in lit_tab.items():
    print(key, ":", value)
print(block_table)
