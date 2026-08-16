import tkinter as tk
from tkinter import messagebox

from app.ui_utils import centrar_ventana, poner_icono


def seleccionar_repos(repos, titulo="Seleccionar Repositorios"):
    if not repos:
        messagebox.showinfo("Info", "No hay repositorios para seleccionar.")
        return None

    seleccionados = set()

    def toggle(idx):
        if idx in seleccionados:
            seleccionados.remove(idx)
        else:
            seleccionados.add(idx)
        actualizar_lista()

    def seleccionar_todo():
        seleccionados.update(range(len(repos)))
        actualizar_lista()

    def seleccionar_privados():
        seleccionados.clear()
        for i, r in enumerate(repos):
            if r["private"]:
                seleccionados.add(i)
        actualizar_lista()

    def seleccionar_publicos():
        seleccionados.clear()
        for i, r in enumerate(repos):
            if not r["private"]:
                seleccionados.add(i)
        actualizar_lista()

    def desmarcar_todo():
        seleccionados.clear()
        actualizar_lista()

    def confirmar_seleccion():
        root.destroy()

    def actualizar_lista():
        listbox.delete(0, tk.END)
        for i, repo in enumerate(repos):
            mark = "[X]" if i in seleccionados else "[ ]"
            estado = "Privado" if repo["private"] else "Público"
            listbox.insert(tk.END, f"{mark} {repo['name']} ({estado})")

    root = tk.Tk(className='GithubApp')
    root.title(titulo)
    root.resizable(False, False)
    centrar_ventana(root, 800, 700)
    poner_icono(root)

    listbox = tk.Listbox(root, width=70, height=25, font=("Arial", 10))
    listbox.pack(pady=15)
    actualizar_lista()

    frame = tk.Frame(root)
    frame.pack(pady=10)
    
    tk.Button(frame, text="Seleccionar Todo", width=20, bg="#4CAF50", fg="white", command=seleccionar_todo).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(frame, text="Seleccionar Privados", width=20, bg="#2196F3", fg="white", command=seleccionar_privados).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(frame, text="Seleccionar Públicos", width=20, bg="#FF9800", fg="white", command=seleccionar_publicos).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(frame, text="Desmarcar Todo", width=20, bg="#f44336", fg="white", command=desmarcar_todo).grid(row=1, column=1, pady=5)
    tk.Button(frame, text="Confirmar", width=20, bg="#607D8B", fg="white", command=confirmar_seleccion).grid(row=2, column=1, pady=10)

    root.mainloop()
    if not seleccionados:
        return None
    return [repos[i] for i in seleccionados]