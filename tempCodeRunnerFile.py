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