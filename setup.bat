@echo off
title Instalador de Convertidor: YouTube a MP3 papi
echo ==========================================
echo  🚀 Instalador de YouTube Downloader  
echo ==========================================
echo.

:: Verifica si Chocolatey está instalado
where choco >nul 2>nul
if %errorlevel% neq 0 (
    echo 🔹 Instalando Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    if %errorlevel% neq 0 (
        echo ❌ Error al instalar Chocolatey. Instálalo manualmente desde https://chocolatey.org/install
        pause
        exit /b
    )
    echo ✅ Chocolatey se ha instalado correctamente.
) else (
    echo ✅ Chocolatey ya está instalado.
)

:: Instalar FFMPEG si no está presente
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo 🔹 Instalando FFMPEG...
    choco install ffmpeg -y
    echo ✅ FFMPEG instalado correctamente.
) else (
    echo ✅ FFMPEG ya está instalado.
)

:: Verificar si Python está instalado
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 🔹 Instalando Python...
    choco install python -y
    echo ✅ Python instalado correctamente.
) else (
    echo ✅ Python ya está instalado.
)

:: Actualizar pip y asegurarse de que `yt-dlp` y `ffmpeg-python` estén instalados
echo 🔹 Instalando dependencias de Python...
python -m pip install --upgrade pip yt-dlp ffmpeg-python

if %errorlevel% neq 0 (
    echo ❌ Hubo un problema instalando las dependencias.
    pause
    exit /b
)
echo ✅ Dependencias instaladas correctamente.

:: Confirmar instalación
echo.
echo ✅ Todo está listo para usar el descargador.
echo 🔹 Para ejecutarlo, usa: python downloader.py 
pause
exit