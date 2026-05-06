@echo off
echo === Generador de EXE para PDF Image Extractor ===
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error al instalar las dependencias
    pause
    exit /b 1
)

REM Ejecutar script de construcción
echo.
echo Iniciando construcción del EXE...
python build_exe.py

echo.
echo Proceso finalizado. Presiona cualquier tecla para salir.
pause >nul
