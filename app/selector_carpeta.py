import os
import tkinter as tk
from tkinter import messagebox

from app.carpetas import (borrar_items, confirmar_vaciar_carpeta,
                          es_carpeta_protegida, ventana_elegir_items_a_vaciar)
from app.ui_utils import centrar_ventana, poner_icono


def seleccionar_carpeta(titulo="Selecciona una carpeta", initialdir=None):
    if initialdir is None:
        initialdir = os.path.expanduser("~")
    if not os.path.isdir(initialdir):
        initialdir = os.path.expanduser("~")

    resultado = {"sel": None}

    root = tk.Tk(className='GithubApp')
    root.title(titulo)
    root.resizable(False, False)
    centrar_ventana(root, 580, 540)
    poner_icono(root)

    home = os.path.expanduser("~")
    var_ruta = tk.StringVar()

    tk.Label(root, text="Carpeta actual:", font=("Arial", 10, "bold")).pack(anchor="w", padx=12, pady=(12, 2))

    frame_ruta = tk.Frame(root)
    frame_ruta.pack(fill=tk.X, padx=12)
    entry_ruta = tk.Entry(frame_ruta, textvariable=var_ruta, font=("Arial", 10))
    entry_ruta.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def ir_a_ruta():
        ruta = var_ruta.get().strip()
        if not ruta or not os.path.isdir(ruta):
            messagebox.showerror("Error", "No existe esa carpeta.\nEscribe una ruta válida y pulsa 'Ir'.")
            return
        refrescar(ruta)

    tk.Button(frame_ruta, text="Ir", width=6, bg="#FF9800", fg="white",
                font=("Arial", 9, "bold"), command=ir_a_ruta).pack(side=tk.LEFT, padx=(6, 0))

    frame_botones = tk.Frame(root)
    frame_botones.pack(fill=tk.X, padx=12, pady=6)
    tk.Button(frame_botones, text="Home", width=8, bg="#4CAF50", fg="white",
                font=("Arial", 9, "bold"), command=lambda: refrescar(home)).grid(row=0, column=0, padx=2)
    tk.Button(frame_botones, text="Escritorio", width=9, bg="#2196F3", fg="white",
                font=("Arial", 9, "bold"),
                command=lambda: refrescar(os.path.join(home, "Escritorio"))).grid(row=0, column=1, padx=2)
    tk.Button(frame_botones, text="Documentos", width=10, bg="#2196F3", fg="white",
                font=("Arial", 9, "bold"),
                command=lambda: refrescar(os.path.join(home, "Documentos"))).grid(row=0, column=2, padx=2)
    tk.Button(frame_botones, text="Descargas", width=10, bg="#2196F3", fg="white",
                font=("Arial", 9, "bold"),
                command=lambda: refrescar(os.path.join(home, "Descargas"))).grid(row=0, column=3, padx=2)
    tk.Button(frame_botones, text="Raíz /", width=7, bg="#607D8B", fg="white",
                font=("Arial", 9, "bold"), command=lambda: refrescar("/")).grid(row=0, column=4, padx=2)

    tk.Button(root, text="▲ Subir", width=10, bg="#FF9800", fg="white",
                font=("Arial", 9, "bold"),
                command=lambda: refrescar(os.path.dirname(var_ruta.get()))).pack(anchor="w", padx=12)

    listbox = tk.Listbox(root, width=80, height=12, font=("Arial", 10))
    scroll = tk.Scrollbar(listbox, command=listbox.yview)
    listbox.configure(yscrollcommand=scroll.set)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.pack(fill=tk.BOTH, expand=True, padx=12)

    def refrescar(carpeta):
        carpeta = os.path.abspath(carpeta)
        if not os.path.isdir(carpeta):
            messagebox.showerror("Error", f"No existe la carpeta:\n{carpeta}")
            return
        var_ruta.set(carpeta)
        listbox.delete(0, tk.END)
        try:
            entradas = sorted(os.listdir(carpeta))
        except PermissionError:
            entradas = []
        for nombre in entradas:
            if os.path.isdir(os.path.join(carpeta, nombre)):
                listbox.insert(tk.END, nombre)
        proteccion = es_carpeta_protegida(carpeta)
        if proteccion:
            btn_usar.config(state=tk.DISABLED)
            lbl_protegida.config(
                text="Carpeta protegida: el botón 'Usar esta carpeta' está desactivado. Entra en una subcarpeta.")
        else:
            btn_usar.config(state=tk.NORMAL)
            lbl_protegida.config(text="")

    def entrar(idx):
        nombre = listbox.get(idx)
        refrescar(os.path.join(var_ruta.get(), nombre))

    listbox.bind("<Double-Button-1>", lambda e: entrar(listbox.nearest(e.y)))

    def usar():
        ruta = var_ruta.get().strip()
        if not os.path.isdir(ruta):
            messagebox.showerror("Error", "No existe esa carpeta.")
            return
        if es_carpeta_protegida(ruta):
            return

        win = tk.Toplevel(root)
        win.title("Confirmar carpeta")
        win.resizable(False, False)
        centrar_ventana(win, 560, 230)
        poner_icono(win)

        tk.Label(win, text=f"¿Usar esta carpeta?\n\n{ruta}", font=("Arial", 10),
                    wraplength=520, justify="left").pack(padx=15, pady=(14, 4))

        var_vaciar = tk.BooleanVar(value=False)
        chk = tk.Checkbutton(win, text="Vaciar esta carpeta antes de usarla",
                                variable=var_vaciar, font=("Arial", 10))
        chk.pack(pady=4)

        def aceptar():
            try:
                tiene_contenido = bool(os.listdir(ruta))
            except PermissionError:
                messagebox.showerror("Error", f"Sin permisos para leer:\n{ruta}")
                return
            if var_vaciar.get() and tiene_contenido:
                if not confirmar_vaciar_carpeta(ruta, win):
                    return
                refrescar(ruta)
            resultado["sel"] = ruta
            win.destroy()
            root.destroy()

        frame_btn = tk.Frame(win)
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="Aceptar", width=12, bg="#4CAF50", fg="white",
                    font=("Arial", 10, "bold"), command=aceptar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="Cancelar", width=12, bg="#607D8B", fg="white",
                    font=("Arial", 10, "bold"), command=win.destroy).pack(side=tk.LEFT, padx=5)

        win.transient(root)
        win.grab_set()
        win.mainloop()

    def vaciar():
        ruta = var_ruta.get().strip()
        if not os.path.isdir(ruta):
            messagebox.showerror("Error", "No existe esa carpeta.")
            return
        if es_carpeta_protegida(ruta):
            messagebox.showerror(
                "Vaciar carpeta",
                "Esta es una carpeta protegida (Escritorio, Documentos, Descargas u otra carpeta importante).\n\n"
                "No se puede vaciar.")
            return
        seleccion = ventana_elegir_items_a_vaciar(ruta, root)
        if seleccion is None:
            return
        borrar_items(ruta, seleccion)
        resultado["sel"] = ruta
        refrescar(ruta)

    lbl_protegida = tk.Label(root, text="", font=("Arial", 9), fg="#B71C1C",
                                wraplength=540, justify="left")
    lbl_protegida.pack(anchor="w", padx=12, pady=(2, 0))

    tk.Label(root, text="Doble clic entra en una carpeta. 'Usar esta carpeta' confirma la carpeta mostrada "
                        "(con casilla para vaciarla antes).",
                font=("Arial", 9), fg="#666666", wraplength=540, justify="left").pack(pady=(2, 0))

    frame_final = tk.Frame(root)
    frame_final.pack(pady=8)
    btn_usar = tk.Button(frame_final, text="Usar esta carpeta", width=18, bg="#4CAF50", fg="white",
                            font=("Arial", 10, "bold"), command=usar)
    btn_usar.pack(side=tk.LEFT, padx=5)
    tk.Button(frame_final, text="Cancelar", width=12, bg="#607D8B", fg="white",
                font=("Arial", 10, "bold"), command=root.destroy).pack(side=tk.LEFT, padx=5)

    refrescar(initialdir)
    root.mainloop()

    if not resultado["sel"]:
        return None
    return resultado["sel"]