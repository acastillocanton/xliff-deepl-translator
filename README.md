# 🌍 XLIFF DeepL Translator

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![DeepL](https://img.shields.io/badge/DeepL-API-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Script automatizado en Python para traducir archivos XLIFF de WordPress/WPML usando la API de DeepL.

## ✨ Características

- ✅ Detección automática de idiomas
- ✅ Respeta shortcodes de WordPress/Divi  
- ✅ Preserva HTML sin romper estructura
- ✅ Mantiene traducciones manuales existentes
- ✅ Maneja textos largos (hasta 250KB)
- ✅ Procesamiento por lotes optimizado

## 🚀 Uso Rápido

\`\`\`bash
python translate_xliff4.py "archivo.xliff"
\`\`\`

## 📚 Documentación

- [Guía Rápida](docs/GUIA_RAPIDA_Traduccion_XLIFF.md)
- [Documentación Técnica](docs/Documentacion_Script_Traduccion_XLIFF.md)

## 🔧 Requisitos

- Python 3.7+
- \`pip install requests\`
- API Key de DeepL

## ⚙️ Configuración

1. Editar \`translate_xliff4.py\` línea 6:
\`\`\`python
API_KEY = "tu-api-key-aqui"
\`\`\`

2. Ejecutar:
\`\`\`bash
python translate_xliff4.py "archivo.xliff"
\`\`\`

## 👤 Autor

Ale Castillo - Identi-ty 360, S.L.  
GitHub: [@acastillocanton](https://github.com/acastillocanton)

## 📝 Licencia

MIT License
