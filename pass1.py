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
        print("Hatalı satır:", parts)
        return None, None, None
def cumleyi_ayir(cumle, isaret):
    bolunmus_kisimlar = cumle.split(isaret)
    yeni_kisimlar = []
    for i, kisim in enumerate(bolunmus_kisimlar):
        if i != 0:
            yeni_kisimlar.append(isaret + kisim)
        else:
            yeni_kisimlar.append(kisim)
    return yeni_kisimlar

    
    
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
    if label not in sym_tab_t and label != None and opcode != "EQU":
        sym_tab_t.append(hex(adres)[2:])
        sym_tab_t.append(label)
        sym_tab_t.append(current_block)
        sym_tab_t.append("R")
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
    equ_deger =0     
    arti=0  
    eksi=0
    if opcode=="EQU":
        if label not in sym_tab_t:
            if  operand == "*":
                sym_tab_t.append(hex(adres)[2:])
                sym_tab_t.append(label)
                sym_tab_t.append(current_block)
                sym_tab_t.append("A")
            elif "-" or "+" in operand :
                arti = operand.count("+")
                eksi = operand.count("-")
                if arti+1 == eksi:
                    bolunmus_kisimlar = cumleyi_ayir(operand, "-")
                    yeni_kisimlar = []
                    for i in bolunmus_kisimlar:
                        if "+" in i:
                            yeni_kisimlar.extend(cumleyi_ayir(i, "+"))
                        else:
                            yeni_kisimlar.append(i)
                    for i in yeni_kisimlar:
                        if i[0] == "+":
                            equ_deger = equ_deger+int(sym_tab_t[sym_tab_t.index(i[1:])-1],16)
                        elif i[0] =="-":
                            equ_deger = equ_deger-int(sym_tab_t[sym_tab_t.index(i[1:])-1],16)
                        else :
                            equ_deger = equ_deger+int(sym_tab_t[sym_tab_t.index(i)-1],16)
                    sym_tab_t.append(hex(equ_deger)[3:])
                    sym_tab_t.append(label)
                    sym_tab_t.append(current_block)
                    sym_tab_t.append("A")
                else:
                    print("Bu işlem yapılamaz")
                    
            elif "*" or "/" in operand:
                print("hata bu işaretler kullanılamaz")
        else:
            print("Bu etiket listede var")
            print(sym_tab_t)
        
        
        
        
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
        if opcode != "START" and opcode !="ORG" and opcode !="LTORG" and opcode != "USE" and opcode != "EQU" and opcode !="WORD"and opcode !="RESW"and opcode !="BYTE" and opcode!="RESB" and opcode != "END":
            
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
for _ in range(int(len(sym_tab_t)/4)):
    satir = []
    for _ in range(4):
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

with open("symtab.txt", 'w') as dosya:
    for label in sym_tab:
        dosya.write(label[0] + " " + label[1]+ " " + str(label[2]) + " " +label[3]  +"\n")

with open("lit_tab.txt", 'w') as dosya:
    for anahtar, deger in lit_tab.items():
        dosya.write(anahtar+" " + deger[0]+" " + deger[1]+ " "+ str(deger[2]) + " " +str(deger[3])+ "\n")
       
with open("block_tab.txt", 'w') as dosya:
    for anahtar, deger in block_table.items():
        dosya.write(anahtar+" " + deger[0]+" " +str(deger[1]) + " "+ str(deger[2]) + " " +str(deger[3])+ "\n")