import os
from tkinter import messagebox

from app.clonar import clonar_repos_por_visibilidad
from app.eliminar import eliminar_carpeta
from app.github_api import cambiar_visibilidad, obtener_repos
from app.selector_carpeta import seleccionar_carpeta
from app.selector_repos import seleccionar_repos


def opcion_cambiar_visibilidad_por_carpeta():
    carpeta_principal = seleccionar_carpeta("Selecciona la carpeta principal donde están 'Publicos' y 'Privados'")
    if not carpeta_principal:
        return

    publicos_path = os.path.join(carpeta_principal, "Publicos")
    privados_path = os.path.join(carpeta_principal, "Privados")

    if not os.path.exists(publicos_path) and not os.path.exists(privados_path):
        messagebox.showinfo("Info", "No se encontraron carpetas 'Publicos' o 'Privados'.")
        return

    repos = obtener_repos()
    if not repos:
        return

    repos_dict = {r["name"]: r for r in repos}

    if os.path.exists(publicos_path):
        for nombre_repo in os.listdir(publicos_path):
            if nombre_repo in repos_dict and repos_dict[nombre_repo]["private"]:
                cambiar_visibilidad(repos_dict[nombre_repo], False)

    if os.path.exists(privados_path):
        for nombre_repo in os.listdir(privados_path):
            if nombre_repo in repos_dict and not repos_dict[nombre_repo]["private"]:
                cambiar_visibilidad(repos_dict[nombre_repo], True)

    messagebox.showinfo("Listo", "Visibilidad actualizada según carpetas.")


def iniciar_clon():
    repos = obtener_repos()
    if not repos:
        return
    seleccionados = seleccionar_repos(repos)
    if not seleccionados:
        return
    carpeta = seleccionar_carpeta()
    if not carpeta:
        return
    clonar_repos_por_visibilidad(seleccionados, carpeta)
    messagebox.showinfo("Listo", f"Repos clonados en {carpeta} separados por visibilidad")


def iniciar_eliminar():
    carpeta_principal = seleccionar_carpeta("Selecciona la carpeta principal donde está 'eliminar'")
    if not carpeta_principal:
        return
    eliminar_carpeta(carpeta_principal)