# =============================================================
# sql_writer.py — Inserta en dbo.tblConsumosTostion
#                 via dbo.sp_InsertarCurvaTueste
# =============================================================
#
# Campos de tblConsumosTostion (en orden de la tabla):
#   Id            int          IDENTITY — lo genera SQL
#   FechaIngreso  datetime     DEFAULT GETDATE() — lo genera SQL
#   Tiempo        time(0)      ← no viene del PLC, lo calculamos aquí
#   IdOrden       int
#   IdCliente     smallint
#   PesoCv        float
#   PesoCt        float
#   TempDesh      float
#   TiempoDesh    time(0)
#   TempRecu      float
#   TiempoRecu    time(0)
#   Temp1Crack    float
#   Tiempo1Crack  time(0)
#   TempfinCurva  float
#   TiempofinCurva time(0)
#   TiempoTueste  time(0)
#   TiempoEnfriamiento time(0)
#   Rendimiento   float
#   ConsumoGas    float
#   ConsumoKwh    float
#   FechaHoraIni  int
#   FechaHoraFin  int
#   Nombre        varchar(20)

from typing import Optional
import pyodbc
from config import SQL_CONN, SP_INSERTAR


class SQLWriter:

    def __init__(self):
        self.conn: Optional[pyodbc.Connection] = None

    # ── Conexión ─────────────────────────────────────────────
    def conectar(self) -> bool:
        try:
            self.conn = pyodbc.connect(SQL_CONN, autocommit=False)
            return True
        except pyodbc.Error as e:
            raise ConnectionError(f"Error conectando a SQL Server: {e}")

    def desconectar(self):
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass

    def _asegurar_conexion(self):
        try:
            if self.conn:
                self.conn.cursor().execute("SELECT 1")
                return
        except Exception:
            pass
        self.conectar()

    # ── Insertar en tblConsumosTostion ───────────────────────
    def insertar(self, d: dict) -> int:
        """
        Ejecuta sp_InsertarCurvaTueste con los datos leídos del PLC.
        Retorna el Id insertado (SCOPE_IDENTITY).
        Lanza excepción si falla → el caller lo captura y loguea.

        Parámetros que recibe el SP (coinciden exactamente con
        los campos de tblConsumosTostion excepto Id y FechaIngreso
        que son autogenerados):

            @IdOrden, @IdCliente, @PesoCv, @PesoCt,
            @TempDesh, @TiempoDesh_seg,
            @TempRecu, @TiempoRecu_seg,
            @Temp1Crack, @Tiempo1Crack_seg,
            @TempfinCurva, @TiempofinCurva_seg,
            @TiempoTueste_seg, @TiempoEnfriamiento_seg,
            @Rendimiento, @ConsumoGas, @ConsumoKwh,
            @FechaHoraIni, @FechaHoraFin, @Nombre
        """
        self._asegurar_conexion()

        sql = (
            f"EXEC {SP_INSERTAR} "
            "@IdOrden=?, @IdCliente=?, @PesoCv=?, @PesoCt=?, "
            "@TempDesh=?, @TiempoDesh_seg=?, "
            "@TempRecu=?, @TiempoRecu_seg=?, "
            "@Temp1Crack=?, @Tiempo1Crack_seg=?, "
            "@TempfinCurva=?, @TiempofinCurva_seg=?, "
            "@TiempoTueste_seg=?, @TiempoEnfriamiento_seg=?, "
            "@Rendimiento=?, @ConsumoGas=?, @ConsumoKwh=?, "
            "@FechaHoraIni=?, @FechaHoraFin=?, @Nombre=?"
        )

        params = (
            d["IdOrden"],              d["IdCliente"],
            d["PesoCv"],               d["PesoCt"],
            d["TempDesh"],             d["TiempoDesh_seg"],
            d["TempRecu"],             d["TiempoRecu_seg"],
            d["Temp1Crack"],           d["Tiempo1Crack_seg"],
            d["TempfinCurva"],         d["TiempofinCurva_seg"],
            d["TiempoTueste_seg"],     d["TiempoEnfriamiento_seg"],
            d["Rendimiento"],          d["ConsumoGas"],
            d["ConsumoKwh"],           d["FechaHoraIni"],
            d["FechaHoraFin"],         d["Nombre"],
        )

        cur = self.conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        self.conn.commit()
        return int(row[0]) if row else -1