import json
import os
import shutil
import winreg as reg


def get_browser_path(browser_name):
    """Devuelve la ruta del directorio de extensiones del navegador."""
    user_dir = os.getenv("LOCALAPPDATA")
    browser_paths = {
        "Brave": os.path.join(user_dir, "BraveSoftware", "Brave-Browser", "User Data", "Default", "Extensions"),
        "Chrome": os.path.join(user_dir, "Google", "Chrome", "User Data", "Default", "Extensions"),
        "Edge": r"SOFTWARE\Policies\Microsoft\Edge\ExtensionInstallForcelist",
    }
    return browser_paths.get(browser_name)

def validate_json_file(file_path):
    """Valida si el archivo JSON tiene un formato adecuado para extensiones."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, list) and all("id" in ext for ext in data):
            return data
        else:
            print("El archivo JSON no tiene el formato adecuado.")
            return None
    except Exception as e:
        print(f"Error al leer o validar el archivo JSON: {e}")
        return None

def import_extensions():
    # Navegadores compatibles
    browsers = {
        "1": "Brave",
        "2": "Chrome",
        "3": "Edge",
    }

    print("Navegadores compatibles para importar extensiones:")
    for key, name in browsers.items():
        print(f"{key}. {name}")

    # Seleccionar navegador
    browser_choice = input("Selecciona el navegador para importar extensiones (1/2/3): ")
    if browser_choice not in browsers:
        print("Opción no válida.")
        return

    browser_name = browsers[browser_choice]
    browser_path = get_browser_path(browser_name)

    # Elegir el archivo JSON
    json_file = input("Ingresa el nombre del archivo JSON de respaldo (incluyendo la extensión .json): ")
    if not os.path.exists(json_file):
        print(f"No se encontró el archivo: {json_file}")
        return

    # Validar el archivo JSON
    extensions = validate_json_file(json_file)
    if not extensions:
        return

    # Procesar importación
    if browser_name in ["Brave", "Chrome"]:
        if not os.path.exists(browser_path):
            print(f"No se encontró el directorio de extensiones para {browser_name}.")
            return

        print(f"Copiando extensiones a {browser_name}...")
        for ext in extensions:
            ext_id = ext["id"]
            ext_path = os.path.join(browser_path, ext_id)
            os.makedirs(ext_path, exist_ok=True)
            print(f"Directorio creado para la extensión: {ext_id}")
        print(f"Extensiones importadas a {browser_name} desde {json_file}.")

    elif browser_name == "Edge":
        try:
            reg_key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, browser_path)
            for index, extension in enumerate(extensions, start=1):
                extension_id = extension["id"]
                update_url = "https://clients2.google.com/service/update2/crx"
                reg.SetValueEx(reg_key, str(index), 0, reg.REG_SZ, f"{extension_id};{update_url}")
            reg.CloseKey(reg_key)
            print(f"Extensiones importadas a Edge desde {json_file}")
        except PermissionError:
            print("Error: Debes ejecutar este script como administrador.")
        except Exception as e:
            print(f"Error al configurar extensiones en el Registro: {e}")
    else:
        print(f"Importación para {browser_name} no soportada actualmente.")

# Ejecutar el script de importación
import_extensions()
