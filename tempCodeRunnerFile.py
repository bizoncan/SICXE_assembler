    elif opcode == "RESW":
        adres += 3 * int(operand)
    elif opcode == "RESB":
        adres += int(operand)