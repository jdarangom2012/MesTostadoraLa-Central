# =============================================================
# plc_types.py — Decodificación de tipos de dato del M221
# =============================================================
#
# El M221 usa direcciones en palabras de 16 bits (%MW).
# Modbus TCP lee Holding Registers (cada uno = 1 word de 16 bits).
#
# Mapeo de direcciones %MW → Holding Register Modbus:
#   %MW500 → HR 500,  %MD500 → HR 500 + 501 (32 bits, 2 words)
#   %MF514 → HR 514 + 515 (REAL = 32 bits, 2 words)
#

import struct


def bcd16_a_segundos(word: int) -> int:
    """
    Decodifica un WORD BCD de 16 bits con formato MM:SS a segundos totales.
    Ejemplo: 0x0135 → 01 min 35 seg → 95 segundos
    El M221 almacena tiempo como BCD: byte alto = minutos, byte bajo = segundos.
    """
    minutos  = ((word >> 12) & 0xF) * 10 + ((word >> 8) & 0xF)
    segundos = ((word >> 4)  & 0xF) * 10 +  (word       & 0xF)
    return minutos * 60 + segundos


def bcd32_a_fecha(dword: int) -> str:
    """
    Decodifica un DWORD BCD de 32 bits a string fecha 'DD/MM/YYYY'.
    Formato M221: 0xDDMMYYYY  (4 bytes BCD)
    Ejemplo: 0x13062025 → '13/06/2025'
    """
    try:
        b = dword.to_bytes(4, byteorder='big')
        dia  = (b[0] >> 4) * 10 + (b[0] & 0xF)
        mes  = (b[1] >> 4) * 10 + (b[1] & 0xF)
        anio = ((b[2] >> 4) * 10 + (b[2] & 0xF)) * 100 + \
               ((b[3] >> 4) * 10 + (b[3] & 0xF))
        return f"{dia:02d}/{mes:02d}/{anio:04d}"
    except Exception:
        return ""


def bcd32_a_hora(dword: int) -> str:
    """
    Decodifica un DWORD BCD de 32 bits a string hora 'HH:MM:SS'.
    Formato M221: 0x00HHMMSS  (byte más significativo reservado)
    Ejemplo: 0x00143022 → '14:30:22'
    """
    try:
        b = dword.to_bytes(4, byteorder='big')
        hh = (b[1] >> 4) * 10 + (b[1] & 0xF)
        mm = (b[2] >> 4) * 10 + (b[2] & 0xF)
        ss = (b[3] >> 4) * 10 + (b[3] & 0xF)
        return f"{hh:02d}:{mm:02d}:{ss:02d}"
    except Exception:
        return ""


def regs_a_udint(regs: list, idx: int) -> int:
    """
    Lee 2 words consecutivos y los combina en un UDINT de 32 bits.
    El M221 almacena word alto primero (big-endian entre words).
    """
    hi = regs[idx]     & 0xFFFF
    lo = regs[idx + 1] & 0xFFFF
    return (hi << 16) | lo


def regs_a_real(regs: list, idx: int) -> float:
    """
    Lee 2 words y los interpreta como IEEE 754 float de 32 bits.
    El M221 almacena el word alto primero.
    """
    raw = struct.pack('>HH', regs[idx], regs[idx + 1])
    return round(struct.unpack('>f', raw)[0], 4)


def regs_a_string(regs: list, idx: int, num_words: int = 10) -> str:
    """
    Lee num_words words y los decodifica como STRING del M221.
    El M221 almacena strings con byte alto = char[n], byte bajo = char[n+1].
    STRING[20] ocupa 10 words + 1 word de longitud → leemos desde idx+1
    en algunas versiones, o desde idx en otras. Aquí leemos desde idx.
    """
    chars = []
    for i in range(num_words):
        word = regs[idx + i]
        hi = (word >> 8) & 0xFF
        lo = word & 0xFF
        if hi:
            chars.append(chr(hi))
        if lo:
            chars.append(chr(lo))
    return "".join(chars).strip("\x00").strip()[:20]
