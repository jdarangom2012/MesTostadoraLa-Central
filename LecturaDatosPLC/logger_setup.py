# =============================================================
# logger_setup.py — Logging con rotación de archivos
# =============================================================

import logging
import os
from logging.handlers import RotatingFileHandler
from config import LOG_FILE, LOG_MAX_BYTES, LOG_BACKUP_COUNT


def crear_logger(nombre: str = "PLCService") -> logging.Logger:
    """
    Crea y retorna el logger del servicio.
    - Archivo rotativo en LOG_FILE (máx LOG_MAX_BYTES, LOG_BACKUP_COUNT copias)
    - Salida a consola (útil al correr en modo manual/debug)
    """
    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    logger = logging.getLogger(nombre)
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ── Handler de archivo rotativo ──────────────────────────
    fh = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    # ── Handler de consola ───────────────────────────────────
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def log_registro_insertado(logger: logging.Logger, tabla: str, datos: dict):
    """
    Escribe en el log una línea detallada con todos los campos del registro insertado.
    Formato legible para auditoría.
    """
    lineas = [f"✔ REGISTRO INSERTADO → {tabla}"]
    for k, v in datos.items():
        lineas.append(f"    {k:<25} = {v}")
    logger.info("\n".join(lineas))


def log_error_insercion(logger: logging.Logger, tabla: str, error: str, datos: dict):
    """
    Escribe en el log el error de inserción junto con los datos que se intentaron guardar.
    """
    lineas = [f"✘ ERROR AL INSERTAR → {tabla} | {error}"]
    for k, v in datos.items():
        lineas.append(f"    {k:<25} = {v}")
    logger.error("\n".join(lineas))
