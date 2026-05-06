#!/usr/bin/env python3
"""
Script para generar el archivo ejecutable EXE del extractor de imágenes de PDF
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """Instala PyInstaller si no está disponible"""
    try:
        import PyInstaller
        print("PyInstaller ya está instalado")
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller instalado correctamente")

def create_spec_file():
    """Crea el archivo .spec personalizado para PyInstaller"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['pdf_image_extractor.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinterdnd2',
        'tkinterdnd2.tkdnd',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDF Image Extractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    distpath='.',
)
'''
    
    with open('pdf_image_extractor.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("Archivo .spec creado correctamente")

def build_exe():
    """Construye el archivo EXE"""
    print("Iniciando construcción del archivo EXE...")
    
    # Limpiar construcciones anteriores
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Eliminar ejecutable anterior si existe en la carpeta actual
    if os.path.exists('PDF Image Extractor.exe'):
        os.remove('PDF Image Extractor.exe')
    
    # Ejecutar PyInstaller
    try:
        subprocess.check_call([
            sys.executable, 
            '-m', 
            'PyInstaller', 
            '--clean',
            '--noconfirm',
            'pdf_image_extractor.spec'
        ])
        print("¡Construcción completada!")
        print(f"El archivo EXE se encuentra en: {os.path.abspath('PDF Image Extractor.exe')}")
        
        # Verificar si el archivo existe
        exe_path = 'PDF Image Extractor.exe'
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"Tamaño del archivo: {size_mb:.2f} MB")
        else:
            print("Error: No se encontró el archivo EXE generado")
            
    except subprocess.CalledProcessError as e:
        print(f"Error durante la construcción: {e}")
        return False
    
    return True

def main():
    """Función principal"""
    print("=== Generador de EXE para PDF Image Extractor ===\n")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('pdf_image_extractor.py'):
        print("Error: No se encuentra el archivo pdf_image_extractor.py")
        print("Por favor ejecuta este script desde la misma carpeta que el programa")
        return
    
    # Instalar PyInstaller
    install_pyinstaller()
    
    # Crear archivo .spec personalizado
    create_spec_file()
    
    # Construir el EXE
    if build_exe():
        print("\n=== Proceso completado exitosamente ===")
        print("Puedes encontrar el archivo ejecutable en la carpeta 'dist'")
        print("Puedes copiar el archivo EXE a cualquier computadora con Windows")
    else:
        print("\n=== Error durante la construcción ===")
        print("Revisa los mensajes de error arriba para más detalles")

if __name__ == "__main__":
    main()
