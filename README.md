# 🌍 XLIFF DeepL Translator

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![DeepL](https://img.shields.io/badge/DeepL-API-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/version-4.1.0-brightgreen.svg)

Script automatizado en Python para traducir archivos XLIFF de WordPress/WPML usando la API de DeepL.

## ✨ Características

- ✅ **Validación inteligente de traducciones** (NUEVO v4.1)
- ✅ Detección automática de idiomas
- ✅ Respeta shortcodes de WordPress/Divi  
- ✅ Preserva HTML sin romper estructura
- ✅ Detecta y corrige traducciones con HTML incorrecto
- ✅ Mantiene traducciones manuales válidas
- ✅ Protege vocabulario Schema.org completo (~450 términos)
- ✅ Maneja textos largos (hasta 250KB)
- ✅ Procesamiento por lotes optimizado

## 🆕 Novedades v4.1

### Validación Inteligente de Estructura HTML

El script ahora **detecta automáticamente** traducciones con estructura HTML incorrecta:

```html
<!-- ❌ ANTES: No se detectaba -->
Source: <p>Precio: 100€<sup>*</sup></p>
Target: <p>Price: 100€</p>  <!-- Falta <sup> -->
→ No se retraducía

<!-- ✅ AHORA: Se detecta y corrige -->
Source: <p>Precio: 100€<sup>*</sup></p>
Target: <p>Price: 100€</p>  <!-- Detecta falta de <sup> -->
→ Se retraduce automáticamente
→ Resultado: <p>Price: 100€<sup>*</sup></p>
```

**Casos que detecta:**
- Tags HTML faltantes (`<sup>`, `<sub>`, `<strong>`, etc.)
- Tags HTML extra que no están en el source
- Cambio de tipo de tag (`<p>` → `<div>`)
- Estructura HTML incompleta o rota

**Ver:** [CHANGELOG.md](CHANGELOG.md) para detalles técnicos completos

## 🚀 Uso Rápido

```bash
python translate_xliff4.py "archivo.xliff"
```

## 📚 Documentación

- **[Guía Rápida](GUIA_RAPIDA_Traduccion_XLIFF.md)** - Comandos básicos
- **[Documentación Técnica](Documentacion_Script_Traduccion_XLIFF.md)** - Arquitectura y detalles
- **[CHANGELOG](CHANGELOG.md)** - Historial de cambios (NUEVO)
- **[Guía de Migración](MIGRATION_GUIDE.md)** - Actualizar de v4.0 a v4.1 (NUEVO)

## 🔧 Requisitos

- Python 3.7+
- `pip install requests`
- API Key de DeepL

## ⚙️ Configuración

1. Editar `translate_xliff4.py` línea 6:
```python
API_KEY = "tu-api-key-aqui"
```

2. Ejecutar:
```bash
python translate_xliff4.py "archivo.xliff"
```

## 📊 Ejemplo de Salida

```
Archivo: Marina_d_Or_Construcciones-translation-job-2159.xliff
Traduccion: ES -> BG
DeepL: ES -> BG

Total segmentos: 505
Ya traducidos: 163  ← Validados con estructura HTML correcta
A saltar: 235       ← Códigos, URLs, Schema.org
Largos: 0
Normales: 107       ← Incluye retraducción de HTML incorrecto

Traduciendo textos normales:
  Lote 1/3... OK
  Lote 2/3... OK
  Lote 3/3... OK

Guardado: Marina_d_Or_Construcciones-translation-job-2159_traducido-BG.xliff
```

## 🛡️ Protección Automática

### Vocabulario Schema.org (~450 términos)

**Tipos protegidos:**
`Thing`, `Organization`, `LocalBusiness`, `RealEstateAgent`, `PropertyValue`, `GeoCoordinates`, `PostalAddress`, `OpeningHoursSpecification`, `FAQPage`, `Question`, `Answer`, `ImageObject`, `WebPage`, `BreadcrumbList`, `ApartmentComplex`, etc.

**Propiedades protegidas:**
`name`, `alternateName`, `description`, `image`, `url`, `address`, `streetAddress`, `addressLocality`, `addressRegion`, `postalCode`, `telephone`, `email`, `latitude`, `longitude`, `openingHours`, `aggregateRating`, `ratingValue`, etc.

### Códigos ISO de Idiomas

**Formato corto:** `es`, `en`, `bg`, `de`, `fr`, `it`, `pt`, `nl`, `pl`, `ru`, `ja`, `zh`, `ar`, `ca`, `eu`, `gl`, etc. (~180 idiomas)

**Formato largo:** `es-ES`, `es-MX`, `en-US`, `en-GB`, `bg-BG`, `pt-PT`, `pt-BR`, `ca-ES`, `eu-ES`, etc. (~120 variantes)

### Valores Técnicos

**Rank Math:** `custom`

**Estados:** `True`, `False`, `InStock`, `OutOfStock`, `NewCondition`, `Male`, `Female`, etc.

**Días:** `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`, `Sunday`

## 🎯 Casos de Uso

### Caso 1: Primera Traducción
```bash
python translate_xliff4.py "nuevo-archivo.xliff"
# Traduce todo el contenido desde cero
```

### Caso 2: Actualizar Traducción Existente
```bash
python translate_xliff4.py "archivo-ya-traducido.xliff"
# Solo retraduce segmentos con:
# - Target vacío
# - Estructura HTML incorrecta (NUEVO v4.1)
# Mantiene traducciones válidas existentes
```

### Caso 3: Corregir Traducciones con HTML Roto
```bash
python translate_xliff4.py "archivo-con-problemas-html.xliff"
# Detecta automáticamente tags faltantes
# Retraduce solo los segmentos problemáticos
```

## 🔍 Validación de Traducciones

La versión 4.1 incluye validación inteligente que compara la **estructura HTML** del source y target:

```python
# Validación automática
Source: <p>Texto con <sup>nota</sup></p>
Target: <p>Text with <sup>note</sup></p>
→ ✅ Válida (estructura idéntica)

Source: <p>Texto con <sup>nota</sup></p>
Target: <p>Text with nota</p>
→ ❌ Inválida (falta <sup>) → Se retraduce
```

**Ver:** [Documentación Técnica](Documentacion_Script_Traduccion_XLIFF.md) para detalles de la validación

## 🐛 Solución de Problemas

### Error: "Payload too large"
**Solución:** El script divide automáticamente. Si persiste, reducir límite en línea 340.

### Error: "Invalid target language"
**Solución:** Revisar mapeo en `normalize_deepl_lang()` y añadir idioma.

### HTML roto después de traducir
**Solución:** Actualizar a v4.1. Incluye validación automática de estructura HTML.

### Tags desaparecen en traducción
**Solución:** Actualizar a v4.1. El script ahora detecta y retraduce automáticamente.

## 📈 Rendimiento

**Consumo API (archivo típico de 500 segmentos):**
- Segmentos normales: ~10 llamadas (50 textos/llamada)
- Segmentos largos: ~50 llamadas (1 texto/llamada)
- **Total:** ~60 llamadas
- **Tiempo:** ~35 segundos
- **Coste:** ~0.30€

**Límites:**
- Máximo por archivo: 2000 segmentos (recomendado)
- Máximo por segmento: 50,000 caracteres
- Rate limit: 100 llamadas/minuto

## 📝 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para historial completo de cambios.

**Última versión:** 4.1.0 (2026-02-20)
- Validación inteligente de estructura HTML
- Detección automática de traducciones incorrectas
- Protección completa de vocabulario Schema.org
- Códigos ISO de idiomas (cortos y largos)

## 🔄 Migración

¿Vienes de v4.0? Ver [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) para instrucciones completas.

**Resumen:** Compatible 100% hacia atrás. Solo descarga y reemplaza el archivo.

## 👤 Autor

**Ale Castillo**  
SEO Consultant & Web Developer  
Identi-ty 360, S.L. - Castellón, España

**Contacto:**
- GitHub: [@acastillocanton](https://github.com/acastillocanton)
- Web: castillocanton.com

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles completos

---

**Versión:** 4.1.0  
**Fecha:** 20/02/2026
