# 🔄 Guía de Migración: v4.0 → v4.1

## ⚡ Resumen Rápido

**¿Necesitas migrar?** Solo si quieres las mejoras de validación de estructura HTML.

**¿Es compatible?** Sí, 100% compatible hacia atrás.

**¿Rompe algo?** No, solo mejora la detección de traducciones incorrectas.

---

## 📋 Checklist de Migración

```
[ ] Descargar translate_xliff4.py v4.1
[ ] Reemplazar el archivo viejo
[ ] (Opcional) Retraducir archivos con problemas de HTML
[ ] (Opcional) Actualizar documentación interna
```

---

## 🆕 ¿Qué Cambió?

### Antes (v4.0)
```python
# Consideraba "traducido" cualquier target con contenido
if target_text and target_text != source_text:
    skip_translation()  # No retraduce
```

**Problema:** Si el target tenía contenido pero **estructura HTML rota**, no lo retraducía.

### Ahora (v4.1)
```python
# Valida que la estructura HTML sea correcta
if has_valid_translation(source_text, target_text):
    skip_translation()  # Solo si estructura es correcta
```

**Mejora:** Detecta y **retraduce segmentos con HTML incorrecto**.

---

## 🔍 Casos que Ahora se Detectan

### Ejemplo 1: Tag Faltante

**v4.0 (incorrecto):**
```
Source: <p>Precio: 100€<sup>*</sup></p>
Target: <p>Price: 100€</p>  ← Falta <sup>
Acción: NO retraduce (tenía contenido)
```

**v4.1 (correcto):**
```
Source: <p>Precio: 100€<sup>*</sup></p>
Target: <p>Price: 100€</p>  ← Detecta que falta <sup>
Acción: SÍ retraduce
Resultado: <p>Price: 100€<sup>*</sup></p>
```

### Ejemplo 2: Tags Extra

**v4.0 (incorrecto):**
```
Source: <p>Texto</p>
Target: <p><strong>Text</strong></p>  ← Tag extra
Acción: NO retraduce
```

**v4.1 (correcto):**
```
Source: <p>Texto</p>
Target: <p><strong>Text</strong></p>  ← Detecta tag extra
Acción: SÍ retraduce
Resultado: <p>Text</p>
```

---

## 🚀 Instrucciones de Migración

### Paso 1: Backup del Script Actual

```bash
# Guardar copia del script viejo
cp translate_xliff4.py translate_xliff4_v4.0_backup.py
```

### Paso 2: Descargar Nueva Versión

```bash
# Opción A: Descargar desde GitHub
# (actualiza la URL cuando subas el archivo)

# Opción B: Copiar manualmente
# Descarga translate_xliff4.py v4.1 y reemplaza el archivo
```

### Paso 3: Verificar Funcionamiento

```bash
# Ejecutar con un archivo de prueba
python translate_xliff4.py "test-file.xliff"

# Verificar que muestra:
# - Total segmentos
# - Ya traducidos
# - A saltar
# - Normales
```

### Paso 4 (Opcional): Retraducir Archivos Problemáticos

Si tienes archivos `.xliff` traducidos con v4.0 que perdieron HTML:

```bash
# El script detectará automáticamente los problemas
python translate_xliff4.py "archivo-con-problemas.xliff"

# Verificar el resultado
# Buscar: <sup>, <sub>, <strong>, etc. en el archivo traducido
```

---

## 🔧 Cambios en el Código

### Función Eliminada

```python
# v4.0 - YA NO SE USA
def has_translation(target_text):
    target_text = target_text.strip()
    if not target_text:
        return False
    return True
```

### Función Nueva

```python
# v4.1 - NUEVA
def has_valid_translation(source_text, target_text):
    """
    Valida que target tenga:
    1. Contenido
    2. Diferente al source
    3. Misma estructura HTML que source
    """
    # ... (ver código completo en el archivo)
```

---

## ⚠️ Comportamiento Diferente

### Situación 1: Archivos Ya Traducidos

**v4.0:**
- Nunca retraduce segmentos con contenido en target

**v4.1:**
- Retraduce segmentos si detecta estructura HTML incorrecta
- **Resultado:** Algunos segmentos se retradujeron = consume más API calls

### Situación 2: Primera Traducción

**v4.0 y v4.1:**
- Comportamiento idéntico
- Ambos traducen desde cero correctamente

---

## 📊 Impacto en Costes de API

### Primer Uso (archivo nuevo)
```
v4.0: 100 segmentos → 100 traducciones
v4.1: 100 segmentos → 100 traducciones
Diferencia: Ninguna
```

### Re-traducción (archivo existente)
```
v4.0: 100 segmentos (80 ya traducidos) → 20 traducciones
v4.1: 100 segmentos (80 OK, 5 HTML roto) → 25 traducciones
Diferencia: +5 traducciones (solo si había problemas)
```

**Coste adicional:** Solo si había errores de HTML en traducciones antiguas.

---

## 🐛 Problemas Conocidos

### Falsos Positivos

**Muy raro, pero posible:**
```html
Source: <p>Texto con <em>énfasis</em> normal</p>
Target: <p>Text with <strong>emphasis</strong> normal</p>
```

Si un traductor humano cambió `<em>` por `<strong>` intencionalmente, v4.1 lo detectará como "inválido" y lo retradujera.

**Solución:** Revisar manualmente después de traducir.

---

## ✅ Testing Post-Migración

### Test 1: Estructura HTML Correcta
```bash
# Traducir archivo con HTML complejo
python translate_xliff4.py "archivo-con-html.xliff"

# Verificar manualmente:
# 1. Abrir archivo traducido
# 2. Buscar: <sup>, <sub>, <strong>, <span>
# 3. Confirmar que todos los tags están presentes
```

### Test 2: Vocabulario Schema.org
```bash
# Verificar que no se traducen términos técnicos
grep -i "PropertyValue\|GeoCoordinates\|custom" archivo_traducido.xliff

# Resultado esperado:
# PropertyValue → PropertyValue (sin traducir)
# custom → custom (sin traducir)
```

### Test 3: Códigos de Idioma
```bash
# Verificar códigos ISO
grep -E '"es"|"en"|"bg"' archivo_traducido.xliff

# Resultado esperado:
# "es" → "es" (sin traducir)
# "bg" → "bg" (sin traducir)
```

---

## 📞 Soporte

**Si encuentras problemas:**

1. Verifica que usas v4.1 correctamente:
   ```bash
   grep -n "def has_valid_translation" translate_xliff4.py
   # Debe mostrar la línea donde está la función
   ```

2. Compara con el archivo de backup:
   ```bash
   diff translate_xliff4_v4.0_backup.py translate_xliff4.py
   ```

3. Revisa el CHANGELOG.md para entender los cambios

---

## 🎯 Rollback (Volver a v4.0)

Si necesitas volver atrás:

```bash
# Restaurar backup
cp translate_xliff4_v4.0_backup.py translate_xliff4.py

# Verificar
python translate_xliff4.py --help
```

**Nota:** Perderás la validación de estructura HTML.

---

## 📅 Fecha de Esta Guía

**Versión:** 1.0  
**Fecha:** 20 de Febrero de 2026  
**Autor:** Ale Castillo - Identi-ty 360, S.L.
