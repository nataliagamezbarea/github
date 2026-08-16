import traceback
import tkinter as tk
from tkinter import messagebox

from app.config import ICONO


def poner_icono(root):
    if ICONO:
        try:
            root.iconphoto(True, ICONO)
        except Exception:
            pass


def centrar_ventana(root, ancho, alto):
    root.update_idletasks()
    x = max((root.winfo_screenwidth() - ancho) // 2, 0)
    y = max((root.winfo_screenheight() - alto) // 2, 0)
    root.geometry(f"{ancho}x{alto}+{x}+{y}")


def reportar_tk_error(exc, value, tb):
    try:
        messagebox.showerror("Error interno",
                             "Ocurrió un error:\n\n" + "".join(traceback.format_exception(exc, value, tb)))
    except Exception:
        pass
    return True