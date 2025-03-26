import tkinter as tk
from tkinter import messagebox, ttk
import socket
import requests
import os
import sys
import threading
import subprocess
import platform

def verificar_terminos_condiciones():
    """Muestra términos y condiciones solo si es la primera ejecución."""
    terms_file = os.path.join(os.path.dirname(sys.executable), "terms_accepted.txt")
    
    if os.path.exists(terms_file):
        return True

    root = tk.Tk()
    root.title("Términos y Condiciones")
    root.geometry("800x600")
    root.resizable(False, False)
    
    # Centrar ventana
    pantalla_ancho = root.winfo_screenwidth()
    pantalla_alto = root.winfo_screenheight()
    x = (pantalla_ancho - 800) // 2
    y = (pantalla_alto - 600) // 2
    root.geometry(f"800x600+{x}+{y}")

    texto = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), height=20)
    texto.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=texto.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    texto['yscrollcommand'] = scrollbar.set

    terminos = """
    TÉRMINOS Y CONDICIONES DE USO:
    
    """
    
    texto.insert(tk.END, terminos)
    texto.configure(state=tk.DISABLED)

    aceptado = False

    def aceptar():
        nonlocal aceptado
        aceptado = True
        root.destroy()

    def declinar():
        root.destroy()

    frame_botones = tk.Frame(root)
    frame_botones.pack(pady=20)

    tk.Button(frame_botones, text="ACEPTAR", command=aceptar, width=15, bg="green", fg="white").pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botones, text="RECHAZAR", command=declinar, width=15, bg="red", fg="white").pack(side=tk.RIGHT, padx=10)

    root.protocol("WM_DELETE_WINDOW", declinar)
    root.mainloop()

    if aceptado:
        with open(terms_file, "w") as f:
            f.write("Términos aceptados por el usuario")
        return True
    return False

def agregar_al_inicio_windows():
    """Agrega el programa al inicio de Windows si no existe."""
    if platform.system() != "Windows":
        return

    try:
        import winreg
        
        clave_reg = r"Software\Microsoft\Windows\CurrentVersion\Run"
        nombre_app = "F"
        ruta_ejecutable = sys.executable

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, clave_reg, 0, winreg.KEY_ALL_ACCESS) as key:
            try:
                valor_actual, _ = winreg.QueryValueEx(key, nombre_app)
                if valor_actual == ruta_ejecutable:
                    return
            except FileNotFoundError:
                pass

            winreg.SetValueEx(key, nombre_app, 0, winreg.REG_SZ, ruta_ejecutable)
    except Exception as e:
        print(f"No se pudo agregar al inicio: {e}")

