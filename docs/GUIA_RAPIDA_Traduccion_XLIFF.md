# 🚀 GUÍA RÁPIDA - Traducir Archivos XLIFF con DeepL

## 📌 ¿Qué hace este script?

Traduce automáticamente archivos XLIFF de WordPress/WPML usando DeepL.

## 🎯 PROCESO PASO A PASO

### PASO 1: Abrir Terminal en la carpeta
```bash
cd /ruta/a/tu/carpeta/XLIFF
```

### PASO 2: Ejecutar script
```bash
python translate_xliff4.py "archivo.xliff"
```

### PASO 3: Subir archivo traducido a WPML

El archivo generado será: `archivo_traducido-EN.xliff` (o BG, etc.)

## ⚡ RESUMEN ULTRA-RÁPIDO
```bash
# 1. Ir a carpeta
cd /ruta/XLIFF

# 2. Traducir
python translate_xliff4.py "archivo.xliff"

# 3. Subir archivo_traducido-XX.xliff a WPML
```

## 🚨 SOLUCIÓN DE PROBLEMAS

### Error: "python no se reconoce"
```bash
python3 translate_xliff4.py "archivo.xliff"
```

### Error: "No such file"
```bash
# Ver archivos disponibles
ls *.xliff

# Copiar nombre exacto
python translate_xliff4.py "nombre-exacto.xliff"
```

### Error: "Invalid API key"
Editar el script y poner tu API key real:
```bash
nano translate_xliff4.py
# Línea 6: API_KEY = "tu-key-real"
```

## 📊 Tiempos Aproximados

- Archivo pequeño (20-50 segmentos): 10-30 segundos
- Archivo mediano (100-200 segmentos): 1-2 minutos
- Archivo grande (500+ segmentos): 5-10 minutos

## 💡 COMANDOS ÚTILES

Ver archivos XLIFF:
```bash
ls *.xliff
```

Traducir múltiples archivos:
```bash
for file in *.xliff; do python translate_xliff4.py "$file"; done
```

Borrar archivos traducidos:
```bash
rm *_traducido-*.xliff
```

## 👤 Autor

Ale Castillo - Identi-ty 360, S.L.  
Castellón, España

---

**Versión:** 1.0  
**Fecha:** Febrero 2026
