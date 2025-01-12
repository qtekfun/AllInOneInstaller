import json
import os


def get_browser_path(browser_name):
    user_dir = os.getenv("LOCALAPPDATA")
    browser_paths = {
        "Brave": os.path.join(user_dir, "BraveSoftware", "Brave-Browser", "User Data", "Default", "Extensions"),
        "Chrome": os.path.join(user_dir, "Google", "Chrome", "User Data", "Default", "Extensions"),
        "Edge": os.path.join(user_dir, "Microsoft", "Edge", "User Data", "Default", "Extensions"),
    }
    return browser_paths.get(browser_name)

def export_extensions():
    # Mostrar navegadores disponibles
    browsers = ["Brave", "Chrome", "Edge"]
    print("Navegadores compatibles:")
    for i, browser in enumerate(browsers, start=1):
        print(f"{i}. {browser}")

    # Seleccionar navegador
    choice = int(input("Selecciona el navegador para exportar extensiones (1/2/3): "))
    browser_name = browsers[choice - 1]
    browser_path = get_browser_path(browser_name)

    if not browser_path or not os.path.exists(browser_path):
        print(f"No se encontró la ruta para {browser_name}.")
        return

    # Exportar extensiones
    extensions = []
    print(f"Explorando extensiones en: {browser_path}")
    for folder in os.listdir(browser_path):
        folder_path = os.path.join(browser_path, folder)
        for root, _, files in os.walk(folder_path):
            if "manifest.json" in files:
                manifest_path = os.path.join(root, "manifest.json")
                try:
                    with open(manifest_path, "r", encoding="utf-8") as file:
                        manifest = json.load(file)
                        extensions.append({
                            "id": folder,
                            "name": manifest.get("name", "Unknown"),
                            "version": manifest.get("version", "Unknown"),
                        })
                        print(f"Extensión encontrada: {manifest.get('name', 'Unknown')} (ID: {folder})")
                except Exception as e:
                    print(f"Error leyendo {manifest_path}: {e}")

    # Guardar extensiones en un archivo JSON
    output_file = f"{browser_name.lower()}_extensions_backup.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(extensions, file, indent=4)
    print(f"Extensiones extraídas y guardadas en {output_file}")

# Ejecutar exportación
export_extensions()
