import tkinter as tk
from tkinter import messagebox

from app.acciones import (iniciar_clon, iniciar_eliminar,
                          opcion_cambiar_visibilidad_por_carpeta)
from app.ui_utils import centrar_ventana, poner_icono, reportar_tk_error


def menu_inicial():
    root = tk.Tk(className='GithubApp')
    root.title("Gestor de Repositorios")
    root.resizable(False, False)
    centrar_ventana(root, 500, 430)
    poner_icono(root)
    root.report_callback_exception = reportar_tk_error

    def salir():
        if messagebox.askyesno("Salir", "¿Estás segura de que quieres salir?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", salir)
    tk.Label(root, text="Selecciona una opción:", font=("Arial", 13, "bold")).pack(pady=20)

    tk.Button(root, text="Clonar Repositorios", width=30, height=2, bg="#2196F3", fg="white",
                font=("Arial", 11, "bold"),
                command=lambda: [root.destroy(), iniciar_clon(), menu_inicial()]).pack(pady=12)
    tk.Button(root, text="Eliminar Carpeta 'eliminar'", width=30, height=2, bg="#f44336", fg="white",
                font=("Arial", 11, "bold"),
                command=lambda: [root.destroy(), iniciar_eliminar(), menu_inicial()]).pack(pady=12)
    tk.Button(root, text="Cambiar Visibilidad Carpetas", width=30, height=2, bg="#FF9800", fg="white",
                font=("Arial", 11, "bold"),
                command=lambda: [root.destroy(), opcion_cambiar_visibilidad_por_carpeta(), menu_inicial()]).pack(pady=12)
    tk.Button(root, text="Salir", width=30, height=2, bg="#607D8B", fg="white",
                font=("Arial", 11, "bold"), command=salir).pack(pady=12)

    root.mainloop()


if __name__ == "__main__":
    menu_inicial()