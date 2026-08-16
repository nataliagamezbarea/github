import requests
from tkinter import messagebox

from app.config import TOKEN, USUARIO


def obtener_repos():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/user/repos?per_page=100&page={page}"
        try:
            r = requests.get(url, auth=(USUARIO, TOKEN))
            r.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener repositorios:\n{e}")
            return None
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos


def cambiar_visibilidad(repo, hacer_privado):
    url = f"https://api.github.com/repos/{USUARIO}/{repo['name']}"
    headers = {"Authorization": f"token {TOKEN}"}
    data = {"private": hacer_privado}
    try:
        r = requests.patch(url, json=data, headers=headers)
        r.raise_for_status()
        estado = "Privado" if hacer_privado else "Público"
        print(f"{repo['name']} ahora es {estado}")
        repo["private"] = hacer_privado
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar {repo['name']}:\n{e}")
        return False