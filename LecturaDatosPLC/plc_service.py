# =============================================================
# plc_service.py — Servicio Windows
# Cada 2 seg lee %M93 → si = 1 → lee PLC → sp_InsertarCurvaTueste
#                                           → tblConsumosTostion
#                                           → log completo
#
# INSTALAR servicio (cmd como Administrador):
#   python plc_service.py install
#   python plc_service.py start
#
# PROBAR sin instalar (modo consola):
#   python plc_service.py debug
#
# GESTIÓN:
#   python plc_service.py stop
#   python plc_service.py remove
# =============================================================

import sys
import time
import traceback

import win32serviceutil
import win32service
import win32event
import servicemanager

from config import POLL_SEG
from logger_setup import crear_logger, log_registro_insertado, log_error_insercion
from plc_reader import PLCReader
from sql_writer import SQLWriter


# =============================================================
# CICLO DE NEGOCIO
# =============================================================
def procesar_ciclo(lector: PLCReader, escritor: SQLWriter, log):
    """
    1. Lee %M93
    2. Si = 1 → lee bloque %MW500-537
    3. Ejecuta sp_InsertarCurvaTueste → tblConsumosTostion
    4. Escribe log con fecha/hora y registro completo
    5. Resetea %M93 = 0
    """

    # ── Leer bit disparador ───────────────────────────────────
    try:
        trigger = lector.leer_trigger()
    except IOError as e:
        log.warning(f"Sin respuesta al leer %M93: {e}")
        return

    if trigger is None:
        log.warning("Respuesta nula de %M93 — PLC no responde")
        return

    if not trigger:
        return   # Normal: el tueste aún no terminó

    # ── %M93 = 1 ─────────────────────────────────────────────
    log.info("▶ %M93 activado — leyendo registros del PLC")

    # ── Leer datos del PLC ───────────────────────────────────
    try:
        datos = lector.leer_datos()
    except Exception as e:
        log.error(f"Error leyendo bloque Modbus: {e}\n{traceback.format_exc()}")
        return

    # ── Insertar en SQL Server ────────────────────────────────
    try:
        id_ins = escritor.insertar(datos)

        # Log completo del registro insertado
        # Excluimos el campo interno _PerfilTueste del resumen SQL
        datos_log = {k: v for k, v in datos.items() if not k.startswith("_")}
        log_registro_insertado(
            log,
            tabla=f"dbo.tblConsumosTostion (Id={id_ins})",
            datos=datos_log
        )

    except Exception as e:
        datos_log = {k: v for k, v in datos.items() if not k.startswith("_")}
        log_error_insercion(
            log,
            tabla="dbo.tblConsumosTostion",
            error=str(e),
            datos=datos_log
        )
        # No reseteamos %M93 para que el operador pueda reintentar
        return

    # ── Resetear %M93 ─────────────────────────────────────────
    try:
        lector.resetear_trigger()
        log.info("◀ %M93 reseteado a 0 — esperando próximo tueste")
    except IOError as e:
        log.warning(f"No se pudo resetear %M93: {e}")


# =============================================================
# SERVICIO WINDOWS
# =============================================================
class PLCService(win32serviceutil.ServiceFramework):

    _svc_name_         = "PLCConsumosTostion"
    _svc_display_name_ = "PLC Consumos Tostion — Modicon M221"
    _svc_description_  = (
        "Lee curvas de tueste del PLC Modicon M221 via Modbus TCP/IP "
        "y las almacena en dbo.tblConsumosTostion (SQL Server)."
    )

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self._stop_event = win32event.CreateEvent(None, 0, 0, None)
        self._running    = True
        self.log         = crear_logger("PLCService")

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self._stop_event)
        self._running = False
        self.log.info("Solicitud de parada recibida.")

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, "")
        )
        self.log.info(
            f"═══ Servicio PLCConsumosTostion iniciado ═══  "
            f"PLC={__import__('config').PLC_HOST} | "
            f"Poll={POLL_SEG}s | Trigger=%M93"
        )
        self._loop()

    def _loop(self):
        lector   = PLCReader()
        escritor = SQLWriter()

        # Conexiones iniciales
        try:
            lector.conectar()
            self.log.info("✔ Conectado al PLC")
        except Exception as e:
            self.log.error(f"Conexión inicial al PLC fallida: {e}")

        try:
            escritor.conectar()
            self.log.info("✔ Conectado a SQL Server")
        except Exception as e:
            self.log.error(f"Conexión inicial a SQL Server fallida: {e}")

        # Bucle principal — verifica parada cada 0.5 s
        while self._running:
            try:
                procesar_ciclo(lector, escritor, self.log)
            except Exception:
                self.log.error(
                    f"Error inesperado en ciclo:\n{traceback.format_exc()}"
                )

            for _ in range(int(POLL_SEG / 0.5)):
                if not self._running:
                    break
                time.sleep(0.5)

        lector.desconectar()
        escritor.desconectar()
        self.log.info("Servicio detenido correctamente.")


# =============================================================
# MODO DEBUG — corre directo en consola (Ctrl+C para salir)
# =============================================================
def _modo_debug():
    log = crear_logger("PLCDebug")
    log.info(
        f"[DEBUG] Poll %M93 cada {POLL_SEG}s — Ctrl+C para salir\n"
        f"  PLC     : {__import__('config').PLC_HOST}:{__import__('config').PLC_PORT}\n"
        f"  Tabla   : dbo.tblConsumosTostion\n"
        f"  SP      : dbo.sp_InsertarCurvaTueste\n"
        f"  Log     : {__import__('config').LOG_FILE}"
    )

    lector   = PLCReader()
    escritor = SQLWriter()

    try:
        lector.conectar()
        log.info("✔ PLC conectado")
    except Exception as e:
        log.error(f"PLC: {e}")

    try:
        escritor.conectar()
        log.info("✔ SQL Server conectado")
    except Exception as e:
        log.error(f"SQL: {e}")

    try:
        while True:
            procesar_ciclo(lector, escritor, log)
            time.sleep(POLL_SEG)
    except KeyboardInterrupt:
        log.info("Detenido manualmente.")
    finally:
        lector.desconectar()
        escritor.desconectar()


# =============================================================
if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "debug":
        _modo_debug()
    else:
        win32serviceutil.HandleCommandLine(PLCService)