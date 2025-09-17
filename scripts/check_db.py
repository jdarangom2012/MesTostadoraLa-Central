"""Pequeño script para validar conexión ODBC antes de correr migrate."""
import os
import sys

import pyodbc

driver = os.getenv('ODBC_DRIVER', 'ODBC Driver 18 for SQL Server')
server = os.getenv('DB_HOST', 'localhost')
port = os.getenv('DB_PORT', '1433')
database = os.getenv('DB_NAME', 'dbTostadoraCentral')
user = os.getenv('DB_USER', '')
password = os.getenv('DB_PASSWORD', '')
trust = os.getenv('DB_TRUST_CERT', 'yes')
encrypt_flag = os.getenv('DB_ENCRYPT', 'no').lower() in ['1', 'true', 'yes']

parts = [
    f"DRIVER={{{driver}}}",
    f"SERVER={server},{port}" if "," not in server and "\\" not in server else f"SERVER={server}",
    f"DATABASE={database}",
]
if user:
    parts.append(f"UID={user}")
if password:
    parts.append(f"PWD={password}")
if encrypt_flag:
    parts.append("Encrypt=yes")
parts.append(f"TrustServerCertificate={trust}")
conn_str = ";".join(parts)

print("Intentando conexión con:")
print(conn_str)

try:
    with pyodbc.connect(conn_str, timeout=5) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        print("Conexión OK", cursor.fetchone())
except Exception as e:  # noqa
    print("ERROR de conexión:", e)
    sys.exit(1)