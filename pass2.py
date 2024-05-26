def find_reg(str1):
    a=0
    x=1
    l=2
    b=3
    s=4
    t=5
    f=6
    pc=8
    sw=9
    if str1=="A":
        return a
    elif str1=="X":
        return x
    elif str1=="L":
        return l
    elif str1=="B":
        return b
    elif str1=="S":
        return s
    elif str1=="T":
        return t
    elif str1=="F":
        return f   
    elif str1=="PC":
        return pc
    elif str1=="SW":
        return sw
def cumleyi_ayir(cumle, isaret):
    bolunmus_kisimlar = cumle.split(isaret)
    return bolunmus_kisimlar
def parse_line(parts):
    if len(parts) == 3:
        label, opcode, operand = parts
        return label, opcode, operand
    elif len(parts) == 2:
        if "START" in parts:
            opcode,operand=parts
            return "*", opcode, operand
        else:
            opcode, operand = parts
            return None, opcode, operand
    elif len(parts) == 2:
        opcode, operand = parts
        return None, opcode, operand
        
    elif len(parts) == 1:
        opcode = parts[0]
        return None, opcode, None
    else:
        print("Hatalı satır:", parts)
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
def fix_word(str1):
    while len(str1) <6:
        str1=birlestir("0",str1)
    return str1
def fix_zero3(str1):
    while len(str1)<6:
        str1 = birlestir("0",str1)
    return(str1)
def fix_zero4(str1):
    while len(str1)<8:
        str1 = birlestir("0",str1)
    return(str1)
def complement_16_negative(num):
    abs_num = abs(num)
    complement = 0xffff - abs_num + 1
    return hex(complement)
def fix_zero2(str1):
    while len(str1)<2:
        str1 = birlestir("0",str1)
    return str1
def listeyi_dosyaya_yaz(liste, dosya_yolu):
    with open(dosya_yolu, 'w') as dosya:
        for eleman in liste:
            dosya.write(str(eleman) + '\n')
            
with open("object_code.txt", 'w') as dosya:
    dosya.seek(0)  
    dosya.truncate() 
with open("object_program.txt", 'w') as dosya:
    dosya.seek(0)  
    dosya.truncate() 
with open("OpcodeTable.txt", "r") as dosya:
    opcodeTable = {}
    for satir  in dosya:
        opcode, hexcode, form = satir.split()
        opcodeTable[opcode] = hexcode, form

    
hatalar=[]
kod_bos=False
with open("source_code.txt", "r") as dosya:
    codes = []
    ilk_karakter = dosya.read(1)
    if not ilk_karakter:
        hatalar.append("Dosya bos" + "\n")
        listeyi_dosyaya_yaz(hatalar,"hata.txt")
        kod_bos=True
with open("source_code.txt", "r") as dosya:
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
format_4=False
object_code_dict = []
object_code= []
current_block=0
base_register = 0
x_register = 0
linkage_register=0
block_adres=[]
lit_list = []
header_kaydi = ""
text_kaydi= []
mod_kaydi=[]
use_used=False
ilk_t = True
kod_uzunluk=0
temp_t_l=""
temp_t_r=""
test_temp_t_l=""
end_kaydi=""
program_length="0"
adreslendi=False
resw_b= False
for key in block_tab:
    block_adres.append(int(block_tab[key][0],16))
    program_length=fix_word(hex(int(program_length,16)+int(block_tab[key][2],16))[2:])
if "START" not in codes:
    baslangic=0
    adres = baslangic   
    header_kaydi=("H"+"^" +"*"+"^" +fix_word(hex(baslangic)[2:])+"^"+program_length)     

