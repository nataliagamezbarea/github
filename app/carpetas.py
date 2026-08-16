import os
import shutil
import tkinter as tk
from tkinter import messagebox

from app.ui_utils import centrar_ventana, poner_icono


def carpetas_protegidas():
    home = os.path.expanduser("~")
    return {
        "/",
        home,
        os.path.join(home, "Escritorio"),
        os.path.join(home, "Documentos"),
        os.path.join(home, "Descargas"),
        os.path.join(home, "Imágenes"),
        os.path.join(home, "Musica"),
        os.path.join(home, "Música"),
        os.path.join(home, "Videos"),
        os.path.join(home, "Vídeos"),
        os.path.join(home, "Plantillas"),
        os.path.join(home, "Publico"),
        os.path.join(home, "Público"),
    }


def es_carpeta_protegida(ruta):
    return os.path.abspath(ruta) in carpetas_protegidas()


def ventana_elegir_items_a_vaciar(ruta, padre):
    try:
        items = sorted(os.listdir(ruta))
    except (PermissionError, OSError):
        items = []
    if not items:
        messagebox.showinfo("Vaciar carpeta", "La carpeta está vacía.")
        return set()

    resultado = {"ok": None}

    win = tk.Toplevel(padre)
    win.title("Elegir qué vaciar")
    win.resizable(False, False)
    centrar_ventana(win, 580, min(80 + len(items) * 30, 460))
    poner_icono(win)

    tk.Label(win, text=f"Contenido de:\n{ruta}\n\nMarca lo que quieres vaciar:",
                font=("Arial", 10), justify="left", wraplength=550).pack(padx=15, pady=(12, 6))

    frame_canvas = tk.Frame(win)
    frame_canvas.pack(fill=tk.BOTH, expand=True, padx=15)
    canvas = tk.Canvas(frame_canvas, width=540, height=min(40 + len(items) * 26, 300))
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    sbar = tk.Scrollbar(frame_canvas, orient=tk.VERTICAL, command=canvas.yview)
    sbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=sbar.set)

    frame = tk.Frame(canvas)
    win_id = canvas.create_window((0, 0), window=frame, anchor="nw")

    def _configurar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfigure(win_id, width=event.width)

    canvas.bind("<Configure>", _configurar_scroll)

    variables = {}
    for nombre in items:
        v = tk.BooleanVar(value=True)
        variables[nombre] = v
        tk.Checkbutton(frame, text=nombre, variable=v, font=("Arial", 10), anchor="w").pack(fill=tk.X, pady=1)

    def confirmar():
        resultado["ok"] = {nombre for nombre, v in variables.items() if v.get()}
        win.destroy()

    frame_btn = tk.Frame(win)
    frame_btn.pack(pady=8)
    tk.Button(frame_btn, text="Vaciar lo marcado", width=18, bg="#f44336", fg="white",
                font=("Arial", 10, "bold"), command=confirmar).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn, text="Cancelar", width=12, bg="#607D8B", fg="white",
                font=("Arial", 10, "bold"), command=win.destroy).pack(side=tk.LEFT, padx=5)

    win.transient(padre)
    win.grab_set()
    win.mainloop()

    if resultado["ok"] is None:
        return None
    return resultado["ok"]


def borrar_items(ruta, seleccion):
    errores = 0
    borrados = 0
    for nombre in seleccion:
        ruta_item = os.path.join(ruta, nombre)
        try:
            if os.path.isdir(ruta_item) and not os.path.islink(ruta_item):
                shutil.rmtree(ruta_item)
            else:
                os.remove(ruta_item)
            borrados += 1
        except Exception:
            errores += 1
    if errores:
        messagebox.showerror("Vaciar carpeta",
                                f"{borrados} elemento(s) borrados, pero {errores} no se pudieron eliminar.")
    elif borrados:
        messagebox.showinfo("Vaciar carpeta", f"Se vaciaron los elementos marcados:\n{ruta}")


def confirmar_vaciar_carpeta(ruta, padre):
    if es_carpeta_protegida(ruta):
        messagebox.showerror(
            "Vaciar carpeta",
            "Esta es una carpeta protegida (Escritorio, Documentos, Descargas u otra carpeta importante).\n\n"
            "No se puede vaciar.")
        return False

    resultado = {"ok": False}

    win = tk.Toplevel(padre)
    win.title("Vaciar carpeta")
    win.resizable(False, False)
    centrar_ventana(win, 560, 240)
    poner_icono(win)

    tk.Label(win, text=f"Se vaciará TODO el contenido de:\n\n{ruta}", font=("Arial", 10),
                wraplength=520, justify="left").pack(padx=15, pady=(14, 4))

    var_check = tk.BooleanVar(value=False)
    chk = tk.Checkbutton(win, text="Sí, quiero vaciar esta carpeta (no se puede deshacer)",
                            variable=var_check, font=("Arial", 10))
    chk.pack(pady=8)

    def ejecutar():
        if not var_check.get():
            messagebox.showwarning("Vaciar carpeta",
                                    "Marca la casilla para confirmar que quieres vaciarla.")
            return
        try:
            elementos = os.listdir(ruta)
        except PermissionError:
            messagebox.showerror("Vaciar carpeta", f"Sin permisos para leer:\n{ruta}")
            return
        errores = 0
        borrados = 0
        for nombre in elementos:
            ruta_item = os.path.join(ruta, nombre)
            try:
                if os.path.isdir(ruta_item) and not os.path.islink(ruta_item):
                    shutil.rmtree(ruta_item)
                else:
                    os.remove(ruta_item)
                borrados += 1
            except Exception:
                errores += 1
        if errores:
            messagebox.showerror("Vaciar carpeta",
                                    f"{borrados} elemento(s) borrados, pero {errores} no se pudieron eliminar.")
        else:
            messagebox.showinfo("Vaciar carpeta", f"Carpeta vaciada:\n{ruta}")
        resultado["ok"] = True
        win.destroy()

    frame_btn = tk.Frame(win)
    frame_btn.pack(pady=10)
    tk.Button(frame_btn, text="Vaciar", width=12, bg="#f44336", fg="white",
                font=("Arial", 10, "bold"), command=ejecutar).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn, text="Cancelar", width=12, bg="#607D8B", fg="white",
                font=("Arial", 10, "bold"), command=win.destroy).pack(side=tk.LEFT, padx=5)

    win.transient(padre)
    win.grab_set()
    win.mainloop()
    return resultado["ok"]