def verificar_conexion_internet():
    """Verifica si hay conexión a Internet y retorna el resultado sin ventana emergente."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        print("Conexión a Internet exitosa.")
        return True
    except OSError:
        print("No hay conexión a Internet.")
        return False

def descargar_actualizacion(url, progress_var, progress_bar, progress_window):
    """Descarga la nueva versión del programa con una barra de progreso."""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        total_length = int(response.headers.get('content-length', 0))
        nuevo_archivo = os.path.join(os.path.dirname(sys.executable), os.path.basename(url))

        with open(nuevo_archivo, "wb") as file:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)
                    if total_length != 0:
                        porcentaje = (downloaded / total_length) * 100
                        progress_var.set(porcentaje)
                        progress_bar.update()

        progress_window.destroy()
        return nuevo_archivo
    except Exception as e:
        progress_window.destroy()
        raise Exception(f"Error al descargar la actualización: {e}")

def ejecutar_actualizacion(nuevo_archivo):
    """Ejecuta el nuevo archivo descargado y cierra el programa actual."""
    try:
        subprocess.Popen([nuevo_archivo], shell=False)
        sys.exit()
    except Exception as e:
        raise Exception(f"Error al ejecutar el archivo descargado: {e}")

def verificar_version_general(version_actual):
    """Verifica si la versión general está actualizada y maneja la actualización."""
    try:
        version_url = "https://raw.githubusercontent.com/LuisAnthony1/MPR/main/version.txt"
        response = requests.get(version_url, timeout=10)
        response.raise_for_status()
        version_remota = response.text.strip()

        if version_actual == version_remota:
            return True

        root = tk.Tk()
        root.withdraw()
        respuesta = messagebox.askyesno("Nueva versión disponible", f"Se ha detectado una nueva versión ({version_remota}). ¿Quieres descargarla ahora?")
        root.destroy()

        if not respuesta:
            messagebox.showwarning("Actualización cancelada", "Has decidido no actualizar. El programa se cerrará.")
            sys.exit()

        download_url = f"https://github.com/LuisAnthony1/MPR/releases/latest/download/MPR.{version_remota}.exe"
        progress_window = tk.Tk()
        progress_window.title("Descargando Actualización")
        progress_window.geometry("500x150")
        progress_window.resizable(False, False)
        progress_window.attributes('-topmost', 1)

        screen_width = progress_window.winfo_screenwidth()
        screen_height = progress_window.winfo_screenheight()
        window_width, window_height = 500, 150
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        progress_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        tk.Label(progress_window, text="¡Descargando actualización!", font=("Arial", 14)).pack(pady=10)
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=100)
        progress_bar.pack(pady=10, padx=20, fill=tk.X)
        tk.Label(progress_window, text="Por favor, no cierres esta ventana.", font=("Arial", 10), fg="red").pack(pady=5)

        def descargar_thread():
            try:
                nuevo_archivo = descargar_actualizacion(download_url, progress_var, progress_bar, progress_window)
                messagebox.showinfo("Actualización", "¡Actualización descargada con éxito! Ejecutando el nuevo programa...")
                ejecutar_actualizacion(nuevo_archivo)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                sys.exit()

        threading.Thread(target=descargar_thread, daemon=True).start()
        progress_window.mainloop()
        return False  # No continúa si se inicia la actualización

    except requests.RequestException as e:
        messagebox.showerror("Error de conexión", f"No se pudo verificar la actualización: {e}")
        sys.exit()
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado al verificar la actualización: {e}")
        sys.exit()

def eliminar_archivos_mpr():
    """Elimina todos los ejecutables antiguos que comiencen con 'MPR'."""
    try:
        directorio = os.path.dirname(sys.executable)
        for archivo in os.listdir(directorio):
            if archivo.startswith("MPR") and archivo.endswith(".exe") and archivo != os.path.basename(sys.executable):
                os.remove(os.path.join(directorio, archivo))
                print(f"Archivo eliminado: {archivo}")
    except Exception as e:
        print(f"Error al eliminar archivos: {e}")

def main():
    # Paso 1: Verificar términos y condiciones
    if not verificar_terminos_condiciones():
        print("Términos y condiciones no aceptados. El programa se cerrará.")
        sys.exit()

    # Paso 2: Agregar al inicio de Windows (silencioso, no detiene el flujo)
    agregar_al_inicio_windows()

    # Paso 3: Verificar conexión a Internet
    if not verificar_conexion_internet():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error de Conexión", "No hay conexión a Internet. Por favor, verifica tu conexión y reinicia el programa.")
        root.destroy()
        sys.exit()

    # Paso 4: Verificar versión general
    version_actual = "V5.1.0"
    
    if not verificar_version_general(version_actual):
        return  # No continúa si se inicia la actualización

    # Paso 5: Eliminar archivos antiguos
    eliminar_archivos_mpr()

    # Paso 6: Importar y lanzar el sistema de confirmaciones
    try:
        import sistema_confirmaciones
        sistema_confirmaciones.pre_menu()
    except ImportError as e:
        messagebox.showerror("Error de Importación", f"No se pudo importar el Sistema de confirmaciones: {e}")
        sys.exit()
    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar el menú principal: {e}")
        sys.exit()

if __name__ == "__main__":
    main()