for code in codes:
    label, opcode, operand=parse_line(code)
    object_code_curr="0"
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
        header_kaydi=("H"+"^" +label+"^" +fix_word(hex(baslangic)[2:])+"^"+program_length)
    if opcode[0] == "+":
            if operand in symtab or operand[:-2] in symtab or operand[1:] in symtab:
                object_code.append(fix_word(hex(adres)[2:]))
                if operand[0] == "@":
                    object_code_curr = int(opcodeTable[(opcode[1:])][0],16) + 2
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"1")
                    object_code_curr=birlestir(object_code_curr,fix_format4(symtab[operand[1:]][0]))
                    object_code_curr=fix_zero4(object_code_curr)
                    if symtab[operand[1:]][2] =="R" :
                        mod_kaydi.append("M" + "^"+fix_word(hex(adres - baslangic+1)[2:])+ "^" + "05" )
                elif operand[0] == "#":
                    object_code_curr = int(opcodeTable[(opcode[1:])][0],16) + 1
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"1")
                    object_code_curr=birlestir(object_code_curr,fix_format4(symtab[operand[1:]][0]))
                    object_code_curr=fix_zero4(object_code_curr)
                    if symtab[operand[1:]][2] =="R" :
                        mod_kaydi.append("M" + "^"+fix_word(hex(adres - baslangic+1)[2:])+ "^" + "05" )
                elif operand[-2:] == ",X":
                    object_code_curr = int(opcodeTable[(opcode[1:])][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"9")
                    object_code_curr=birlestir(object_code_curr,fix_format4(hex(int(symtab[operand[:-2]][0],16)+x_register)[2:]))
                    object_code_curr=fix_zero4(object_code_curr)
                    if  symtab[operand[:-2]][2] =="R" :
                        mod_kaydi.append("M" + "^"+fix_word(hex(adres - baslangic+1)[2:])+ "^" + "05" )
                else:
                    object_code_curr = int(opcodeTable[(opcode[1:])][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"1")
                    object_code_curr=birlestir(object_code_curr,fix_format4(symtab[operand][0]))
                    object_code_curr=fix_zero4(object_code_curr)
                    if symtab[operand][2] =="R":
                        mod_kaydi.append("M" + "^"+fix_word(hex(adres - baslangic+1)[2:])+ "^" + "05" )
                adres = adres + 4 
            elif operand[0] == "#":
                object_code.append(fix_word(hex(adres)[2:]))
                object_code_curr = int(opcodeTable[(opcode[1:])][0],16) + 1
                object_code_curr = hex(object_code_curr)[2:]
                object_code_curr=birlestir(object_code_curr,"1")
                object_code_curr=birlestir(object_code_curr,fix_format4(operand[1:]))
                object_code_curr=fix_zero4(object_code_curr)
                adres = adres + 4 
            else:
                hatalar.append("Format 4'te hata var: "+hex(adres))
                print(opcode)

    elif opcode in opcodeTable and operand != None and opcodeTable[opcode][1] == "3/4":
        
        
        if operand[0] == "@":
            
            if operand[1:] in symtab:
                object_code.append(fix_word(hex(adres)[2:]))
                adreslendi=True
                next_adres=adres + 3
                if pc_adres(next_adres,symtab[operand[1:]][0]):
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"2")                 
                    toplam=int(symtab[operand[1:]][0],16)-next_adres
                    if toplam< 0:
                        top_hex=complement_16_negative(toplam)
                        if top_hex[2:4]=="ff":
                            top_hex= (top_hex[2:])[1:]
                            object_code_curr=birlestir(object_code_curr,fix_format3(top_hex))
                    else:
                        object_code_curr=birlestir(object_code_curr,fix_format3(hex(toplam)[2:]))
                elif base_adres(base_register,symtab[operand[1:]][0]):
                    object_code_curr = int(opcodeTable[(opcode[1:])][0],16) + 2
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"4")                 
                    next_adres=adres + 3
                    object_code_curr=birlestir(object_code_curr,fix_format3(hex(int(symtab[operand[1:]][0],16)-base_register)[2:]))
                else:
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 2
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"1") 
                    format_4 = True
                    object_code_curr=birlestir(object_code_curr,fix_format4(hex(int(symtab[operand[1:]][0],16))[2:]))
                    mod_kaydi.append("M" + fix_word(hex(adres - baslangic+1)[2:]) + "05" )
            else:
                if operand[1:].isnumeric() and int(operand[1:],16)<=4095 and int(operand[1:],16)>=0:
                    adreslendi=True
                    object_code.append(fix_word(hex(adres)[2:]))
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 2
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"0")                 
                    object_code_curr=birlestir(object_code_curr,fix_format3(operand[1:]))
                else:
                    adreslendi=False
                    hatalar.append("Boyle bir adres yok")
        elif operand[0] == "#":
            
            if operand[1:] in symtab:
                object_code.append(fix_word(hex(adres)[2:]))
                next_adres=adres + 3
                adreslendi=True
                if pc_adres(next_adres,symtab[operand[1:]][0]):
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"2")                 
                    toplam=int(symtab[operand[1:]][0],16)-next_adres
                    if toplam< 0:
                        top_hex=complement_16_negative(toplam)
                        if top_hex[2:4]=="ff":
                            top_hex= (top_hex[2:])[1:]
                            object_code_curr=birlestir(object_code_curr,fix_format3(top_hex))
                    else:
                        object_code_curr=birlestir(object_code_curr,fix_format3(hex(toplam)[2:]))
                elif base_adres(base_register,symtab[operand[1:]][0]):
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 1
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"4")                 
                    object_code_curr=birlestir(object_code_curr,fix_format3(hex(int(symtab[operand[1:]][0],16)-base_register)[2:]))
                else:
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 1
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"1") 
                    format_4 = True
                    object_code_curr=birlestir(object_code_curr,fix_format4(hex(symtab[operand[1:]][0],16)[2:]))
                    mod_kaydi.append("M" + fix_word(hex(adres - baslangic+1)[2:]) + "05" )
            else: 
                if operand[1:].isnumeric()and int(operand[1:],16)<=4095 and int(operand[1:],16)>=0: 
                    adreslendi=True
                    object_code.append(fix_word(hex(adres)[2:]))
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 1
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"0")                 
                    object_code_curr=birlestir(object_code_curr,fix_format3(operand[1:]))
                else:
                    adreslendi=False
                    hatalar.append("Boyle bir adres yok")
        elif operand[-2:] == ",X":

            if operand[:-2] in symtab:
                object_code.append(fix_word(hex(adres)[2:]))
                next_adres=adres + 3
                adreslendi=True
                if pc_adres(next_adres,symtab[operand[:-2]][0]):            
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"a")                 
                    toplam=int(symtab[operand[:-2]][0],16)-next_adres+x_register
                    if toplam< 0:
                        top_hex=complement_16_negative(toplam)
                        if top_hex[2:4]=="ff":
                            top_hex= (top_hex[2:])[1:]
                            object_code_curr=birlestir(object_code_curr,fix_format3(top_hex))
                    else:
                        object_code_curr=birlestir(object_code_curr,fix_format3(hex(toplam)[2:]))
                elif base_adres(base_register,symtab[operand[:-2]][0]):
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"c")                 
                    object_code_curr=birlestir(object_code_curr,fix_format3(hex(int(symtab[operand[:-2]][0],16)-base_register+x_register)[2:]))
                elif int(symtab[operand[:-2]][0],16) < 61439:
                    object_code_curr = int(opcodeTable[(opcode)][0],16) 
                    object_code_curr = hex(object_code_curr)[2:]
                    toplam=  32768 + int(symtab[operand[:-2]][0],16)
                    object_code_curr=birlestir(object_code_curr,fix_format3(hex(toplam+x_register)[2:]))
                    mod_kaydi.append("M" + fix_word(hex(adres - baslangic+1)[2:]) + "04" )
                else:
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"9") 
                    format_4 = True
                    object_code_curr=birlestir(object_code_curr,fix_format4(hex(int(symtab[operand[:-2]][0],16)+x_register)[2:]))
                    mod_kaydi.append("M" + fix_word(hex(adres - baslangic+1)[2:]) + "05" )
            else:
                if operand[:-2].isnumeric() and int(operand[:-2],16)<=4095 and int(operand[:-2],16)>=0:
                    adreslendi=True
                    object_code.append(fix_word(hex(adres)[2:]))
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"8")                 
                    object_code_curr=birlestir(object_code_curr,fix_format3(hex(int(operand[:-2],16)+x_register)[2:]))
                else:
                    adreslendi=False
                    hatalar.append("Boyle bir adres yok")
        elif operand[0] == "=":
            if operand in lit_tab:  
                object_code.append(fix_word(hex(adres)[2:]))
                if operand not in lit_list:
                    lit_list.append(operand)
                next_adres=adres + 3
                adreslendi=True
                if pc_adres(next_adres,lit_tab[operand][1]): 
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"2")                 
                    toplam=int(lit_tab[operand][1],16)-next_adres
                    if toplam< 0:
                        top_hex=complement_16_negative(toplam)
                        if top_hex[2:4]=="ff":
                            top_hex= (top_hex[2:])[1:]
                            object_code_curr=birlestir(object_code_curr,fix_format3(top_hex))
                    else:
                        object_code_curr=birlestir(object_code_curr,fix_format3(hex(toplam)[2:]))
                elif base_adres(base_register,lit_tab[operand][1]):
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"4")        
                             
                    object_code_curr=birlestir(object_code_curr,fix_format3(hex(int(lit_tab[operand][1],16)-base_register)[2:]))
                else:
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"1") 
                    format_4 = True
                    object_code_curr=birlestir(object_code_curr,fix_format4(lit_tab[operand][1]))
                    mod_kaydi.append("M" + fix_word(hex(adres - baslangic+1)[2:]) + "05" )
            else:
                adreslendi=False
                print("Hatalı yazım")
                hatalar.append("Bu literal tabloda yok:" +operand)

        else:
            
            if operand in symtab:
                object_code.append(fix_word(hex(adres)[2:]))
                next_adres=adres + 3
                adreslendi=True
                if pc_adres(next_adres,symtab[operand][0]):  
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"2")                 
                    toplam=int(symtab[operand][0],16)-next_adres
                    if toplam< 0:
                        top_hex=complement_16_negative(toplam)
                        if top_hex[2:4]=="ff":
                            top_hex= (top_hex[2:])[1:]
                            object_code_curr=birlestir(object_code_curr,fix_format3(top_hex))
                    else:
                        object_code_curr=birlestir(object_code_curr,fix_format3(hex(toplam)[2:]))
                elif base_adres(base_register,symtab[operand][0]):
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"4")                 
                    object_code_curr=birlestir(object_code_curr,fix_format3(hex(int(symtab[operand][0],16)-base_register)[2:]))
                elif int(symtab[operand][0],16) < 61439:
                    
                    object_code_curr = int(opcodeTable[(opcode)][0],16) 
                    object_code_curr = hex(object_code_curr)[2:]
                    if len(symtab[operand][0])<= 3:
                        object_code_curr=birlestir(object_code_curr,"0")
                    toplam=  int(symtab[operand][0],16)
                    object_code_curr=birlestir(object_code_curr,fix_format3(hex(toplam)[2:]))
                    mod_kaydi.append("M" + fix_word(hex(adres - baslangic+1)[2:]) + "04" )
                else:

                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"1") 
                    format_4 = True
                    object_code_curr=birlestir(object_code_curr,fix_format4(hex(symtab[operand][0])[2:]))
                    mod_kaydi.append("M" + fix_word(hex(adres - baslangic+1)[2:]) + "05" )
            else:
                if operand.isnumeric() and int(operand,16)<=4095 and int(operand,16)>=0:
                    adreslendi=True
                    object_code.append(fix_word(hex(adres)[2:]))
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"0")                 
                    object_code_curr=birlestir(object_code_curr,fix_format3(operand))   
                else:
                  
                    adreslendi=False
                    hatalar.append("Boyle bir adres yok")   
        if format_4:
            
            adres = adres + 4
            object_code_curr=fix_zero4(object_code_curr)
            format_4=False
        else:
            if adreslendi:
                adres = adres +3   
                object_code_curr=fix_zero3(object_code_curr)    
    elif opcode in opcodeTable and opcodeTable[opcode][1] == "2" and operand != None:
        object_code.append(fix_word(hex(adres)[2:]))
        object_code_curr = opcodeTable[opcode][0]
        
        if len(operand) == 1:
            object_code_curr = birlestir(object_code_curr,str(find_reg(operand)))
            object_code_curr = birlestir(object_code_curr,"0")
        else:
            operands=cumleyi_ayir(operand,",")
            object_code_curr = birlestir(object_code_curr,str(find_reg(operands[0])))
            object_code_curr = birlestir(object_code_curr,str(find_reg(operands[1])))

        adres = adres +2
    elif opcode in opcodeTable and opcodeTable[opcode][1] == "1":
        object_code.append(fix_word(hex(adres)[2:]))
        object_code_curr=opcodeTable[opcode][0]
        adres=adres+1
    elif opcode in opcodeTable and operand == None and opcodeTable[opcode][1] == "3/4":
   
        if opcode == "RSUB":
            object_code.append(fix_word(hex(adres)[2:]))
            object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
            object_code_curr = hex(object_code_curr)[2:]
            object_code_curr=birlestir(object_code_curr,"0")   
            object_code_curr=birlestir(object_code_curr,fix_format3(hex(linkage_register)[2:]))
            adres = adres + 3
        else:
            print("Hata, bu komut bu sekilde kullanilamaz:  "+opcode )
            hatalar.append("Hata, bu komut bu sekilde kullanilamaz:  "+opcode)
    elif opcode=="USE":     
        
        if operand == None:
            use_used=True
            current_block=0
            adres = block_adres[current_block]
        elif operand in block_tab:
            use_used=True
            current_block = int(block_tab[operand][1],16)
            adres = block_adres[current_block]
        else: 
            print("Bu blok blok tablosunda yok")
            hatalar.append("Bu blok blok tablosunda yok: " +operand)
    elif opcode == "LTORG":
        if len(lit_list) == 0:
            print("Herhangi bir literal yok")
            hatalar.append("Herhangi bir literal yok: " +hex(adres)[2:])
        else :
            for lit in lit_list:
                object_code_curr = lit_tab[lit][0]
                object_code.append(fix_word(hex(adres)[2:]))
                object_code.append(lit)
                object_code.append(object_code_curr)
                if ilk_t and object_code_curr != "0" :

                    temp_t_r = birlestir("T","^")
                    temp_t_r = birlestir(temp_t_r,fix_word(hex(adres)[2:]))
                    temp_t_r = birlestir(temp_t_r,"^")
                    ilk_t=False
                if kod_uzunluk + len(object_code_curr) <= 60 :
                    kod_uzunluk= len(object_code_curr)+ kod_uzunluk 
                    temp_t_l = birlestir(temp_t_l , "^")
                    temp_t_l=birlestir(temp_t_l,object_code_curr)
                else :
                    
                    text_lenght=fix_zero2(hex(int(kod_uzunluk/2))[2:])
                    temp_t_l = birlestir( text_lenght, temp_t_l)
                    temp_t_r = birlestir(temp_t_r,temp_t_l)
                    text_kaydi.append(temp_t_r)
                    temp_t_r = birlestir("T","^")
                    temp_t_r = birlestir(temp_t_r,fix_word(hex(adres-int(len(object_code_curr)/2))[2:]))
                    temp_t_r = birlestir(temp_t_r,"^")
                    temp_t_l= birlestir("^",object_code_curr)
                    kod_uzunluk=len(object_code_curr)
                adres = adres + int(lit_tab[lit][2])
            lit_list=[]
            object_code_curr="0"
            
    elif opcode == "ORG":
        if operand == None:
            pass
        elif operand in symtab:
            adres= int(symtab[operand][0])
        else:
            hatalar.append("Bu operand sembol tablosunda bulunmuyor"+"\n")
    elif opcode=="WORD":   
        object_code.append(fix_word(hex(adres)[2:]))
        object_code_curr=fix_word(hex(int(operand))[2:])
        adres = adres  + 3
    elif opcode=="BYTE":
        
        if operand[:2] == "C'":
            object_code.append(fix_word(hex(adres)[2:]))
            object_code_curr_tt= [hex(ord(i))[2:] for i in operand[2:-1]]
            object_code_curr="".join(object_code_curr_tt)
            adres=adres + int(len(object_code_curr) /2)
        elif operand[:2]== "X'":
            object_code.append(fix_word(hex(adres)[2:]))
            object_code_curr=operand[2:-1]
            adres=adres + int(len(object_code_curr) /2)
        else:
            print("Hatali tuslama")
            print(operand)
            hatalar.append("Hatali tuslama: " +hex(adres)[2:] + opcode)
    elif opcode == "RESW":
        adres += 3 * int(operand)
        resw_b=True
    elif opcode == "RESB":
        resw_b=True
        adres += int(operand)
    elif opcode =="END" :
        if len(lit_list) != 0:
            for lit in lit_list:
                object_code_curr = lit_tab[lit][0]
                object_code.append(fix_word(hex(adres)[2:]))
                object_code.append(lit)
                object_code.append(object_code_curr)
                if ilk_t and object_code_curr != "0" :

                    temp_t_r = birlestir("T","^")
                    temp_t_r = birlestir(temp_t_r,fix_word(hex(adres)[2:]))
                    temp_t_r = birlestir(temp_t_r,"^")
                    ilk_t=False
                if kod_uzunluk + len(object_code_curr) <= 60 :
                    kod_uzunluk= len(object_code_curr)+ kod_uzunluk 
                    temp_t_l = birlestir(temp_t_l , "^")
                    temp_t_l=birlestir(temp_t_l,object_code_curr)
                else :
                    text_lenght=fix_zero2(hex(int(kod_uzunluk/2))[2:])
                    temp_t_l = birlestir( text_lenght, temp_t_l)
                    temp_t_r = birlestir(temp_t_r,temp_t_l)
                    text_kaydi.append(temp_t_r)
                    temp_t_r = birlestir("T","^")
                    temp_t_r = birlestir(temp_t_r,fix_word(hex(adres-int(len(object_code_curr)/2))[2:]))
                    temp_t_r = birlestir(temp_t_r,"^")
                    temp_t_l= birlestir("^",object_code_curr)
                    kod_uzunluk=len(object_code_curr)
                adres=adres + int(lit_tab[lit][2])
                
            lit_list=[]
            object_code_curr="0"
        end_kaydi =("E"+"^"+fix_word(hex(baslangic)[2:]))
       

    if opcode =="LDB" or opcode == "+LDB" :
        if operand in symtab:

            base_register = int(symtab[operand][0],16)
           
        elif operand[1:] in symtab:
            base_register = int(symtab[operand[1:]][0],16)
        elif operand[:-2] in symtab:
            base_register = int(symtab[operand[:-2]][0],16)
        elif operand in lit_tab:
            base_register = int(lit_tab[operand][0],16)
        else:
            if operand[0] == "@" or  operand[0] == "#" :
                base_register =int(operand[1:],16)
            elif operand[-2:] == ",X":
                base_register =int(operand[:-2],16)
            else:
                base_register =int(operand,16)
        
    if opcode =="LDX" or opcode == "+LDX" :
        if operand in symtab:
            x_register = int(symtab[operand][0],16)
        elif operand[1:] in symtab:
            x_register = int(symtab[operand[1:]][0],16)
        elif operand[:-2] in symtab:
            x_register = int(symtab[operand[:-2]][0],16)
        elif operand in lit_tab:
            x_register = int(lit_tab[operand][0],16)
        else:
            if operand[0] == "@" or  operand[0] == "#" :
                x_register =int(operand[1:],16)
            elif operand[-2:] == ",X":
                x_register =int(operand[:-2],16)
            else:
                x_register =int(operand,16)
    if opcode =="LDL" or opcode == "+LDL" :
        if operand in symtab:
            linkage_register = int(symtab[operand][0],16)
        elif operand[1:] in symtab:
            linkage_register = int(symtab[operand[1:]][0],16)
        elif operand[:-2] in symtab:
            linkage_register = int(symtab[operand[:-2]][0],16)
        elif operand in lit_tab:
            linkage_register = int(lit_tab[operand][0],16)
        else:
            if operand[0] == "@" or  operand[0] == "#" :
                linkage_register =int(operand[1:],16)
            elif operand[-2:] == ",X":
                linkage_register =int(operand[:-2],16)
            else:
                linkage_register =int(operand,16)
    
    if resw_b :
        resw_b=False
        if len(temp_t_l)>0 and len(temp_t_r)>0:
            text_lenght=fix_zero2(hex(int(len(temp_t_l)/2))[2:])
            temp_t_l = birlestir( text_lenght, temp_t_l)
            temp_t_r = birlestir(temp_t_r,temp_t_l)
            text_kaydi.append(temp_t_r)
            temp_t_l=""
            temp_t_r = ""
            kod_uzunluk=0
            ilk_t=True
       
    if opcode in opcodeTable and (opcodeTable[opcode][1] == "3/4" or opcodeTable[opcode][1] == "2") and opcode != "RSUB" and operand == None:
        print("Operand bos, komut object programa eklenmedi")
        hatalar.append("Operand bos, komut object programa eklenmedi: "+opcode)   
        
    if object_code_curr != "0" or use_used :
        if object_code_curr != "0":
            object_code.append(code)
            object_code.append(object_code_curr)
        if ilk_t and object_code_curr != "0" :

            temp_t_r = birlestir("T","^")
            temp_t_r = birlestir(temp_t_r,fix_word(hex(adres-int(len(object_code_curr)/2))[2:]))
            temp_t_r = birlestir(temp_t_r,"^")
            ilk_t=False
        if use_used :
            if temp_t_r != "" and temp_t_l !="":
                text_lenght=fix_zero2(hex(int(len(temp_t_l)/2))[2:])
                temp_t_l = birlestir( text_lenght, temp_t_l)
                temp_t_r = birlestir(temp_t_r,temp_t_l)
                text_kaydi.append(temp_t_r)
                temp_t_l=""
                temp_t_r = birlestir("T","^")
                temp_t_r = birlestir(temp_t_r,fix_word(hex(adres-int(len(object_code_curr)/2))[2:]))
                temp_t_r = birlestir(temp_t_r,"^")
                kod_uzunluk=0
            
            ilk_t=True
            use_used=False
        elif kod_uzunluk + len(object_code_curr) <= 60 and object_code_curr != "0":
            kod_uzunluk= len(object_code_curr)+ kod_uzunluk 
            temp_t_l = birlestir(temp_t_l , "^")
            temp_t_l=birlestir(temp_t_l,object_code_curr)
        elif object_code_curr != "0" :
            text_lenght=fix_zero2(hex(int(kod_uzunluk/2))[2:])
            temp_t_l = birlestir( text_lenght, temp_t_l)
            
            temp_t_r = birlestir(temp_t_r,temp_t_l)
            text_kaydi.append(temp_t_r)
            temp_t_r = birlestir("T","^")
            temp_t_r = birlestir(temp_t_r,fix_word(hex(adres-int(len(object_code_curr)/2))[2:]))
            temp_t_r = birlestir(temp_t_r,"^")
            temp_t_l= birlestir("^",object_code_curr)
            kod_uzunluk=len(object_code_curr)
    if object_code_curr =="0":
        object_code.append(fix_word(hex(adres)[2:]))
        object_code.append(code)
        object_code.append("-")

    block_adres[current_block]=adres
