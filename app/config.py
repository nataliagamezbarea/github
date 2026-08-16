import os
import tkinter as tk
from dotenv import load_dotenv

# ==========================
# CARGAR VARIABLES DE .ENV
# ==========================
load_dotenv()
TOKEN = os.getenv("TOKEN")
USUARIO = os.getenv("USER")

if not TOKEN or not USUARIO:
    raise ValueError("Debes definir TOKEN y USER en el archivo .env")

# ==========================
# ICONO DE LA APLICACIÓN
# ==========================
ICONO = None
try:
    ICONO = tk.PhotoImage(file="/app/icon.png")
except Exception:
    ICONO = None