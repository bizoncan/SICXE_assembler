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

temp = []
labels = []
adres = 0
baslangic=0
cnt=0
brk = False
for code in codes:
    label, opcode, operand=parse_line(code)
    if label not in temp:
        temp.append(hex(adres)[2:])
        temp.append(label)
    elif label in temp and label is not None:
        print(label)  
        print("HATA: Bu sembol, sembol tablosunda zaten var.")

    if opcode == "START":
        if operand == None:
            baslangic=0
            print(opcode + " "+hex(adres))
        else:
            brk=True
            baslangic = int(code[code.index(opcode)+1], 16)           
            adres = baslangic        
            print(opcode + " "+hex(adres))
    if (opcode in opcodeTable or opcode[0]=="+") and opcode != "START":
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

        elif opcode in opcodeTable:
            if opcodeTable[opcode][1] == "3/4":
                print(opcode + " "+hex(adres))
                adres += 3
            elif opcodeTable[opcode][1] == "2":
                print(opcode + " "+hex(adres))
                adres += 2
            elif opcodeTable[opcode][1] == "1":
                print(opcode + " "+hex(adres))
                adres += 1       
        elif opcode[0]=="+":
            print(opcode + " "+hex(adres))
            adres += 4




    else:
            print("HATA: Bu komut, komut tablosunda yok.")
    
