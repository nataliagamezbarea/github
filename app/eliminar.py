import os
import shutil

import requests
from tkinter import messagebox

from app.config import TOKEN, USUARIO


def eliminar_carpeta(carpeta_principal):
    carpeta = os.path.join(carpeta_principal, "eliminar")
    if not os.path.exists(carpeta):
        messagebox.showinfo("Info", "No se encontró la carpeta 'eliminar'.")
        return
    elementos = os.listdir(carpeta)
    if not elementos:
        messagebox.showinfo("Info", "La carpeta 'eliminar' está vacía.")
        return

    lista_elementos = "\n".join(elementos)
    if not messagebox.askyesno("Confirmar", f"Se eliminarán los siguientes repos:\n\n{lista_elementos}\n\n¿Continuar?"):
        return

    headers = {"Authorization": f"token {TOKEN}"}
    for item in elementos:
        url = f"https://api.github.com/repos/{USUARIO}/{item}"
        try:
            r = requests.delete(url, headers=headers)
            if r.status_code == 204:
                print(f"Repositorio remoto eliminado: {item}")
            else:
                messagebox.showerror("Error", f"No se pudo eliminar remoto {item}:\n{r.text}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar remoto {item}:\n{e}")

        item_path = os.path.join(carpeta, item)
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar local {item_path}:\n{e}")

    messagebox.showinfo("Listo", "Repositorios eliminados en remoto y local.")