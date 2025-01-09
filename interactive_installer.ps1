# Configuración
$appsFile = "apps.txt"
$portmasterInstaller = "https://updates.safing.io/latest/windows-installer.exe"
$tempDir = "$env:TEMP\PortmasterInstaller.exe"

# Comprobar si se ejecuta como administrador
function Ensure-Admin {
    if (-not ([bool](New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))) {
        Write-Host "Este script debe ejecutarse como administrador. Reiniciando como administrador..." -ForegroundColor Yellow
        Start-Process -FilePath "powershell" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
        exit
    }
}

# Función para instalar aplicaciones usando winget
function Install-Apps {
    if (-not (Get-Command "winget" -ErrorAction SilentlyContinue)) {
        Write-Host "winget no está instalado o no está disponible en el PATH. Actualiza Windows para obtener winget." -ForegroundColor Red
        return
    }

    if (-not (Test-Path $appsFile)) {
        Write-Host "El archivo '$appsFile' no existe. Crea una lista de aplicaciones." -ForegroundColor Red
        return
    }

    $apps = Get-Content $appsFile | Where-Object { $_ -notmatch "^\s*$" }

    Write-Host "Instalando las siguientes aplicaciones:" -ForegroundColor Green
    $apps | ForEach-Object { Write-Host "- $_" }

    foreach ($app in $apps) {
        Write-Host "Instalando $app..." -ForegroundColor Yellow
        try {
            winget install --id $app --silent --accept-package-agreements --accept-source-agreements
            Write-Host "$app instalado con éxito." -ForegroundColor Green
        } catch {
            Write-Host ("Error instalando $app : $_") -ForegroundColor Red

        }
    }
}

# Función para instalar Portmaster
function Install-Portmaster {
    Write-Host "Verificando si Portmaster ya está instalado..." -ForegroundColor Cyan
    $portmasterPath = "C:\Program Files\Safing Portmaster"

    if (Test-Path $portmasterPath) {
        Write-Host "Portmaster ya está instalado." -ForegroundColor Green
        return
    }

    Write-Host "Descargando e instalando Portmaster..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $portmasterInstaller -OutFile $tempDir
        Start-Process -FilePath $tempDir -ArgumentList "/S" -Wait
        Remove-Item $tempDir -Force
        Write-Host "Portmaster instalado con éxito." -ForegroundColor Green
    } catch {
        Write-Host "Error instalando Portmaster: $_" -ForegroundColor Red
    }
}

# Función para configurar WSL
function Configure-WSL {
    Write-Host "Verificando WSL..." -ForegroundColor Cyan
    if (wsl --list --quiet) {
        Write-Host "WSL ya está instalado." -ForegroundColor Green
    } else {
        Write-Host "Instalando WSL..." -ForegroundColor Yellow
        wsl --install
        Write-Host "WSL instalado con éxito. Reinicia tu computadora para finalizar la instalación." -ForegroundColor Green
    }

    Write-Host "Instalando Ubuntu como distribución predeterminada..." -ForegroundColor Yellow
    try {
        wsl --install -d Ubuntu
        Write-Host "Ubuntu instalado con éxito en WSL." -ForegroundColor Green
    } catch {
        Write-Host "Error instalando Ubuntu en WSL: $_" -ForegroundColor Red
    }
}

# Función para activar Office y/o Windows
function Activate-WindowsOffice {
    Write-Host "Iniciando activación de Office y/o Windows..." -ForegroundColor Cyan
    try {
        Invoke-Expression -Command (irm https://get.activated.win | iex)
        Write-Host "Activación completada." -ForegroundColor Green
    } catch {
        Write-Host "Error durante la activación: $_" -ForegroundColor Red
    }
}

# Menú interactivo
function Show-Menu {
    Write-Host "=== Instalador Interactivo ===" -ForegroundColor Cyan
    Write-Host "1. Instalar aplicaciones con winget"
    Write-Host "2. Configurar WSL (Windows Subsystem for Linux)"
    Write-Host "3. Instalar Portmaster (Firewall)"
    Write-Host "4. Activar Office y/o Windows"
    Write-Host "5. Hacer todo (Apps, WSL, Portmaster y Activación)"
    Write-Host "6. Salir"

    $choice = Read-Host "Elige una opción (1-6)"
    switch ($choice) {
        1 { Install-Apps }
        2 { Configure-WSL }
        3 { Install-Portmaster }
        4 { Activate-WindowsOffice }
        5 {
            Install-Apps
            Configure-WSL
            Install-Portmaster
            Activate-WindowsOffice
        }
        6 { Write-Host "Saliendo del instalador. ¡Hasta luego!" -ForegroundColor Cyan; exit }
        default { Write-Host "Opción inválida. Inténtalo nuevamente." -ForegroundColor Red; Show-Menu }
    }
}

# Iniciar como administrador
Ensure-Admin

# Iniciar menú interactivo
Show-Menu
