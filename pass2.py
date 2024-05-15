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
    while len(str1)<5:
        str1 = birlestir("0",str1)
    return(str1)
def complement_16_negative(num):
    abs_num = abs(num)
    complement = 0xffff - abs_num + 1
    return hex(complement)
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
format_4=False
current_block=0
base_register = 0
x_register = 0
linkage_register=0
block_adres=[]
lit_list = []
for key in block_tab:
    block_adres.append(int(block_tab[key][0],16))
object_code= []
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
            object_code_curr=birlestir(object_code_curr,fix_format4(hex(int(symtab[operand[:-2]][0],16)+x_register)[2:]))
        else:
            object_code_curr = int(opcodeTable[(opcode[1:])][0],16) + 3
            object_code_curr = hex(object_code_curr)[2:]
            object_code_curr=birlestir(object_code_curr,"1")
            object_code_curr=birlestir(object_code_curr,fix_format4(symtab[operand][0]))
        adres = adres + 4 
    elif opcode in opcodeTable and operand != None:
        if operand[0] == "@":
            if operand[1:] in symtab:
                next_adres=adres + 6
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
            else:
                object_code_curr = int(opcodeTable[(opcode)][0],16) + 2
                object_code_curr = hex(object_code_curr)[2:]
                object_code_curr=birlestir(object_code_curr,"0")                 
                object_code_curr=birlestir(object_code_curr,fix_format3(operand[1:]))
        elif operand[0] == "#":
            if operand[1:] in symtab:
                next_adres=adres + 6
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
            else:  
                object_code_curr = int(opcodeTable[(opcode)][0],16) + 1
                object_code_curr = hex(object_code_curr)[2:]
                object_code_curr=birlestir(object_code_curr,"0")                 
                object_code_curr=birlestir(object_code_curr,fix_format3(operand[1:]))
        elif operand[-2:] == ",X":
            next_adres=adres + 6
            if operand[:-2] in symtab:
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
                else:
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"9") 
                    format_4 = True
                    object_code_curr=birlestir(object_code_curr,fix_format4(hex(int(symtab[operand[:-2]][0],16)+x_register)[2:]))
            else:
                object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                object_code_curr = hex(object_code_curr)[2:]
                object_code_curr=birlestir(object_code_curr,"8")                 
                object_code_curr=birlestir(object_code_curr,fix_format3(hex(int(operand[:-2],16)+x_register)[2:]))
        elif operand[0] == "=":
            if operand in lit_tab:  
                lit_list.append(operand)
                next_adres=adres + 6
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
                    print(operand)
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"1") 
                    format_4 = True
                    
                    object_code_curr=birlestir(object_code_curr,fix_format4(lit_tab[operand][1]))
            else:
                print("Hatalı yazım")
        else:
            next_adres=adres + 6
            if operand in symtab:
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
                    if opcode=="LDX":
                        print(31)
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
                else:

                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"1") 
                    format_4 = True
                    object_code_curr=birlestir(object_code_curr,fix_format4(hex(symtab[operand][0])[2:]))
            else:
                    
                    object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
                    object_code_curr = hex(object_code_curr)[2:]
                    object_code_curr=birlestir(object_code_curr,"0")                 
                    object_code_curr=birlestir(object_code_curr,fix_format3(operand))      
        if format_4:
            adres = adres + 4
            object_code_curr=fix_zero4(object_code_curr)
            format_4=False
        else:
            adres = adres +3   
            object_code_curr=fix_zero3(object_code_curr)    
    elif opcode in opcodeTable and operand == None:
        if opcode == "RSUB":
            object_code_curr = int(opcodeTable[(opcode)][0],16) + 3
            object_code_curr = hex(object_code_curr)[2:]
            object_code_curr=birlestir(object_code_curr,"0")   
            object_code_curr=birlestir(object_code_curr,fix_format3(hex(linkage_register)[2:]))
        else:
            object_code_curr = int(opcodeTable[(opcode)][0],16)
            object_code_curr = hex(object_code_curr)[2:]
    elif opcode=="USE":     
        if operand == None:
            current_block=0
            adres = int(block_tab[" "][1])
        elif operand in block_tab:
            current_block = int(block_tab[operand][1])
            adres = block_adres[current_block]
        else: 
            print("Bu blok blok tablosunda yok")
    elif opcode == "LTORG":
        if len(lit_list) == 0:
            print("Herhangi bir literal yok")
        else :
            for lit in lit_list:
                object_code_curr = lit_tab[lit][0]
                object_code.append(object_code_curr)
            lit_list=[]
            object_code_curr="0"
    elif opcode == "ORG":
        if operand == None:
            pass
        else:
            adres= int(symtab[operand][0])   
    elif opcode=="WORD":   
        
        object_code_curr=fix_word(hex(int(operand))[2:])
        adres = adres  + 3
    elif opcode=="BYTE":
        if operand[:2] == "C'":
            object_code_curr_tt= [hex(ord(i))[2:] for i in operand[2:-1]]
            object_code_curr="".join(object_code_curr_tt)
            adres=adres + int(len(object_code_curr) /2)
        elif operand[:2]== "X'":
            object_code_curr=operand[2:-1]
            adres=adres + int(len(object_code_curr) /2)
        else:
            print("Hatali tuslama")
    elif opcode =="END" and len(lit_list) != 0:
        for lit in lit_list:
            object_code_curr = lit_tab[lit][0]
            object_code.append(object_code_curr)
        lit_list=[]
        object_code_curr="0"
    
    if object_code_curr != "0" :
        object_code.append(object_code_curr)
   
    block_adres[current_block]=adres
            

print(object_code) 
            
            
            
            
            