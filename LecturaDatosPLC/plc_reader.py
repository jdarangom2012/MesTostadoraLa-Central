# =============================================================
# plc_reader.py — Lectura Modbus TCP del M221
# Direcciones exactas según REPORTE_PLC.xlsx
# Mapeo hacia los campos de dbo.tblConsumosTostion
# =============================================================
#
# Campos de tblConsumosTostion ↔ Registro PLC:
#
#  IdOrden              ← %MD500  UDINT 32bit  (2 words: MW500+MW501)
#  IdCliente            ← %MW502  UINT  16bit
#  Nombre (cliente)     ← %MW503-512  STRING 20char (10 words)
#  PerfilTueste (*)     ← %MW513  UINT  (se loguea pero no va a la tabla)
#  PesoCv               ← %MF514  REAL  32bit  (MW514+MW515)
#  FechaHoraIni         ← %MD516+%MD518 BCD → int compacto YYYYMMDDHHMMSS
#  ConsumoGas           ← %MW520  UINT  16bit
#  ConsumoKwh           ← %MW521  UINT  16bit
#  PesoCt               ← %MF522  REAL  32bit  (MW522+MW523)
#  TempDesh             ← %MW524  UINT  → float
#  TiempoDesh_seg       ← %MW525  BCD   → segundos
#  TempRecu             ← %MW526  UINT  → float
#  TiempoRecu_seg       ← %MW527  BCD   → segundos
#  Temp1Crack           ← %MW528  UINT  → float
#  Tiempo1Crack_seg     ← %MW529  BCD   → segundos
#  TempfinCurva         ← %MW530  UINT  → float
#  TiempofinCurva_seg   ← %MW531  BCD   → segundos
#  FechaHoraFin         ← %MD532+%MD534 BCD → int compacto YYYYMMDDHHMMSS
#  TiempoTueste_seg     ← %MW536  BCD   → segundos
#  TiempoEnfriamiento_seg ← %MW537 BCD  → segundos
#
#  Rendimiento          → calculado: (PesoCt / PesoCv) * 100  (float %)
#
# (*) PerfilTueste no tiene columna en tblConsumosTostion, se incluye
#     en el dict solo para el log.

from typing import Optional
import struct
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
from config import PLC_HOST, PLC_PORT, PLC_UNIT_ID, COIL_TRIGGER

# Bloque único: %MW500 al %MW537 = 38 words
BLOQUE_START = 500
BLOQUE_COUNT = 38   # 537 - 500 + 1


# =============================================================
# DECODIFICADORES DE TIPOS DE DATO DEL M221
# =============================================================

def _bcd16_a_seg(word: int) -> int:
    """BCD 16 bit formato MM:SS → segundos totales."""
    mm = ((word >> 12) & 0xF) * 10 + ((word >> 8) & 0xF)
    ss = ((word >> 4)  & 0xF) * 10 + (word        & 0xF)
    return mm * 60 + ss


def _bcd32_fecha_hora_a_int(fecha_dword: int, hora_dword: int) -> int:
    """
    Convierte dos DWORD BCD (fecha + hora del M221) en un entero
    compacto con formato YYYYMMDDHHmmss, apto para la columna int
    FechaHoraIni / FechaHoraFin de tblConsumosTostion.

    Formato M221 fecha BCD: byte0=DD, byte1=MM, byte2=AñoHi, byte3=AñoLo
    Formato M221 hora  BCD: byte0=reservado, byte1=HH, byte2=MM, byte3=SS
    """
    def bcd_byte(b): return (b >> 4) * 10 + (b & 0xF)

    fb = fecha_dword.to_bytes(4, 'big')
    hb = hora_dword.to_bytes(4, 'big')

    dd   = bcd_byte(fb[0]);  mm   = bcd_byte(fb[1])
    anhi = bcd_byte(fb[2]);  anlo = bcd_byte(fb[3])
    yyyy = anhi * 100 + anlo

    HH = bcd_byte(hb[1]);  MI = bcd_byte(hb[2]);  SS = bcd_byte(hb[3])

    return int(f"{yyyy:04d}{mm:02d}{dd:02d}{HH:02d}{MI:02d}{SS:02d}")


def _udint(regs: list, idx: int) -> int:
    """2 words → UDINT 32 bit (word alto primero)."""
    return ((regs[idx] & 0xFFFF) << 16) | (regs[idx + 1] & 0xFFFF)


def _real(regs: list, idx: int) -> float:
    """2 words → IEEE 754 float 32 bit."""
    raw = struct.pack('>HH', regs[idx], regs[idx + 1])
    val = struct.unpack('>f', raw)[0]
    return round(val, 4)


def _string(regs: list, idx: int, num_words: int = 10) -> str:
    """num_words words → STRING M221 (byte alto = char[n], byte bajo = char[n+1])."""
    chars = []
    for i in range(num_words):
        w = regs[idx + i]
        hi, lo = (w >> 8) & 0xFF, w & 0xFF
        if hi: chars.append(chr(hi))
        if lo: chars.append(chr(lo))
    return "".join(chars).strip("\x00").strip()[:20]


def _off(addr: int) -> int:
    """Índice dentro del bloque leído (base BLOQUE_START)."""
    return addr - BLOQUE_START


