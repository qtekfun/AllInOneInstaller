# All in One installer

Este repositorio contiene un script interactivo para automatizar la configuración inicial de una instalación de Windows 11.

## Características

1. **Instalación de aplicaciones** usando `winget`.
2. **Configuración de WSL** (Windows Subsystem for Linux) con Ubuntu como distribución predeterminada.
3. **Instalación de Portmaster**, un firewall avanzado para la privacidad.
4. **Activación de Office y/o Windows** con `irm https://get.activated.win | iex`.

## Archivos

- `apps.txt`: Lista de aplicaciones a instalar.
- `interactive_installer.ps1`: Script interactivo para instalar aplicaciones, configurar WSL, instalar Portmaster y activar Windows/Office.
- `README.md`: Documentación del repositorio.

## Requisitos

- Windows 11 actualizado con soporte para `winget`.
- Permisos de administrador para instalar aplicaciones y configurar WSL.

## Uso

1. **Clona el repositorio o descarga los archivos.**
2. **Abre PowerShell** con permisos de administrador.
3. **Permite la ejecución de scripts:**
   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
