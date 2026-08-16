import os
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

from app.config import TOKEN
from app.ui_utils import centrar_ventana, poner_icono


def clonar_repos_por_visibilidad(repos, carpeta):
    carpeta_publicos = os.path.join(carpeta, "Publicos")
    carpeta_privados = os.path.join(carpeta, "Privados")
    os.makedirs(carpeta_publicos, exist_ok=True)
    os.makedirs(carpeta_privados, exist_ok=True)

    root = tk.Tk(className='GithubApp')
    root.title("Clonando repositorios...")
    centrar_ventana(root, 720, 420)
    poner_icono(root)
    tk.Label(root, text="Progreso de la clonación:", font=("Arial", 11, "bold")).pack(pady=(10, 5))
    lbl_actual = tk.Label(root, text="", font=("Arial", 10))
    lbl_actual.pack(pady=5)

    total = len(repos)
    errores = 0

    prog = ttk.Progressbar(root, maximum=total, length=450)
    prog.pack(pady=5)

    frame_text = tk.Frame(root)
    frame_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    text = tk.Text(frame_text, height=12, font=("Arial", 10))
    scrollbar = tk.Scrollbar(frame_text, command=text.yview)

    estado_scroll = {"auto": True}
    estado = {"cancelar": False, "process": None}

    def on_yview(*args):
        scrollbar.set(*args)
        if len(args) == 2:
            try:
                estado_scroll["auto"] = float(args[1]) >= 0.999
            except (TypeError, ValueError):
                estado_scroll["auto"] = True

    def on_cerrar():
        if not messagebox.askyesno(
                "Cancelar clonación",
                "¿Seguro/a que quieres cancelar la clonación en curso?"):
            return
        estado["cancelar"] = True
        proceso_actual = estado["process"]
        if proceso_actual is not None and proceso_actual.poll() is None:
            try:
                proceso_actual.terminate()
            except Exception:
                pass
        try:
            root.destroy()
        except Exception:
            pass

    root.protocol("WM_DELETE_WINDOW", on_cerrar)

    def actualizar_gui():
        try:
            root.update()
        except Exception:
            pass

    def agregar_linea(texto):
        try:
            text.insert(tk.END, texto)
            if estado_scroll["auto"]:
                text.see(tk.END)
        except Exception:
            pass
        actualizar_gui()

    text.configure(yscrollcommand=on_yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for i, repo in enumerate(repos, start=1):
        if estado["cancelar"]:
            break

        nombre_repo = repo["name"]
        clone_url = repo["clone_url"].replace("https://github.com/", f"https://{TOKEN}@github.com/")
        destino = carpeta_privados if repo["private"] else carpeta_publicos
        ruta_repo = os.path.join(destino, nombre_repo)

        try:
            lbl_actual.config(text=f"({i}/{total}) {nombre_repo} -> {ruta_repo}")
            prog["value"] = i - 1
        except Exception:
            pass
        actualizar_gui()

        if os.path.exists(ruta_repo):
            agregar_linea(f"Se omite (ya existe): {nombre_repo}\n")
            continue

        try:
            process = subprocess.Popen(
                ["git", "clone", "--quiet", clone_url, ruta_repo],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            estado["process"] = process
            while process.poll() is None:
                actualizar_gui()
                if estado["cancelar"]:
                    try:
                        process.terminate()
                        try:
                            process.wait(timeout=5)
                        except Exception:
                            process.kill()
                    except Exception:
                        pass
                    shutil.rmtree(ruta_repo, ignore_errors=True)
                    break
            try:
                process.wait()
            except Exception:
                pass

            if estado["cancelar"]:
                break
            if process.returncode == 0:
                agregar_linea(f"OK: {nombre_repo}\n")
            else:
                errores += 1
                agregar_linea(f"ERROR: no se pudo clonar {nombre_repo}\n")
        except Exception as e:
            errores += 1
            agregar_linea(f"ERROR: {nombre_repo}: {e}\n")
        finally:
            estado["process"] = None

    if estado["cancelar"]:
        try:
            root.destroy()
        except Exception:
            pass
        return

    if not estado["cancelar"]:
        agregar_linea(f"\n=== Terminado: {total - errores} clonados, {errores} errores ===\n")
        try:
            tk.Button(root, text="Cerrar", width=20, bg="#607D8B", fg="white", command=root.destroy).pack(pady=10)
            root.mainloop()
        except Exception:
            pass

    if errores and not estado["cancelar"]:
        messagebox.showerror("Errores", f"{errores} repositorio(s) no se pudieron clonar.")