# =============================================================
# PARSEO DEL BLOQUE
# =============================================================
def _parsear(regs: list) -> dict:
    """
    Transforma los 38 words leídos en el dict exacto que
    sql_writer.insertar() necesita.
    """
    # ── Identificación ───────────────────────────────────────
    id_orden       = _udint(regs, _off(500))           # %MD500
    id_cliente     = regs[_off(502)]                   # %MW502
    nombre         = _string(regs, _off(503), 10)      # %MW503-512
    perfil_tueste  = regs[_off(513)]                   # %MW513 (solo log)

    # ── Pesos ────────────────────────────────────────────────
    peso_cv        = _real(regs, _off(514))            # %MF514
    peso_ct        = _real(regs, _off(522))            # %MF522

    # ── Fechas/horas → int compacto YYYYMMDDHHmmss ──────────
    fecha_ini_dw   = _udint(regs, _off(516))           # %MD516
    hora_ini_dw    = _udint(regs, _off(518))           # %MD518
    fecha_fin_dw   = _udint(regs, _off(532))           # %MD532
    hora_fin_dw    = _udint(regs, _off(534))           # %MD534

    fecha_hora_ini = _bcd32_fecha_hora_a_int(fecha_ini_dw, hora_ini_dw)
    fecha_hora_fin = _bcd32_fecha_hora_a_int(fecha_fin_dw, hora_fin_dw)

    # ── Consumos ─────────────────────────────────────────────
    consumo_gas    = float(regs[_off(520)])            # %MW520
    consumo_kwh    = float(regs[_off(521)])            # %MW521

    # ── Temperaturas → float ─────────────────────────────────
    temp_desh      = float(regs[_off(524)])            # %MW524
    temp_recu      = float(regs[_off(526)])            # %MW526
    temp_1crk      = float(regs[_off(528)])            # %MW528
    temp_fin       = float(regs[_off(530)])            # %MW530

    # ── Tiempos BCD → segundos (el SP convierte a TIME(0)) ───
    tiem_desh_seg      = _bcd16_a_seg(regs[_off(525)])  # %MW525
    tiem_recu_seg      = _bcd16_a_seg(regs[_off(527)])  # %MW527
    tiem_1crk_seg      = _bcd16_a_seg(regs[_off(529)])  # %MW529
    tiem_fin_seg       = _bcd16_a_seg(regs[_off(531)])  # %MW531
    tiem_tueste_seg    = _bcd16_a_seg(regs[_off(536)])  # %MW536
    tiem_enfr_seg      = _bcd16_a_seg(regs[_off(537)])  # %MW537

    # ── Rendimiento calculado ────────────────────────────────
    rendimiento = round((peso_ct / peso_cv) * 100.0, 2) if peso_cv else 0.0

    return {
        # Campos para tblConsumosTostion
        "IdOrden":               id_orden,
        "IdCliente":             id_cliente,
        "PesoCv":                peso_cv,
        "PesoCt":                peso_ct,
        "TempDesh":              temp_desh,
        "TiempoDesh_seg":        tiem_desh_seg,
        "TempRecu":              temp_recu,
        "TiempoRecu_seg":        tiem_recu_seg,
        "Temp1Crack":            temp_1crk,
        "Tiempo1Crack_seg":      tiem_1crk_seg,
        "TempfinCurva":          temp_fin,
        "TiempofinCurva_seg":    tiem_fin_seg,
        "TiempoTueste_seg":      tiem_tueste_seg,
        "TiempoEnfriamiento_seg":tiem_enfr_seg,
        "Rendimiento":           rendimiento,
        "ConsumoGas":            consumo_gas,
        "ConsumoKwh":            consumo_kwh,
        "FechaHoraIni":          fecha_hora_ini,
        "FechaHoraFin":          fecha_hora_fin,
        "Nombre":                nombre,
        # Extra solo para el log (no va al SP)
        "_PerfilTueste":         perfil_tueste,
    }


# =============================================================
# CLASE PRINCIPAL
# =============================================================
class PLCReader:

    def __init__(self):
        self.client: Optional[ModbusTcpClient] = None

    def conectar(self) -> bool:
        try:
            self.client = ModbusTcpClient(
                host=PLC_HOST, port=PLC_PORT, timeout=5
            )
            ok = self.client.connect()
            if not ok:
                raise ConnectionError(
                    f"PLC {PLC_HOST}:{PLC_PORT} rechazó la conexión"
                )
            return ok
        except Exception as e:
            raise ConnectionError(str(e))

    def desconectar(self):
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass

    def _asegurar_conexion(self):
        if not self.client or not self.client.is_socket_open():
            self.conectar()

    # ── %M93 ─────────────────────────────────────────────────
    def leer_trigger(self) -> Optional[bool]:
        """Lee el coil %M93. Retorna True/False o None si no responde."""
        self._asegurar_conexion()
        try:
            r = self.client.read_coils(COIL_TRIGGER, 1, slave=PLC_UNIT_ID)
            if r.isError():
                return None
            return bool(r.bits[0])
        except ModbusException as e:
            raise IOError(f"Error leyendo %M{COIL_TRIGGER}: {e}")

    def resetear_trigger(self):
        """Pone %M93 = False para que el PLC sepa que ya se procesó."""
        self._asegurar_conexion()
        try:
            self.client.write_coil(COIL_TRIGGER, False, slave=PLC_UNIT_ID)
        except ModbusException as e:
            raise IOError(f"Error reseteando %M{COIL_TRIGGER}: {e}")

    # ── Lectura del bloque %MW500-537 ────────────────────────
    def leer_datos(self) -> dict:
        """
        Lee los 38 Holding Registers (%MW500-537) en una sola
        petición Modbus y retorna el dict listo para el SP.
        """
        self._asegurar_conexion()
        r = self.client.read_holding_registers(
            BLOQUE_START, BLOQUE_COUNT, slave=PLC_UNIT_ID
        )
        if r.isError():
            raise IOError(
                f"Error leyendo bloque %MW{BLOQUE_START}-"
                f"%MW{BLOQUE_START + BLOQUE_COUNT - 1}: {r}"
            )
        return _parsear(r.registers)