if len(temp_t_l) != 0:
    text_lenght=fix_zero2(hex(int(kod_uzunluk/2))[2:])
    temp_t_l = birlestir( text_lenght, temp_t_l)
    temp_t_r = birlestir(temp_t_r,temp_t_l)
    text_kaydi.append(temp_t_r)
index=0
for _ in range(int(len(object_code)/3)):
    satir = []
    for _ in range(3):
        satir.append(object_code[index])
        index += 1
    object_code_dict.append(satir)

object_program=[]
if not kod_bos:
    object_program.append(header_kaydi)
for i in text_kaydi:
    object_program.append(i)
for i in mod_kaydi:
    object_program.append(i)
if not kod_bos:
    object_program.append(end_kaydi)

for i in object_program:
    print(i)
with open("object_code.txt", 'w') as dosya:
    dosya.seek(0)  # Dosyanın başına git
    dosya.truncate()
    for code in object_code_dict:
        if not kod_bos:
            dosya.write(code[0] +" ")  
            dosya.write(" ".join(code[1]))
            dosya.write(" "+str(code[2])+ "\n")  
with open("object_program.txt", 'w') as dosya:
    dosya.seek(0)  # Dosyanın başına git
    dosya.truncate()
    for code in object_program:
        if not kod_bos:
            dosya.write(code+"\n")  
            

with open("hata.txt", 'a') as dosya:
 
    for hatacik in hatalar:
        dosya.write(hatacik)