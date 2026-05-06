@echo off
echo === Instalación con compatibilidad mejorada ===
echo.

REM Actualizar pip primero
echo Actualizando pip...
python -m pip install --upgrade pip

REM Instalar paquetes individualmente con versiones compatibles
echo.
echo Instalando PyMuPDF...
python -m pip install PyMuPDF --no-cache-dir

echo.
echo Instalando Pillow...
python -m pip install Pillow --no-cache-dir

echo.
echo Instalando tkinterdnd2...
python -m pip install tkinterdnd2 --no-cache-dir

echo.
echo Instalando PyInstaller...
python -m pip install pyinstaller --no-cache-dir

echo.
echo Verificando instalación...
python -c "import fitz; print('PyMuPDF: OK')"
python -c "import PIL; print('Pillow: OK')"
python -c "import tkinterdnd2; print('tkinterdnd2: OK')"
python -c "import PyInstaller; print('PyInstaller: OK')"

echo.
echo Instalación completada. Ahora puedes ejecutar el script de construcción.
pause
