# Changelog

Historial de cambios del script de traducción XLIFF con DeepL.

---

## [4.1.0] - 2026-02-20

### 🎯 Cambio Mayor: Validación Inteligente de Traducciones

**PROBLEMA DETECTADO:**
El script consideraba "traducido" cualquier segmento con contenido en `<target>`, incluso si la estructura HTML era incorrecta o incompleta. Esto causaba que:
- Tags HTML desaparecieran (`<sup>`, `<sub>`, etc.)
- Traducciones con estructura rota no se corrigieran
- Contenido parcialmente traducido no se retradujera

**SOLUCIÓN IMPLEMENTADA:**
Nueva función `has_valid_translation()` que valida la traducción comparando la **estructura HTML** del source y target:

```python
# ANTES (v4.0)
if target_text and target_text != source_text:
    # Considera traducido → NO retraduce

# AHORA (v4.1)
if has_valid_translation(source_text, target_text):
    # Valida estructura HTML → Solo retraduce si está rota
```

### ✅ Lo Que Valida Ahora

1. **Cantidad de tags HTML** (source vs target)
2. **Tipo de tags** (`<sup>` en source debe estar en target)
3. **Estructura completa** (tags de apertura y cierre)
4. **Normalización** (ignora atributos, solo valida estructura)

### 📊 Ejemplos de Casos Detectados

**Caso 1: Tag faltante (RETRADUCE)**
```html
Source: <p>Precio: 247.947 €<sup class="nota">*</sup></p>
Target: <p>Цена: 247 947 €</p>  ❌ Falta <sup>
→ Resultado: RETRADUCE y añade el <sup>
```

**Caso 2: Estructura correcta (NO RETRADUCE)**
```html
Source: <p>Precio: 247.947 €<sup class="nota">*</sup></p>
Target: <p>Цена: 247 947 €<sup class="nota">*</sup></p>  ✓ Completo
→ Resultado: Mantiene traducción existente
```

**Caso 3: Atributos diferentes (NO RETRADUCE)**
```html
Source: <span class="price">100€</span>
Target: <span class="precio">100€</span>  ✓ Estructura OK
→ Resultado: Acepta (ignora atributos)
```

### 🚀 Mejoras Adicionales

- **Protección completa vocabulario Schema.org** (~450 términos)
- **Códigos ISO de idiomas** (cortos y largos: `es`, `es-ES`, `bg-BG`, etc.)
- **Término `custom`** de Rank Math protegido
- **Optimización de rendimiento** en validación de tags

### 🔧 Cambios Técnicos

**Archivo modificado:**
- `translate_xliff4.py`

**Funciones nuevas:**
- `has_valid_translation(source_text, target_text)` - Valida estructura HTML

**Funciones modificadas:**
- `process_xliff()` - Usa nueva validación en lugar de `has_translation()`

**Funciones eliminadas:**
- `has_translation()` - Reemplazada por `has_valid_translation()`

### 📈 Impacto

**Rendimiento:**
- Sin impacto significativo (validación muy rápida)
- Mismo número de llamadas a la API de DeepL

**Compatibilidad:**
- ✅ Compatible con archivos XLIFF anteriores
- ✅ No requiere cambios en uso del script
- ✅ Detecta y corrige traducciones antiguas con errores

### 🐛 Bugs Corregidos

- **#1**: Tags `<sup>` y `<sub>` desaparecían en traducciones
- **#2**: Estructura HTML se perdía en segmentos complejos
- **#3**: Traducciones parciales no se detectaban como inválidas

---

## [4.0.0] - 2026-02-06

### ✨ Características Iniciales

- Detección automática de idiomas
- Filtros inteligentes para shortcodes, URLs, códigos
- División automática de textos largos (hasta 250KB)
- Preservación de HTML con `tag_handling: 'html'`
- Mantenimiento de traducciones manuales existentes
- Procesamiento optimizado por lotes (50 textos/llamada)

### 📦 Componentes

- Script principal: `translate_xliff4.py`
- Documentación técnica completa
- Guía rápida de uso
- Licencia MIT

---

## Formato del Changelog

Este changelog sigue el formato [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

### Tipos de Cambios
- `Added` → Nuevas características
- `Changed` → Cambios en funcionalidad existente
- `Deprecated` → Características que serán eliminadas
- `Removed` → Características eliminadas
- `Fixed` → Bugs corregidos
- `Security` → Vulnerabilidades corregidas
