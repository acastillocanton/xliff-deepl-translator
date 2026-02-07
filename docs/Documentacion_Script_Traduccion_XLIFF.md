# Documentación Técnica - Script de Traducción XLIFF

## 📋 Resumen Ejecutivo

Script automatizado para traducir archivos XLIFF de WordPress/WPML usando la API de DeepL.

**Características principales:**
- Detección automática de idiomas fuente y objetivo
- Filtros inteligentes para shortcodes, URLs, códigos
- División automática de textos largos (hasta 250KB)
- Preservación de HTML sin romper estructura
- Mantenimiento de traducciones manuales existentes
- Procesamiento optimizado por lotes (50 textos/llamada)

## 🏗️ Arquitectura

### Funciones Principales

**should_skip_translation(text)**
- Filtra elementos no traducibles
- Detecta: shortcodes, URLs, códigos de tamaño, nombres de fuentes
- Retorna: True/False

**extract_languages(content)**
- Lee idiomas del header XLIFF
- Extrae: source-language y target-language
- Retorna: (source_lang, target_lang)

**translate_text(texts, source_lang, target_lang)**
- Llamada batch a DeepL API
- Traduce hasta 50 textos simultáneamente
- Retorna: lista de traducciones

**split_long_text(text)**
- Divide textos largos inteligentemente
- Para HTML: divide entre bloques completos
- Para texto: divide por párrafos y frases

**process_xliff(input_file)**
- Función principal que orquesta todo
- Clasifica segmentos (ya traducidos, a saltar, largos, normales)
- Traduce en 3 fases y reconstruye XLIFF

## 🎯 Flujo de Ejecución

1. Leer archivo XLIFF
2. Extraer idiomas (ES → EN)
3. Parsear segmentos <source> y <target>
4. Clasificar segmentos
5. Traducir en lotes (normales)
6. Traducir individualmente (largos)
7. Copiar sin traducir (códigos/URLs)
8. Reconstruir XML preservando CDATA
9. Guardar archivo_traducido-XX.xliff

## 🔧 Casos Edge Resueltos

### Textos con CDATA
Preserva correctamente `<![CDATA[...]]>` en source y target

### HTML enorme (250KB)
Divide automáticamente en chunks de 8KB respetando estructura

### Traducciones manuales
Detecta y mantiene traducciones existentes

### Códigos de tamaño
No traduce: B3, B4-S, A4, Letter, etc.

### Nombres de fuentes
No traduce: Avant, Helvetica, etc.

### Shortcodes WordPress
No traduce: [et_pb_section], [contact-form-7], etc.

## 📊 Rendimiento

**Consumo API:**
- 500 segmentos normales → ~10 llamadas
- 50 segmentos largos → 50 llamadas
- Total: ~60 llamadas
- Tiempo: ~35 segundos
- Coste: ~0.30€

**Límites:**
- Máximo por archivo: 2000 segmentos
- Máximo por segmento: 50,000 caracteres
- Rate limit: 100 llamadas/minuto

## 🔐 Seguridad

**API Key:**
- No incluir en repositorios públicos
- Usar variables de entorno en producción
- El .gitignore está configurado para proteger archivos

**Archivos de clientes:**
- Los .xliff no se suben a GitHub
- Configurado en .gitignore

## 🚨 Troubleshooting

### Error: "Payload too large"
**Solución:** El script divide automáticamente. Si persiste, reducir límite en línea 140.

### Error: "Invalid target language"
**Solución:** Revisar mapeo en `normalize_deepl_lang()` y añadir idioma.

### HTML roto
**Solución:** Añadir tag a lista segura en `split_long_text()` línea 154.

### Script lento
**Optimización:** Aumentar límites o reducir sleep entre llamadas.

## 📝 Changelog

**v4.0 (2026-02-06)**
- Detección automática de idiomas
- Filtros completos
- División inteligente HTML
- Preservación traducciones manuales
- Manejo textos mega-largos

## 👤 Autor

Ale Castillo  
SEO Consultant & Web Developer  
Identi-ty 360, S.L. - Castellón, España

**Contacto:**
- GitHub: @acastillocanton
- Web: castillocanton.com

---

**Versión:** 4.0  
**Fecha:** 06/02/2026
