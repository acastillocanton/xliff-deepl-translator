import re
import sys
import requests
import time

API_KEY = "TU_API_KEY_AQUI"

def should_skip_translation(text):
    text = text.strip()
    if re.match(r'^\[[\w_-]+\s', text) or re.match(r'^\[[\w_-]+\]$', text):
        return True
    if re.match(r'^(\[[\w_-]+[^\]]*\])+$', text.replace('\n', '').replace('\r', '')):
        return True
    if re.match(r'^https?://[^\s]+$', text):
        return True
    if re.match(r'^/[\w\-/\.]+$', text):
        return True
    schema_values = ['custom', 'FAQPage', 'WebPage', 'Question', 'Answer', 'es-ES', 'bg-BG', 'en-US']
    if text in schema_values:
        return True
    if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', text):
        return True
    if re.match(r'^https?://[^\s]+#[\w-]+$', text):
        return True
    page_sizes = ['A3', 'A4', 'A5', 'B3', 'B4', 'B4-S', 'B5', 'Letter', 'Legal', 'Tabloid', 'Ledger']
    if text in page_sizes:
        return True
    if re.match(r'^[A-Z][a-z]+(-[A-Z][a-z]+)*$', text) and len(text) < 20:
        return True
    if re.match(r'^[A-Z0-9]{1,3}(-[A-Z0-9]{1,3})?$', text):
        return True
    if re.match(r'^[A-Z][a-z]+(\s[a-z]+){2,5}$', text) and '.' not in text and ',' not in text:
        return True
    return False

def extract_languages(content):
    source_match = re.search(r'source-language=["\']([a-zA-Z]{2}(?:-[a-zA-Z]{2})?)["\']', content)
    source_lang = source_match.group(1).upper() if source_match else "ES"
    target_match = re.search(r'target-language=["\']([a-zA-Z]{2}(?:-[a-zA-Z]{2})?)["\']', content)
    target_lang = target_match.group(1).upper() if target_match else "BG"
    return source_lang, target_lang

def normalize_deepl_lang(lang_code):
    if '-' not in lang_code:
        return lang_code
    deepl_variants = {'EN-US': 'EN-US', 'EN-GB': 'EN-GB', 'PT-BR': 'PT-BR', 'PT-PT': 'PT-PT', 'ES-ES': 'ES', 'BG-BG': 'BG'}
    return deepl_variants.get(lang_code, lang_code.split('-')[0])

def is_html_content(text):
    html_tags = r'<(div|table|tr|td|th|p|span|a|img|ul|li|h[1-6])[>\s]'
    return bool(re.search(html_tags, text, re.IGNORECASE))

def split_long_text(text, max_length=1500):
    if len(text) <= max_length:
        return [text]
    if is_html_content(text):
        if len(text) <= 10000:
            return [text]
        safe_split_pattern = r'(</(?:div|table|section|article|p)>\s*<(?:div|table|section|article|p)[^>]*>)'
        parts = re.split(safe_split_pattern, text)
        chunks = []
        current = ""
        for part in parts:
            if len(current) + len(part) > 8000 and current:
                chunks.append(current)
                current = part
            else:
                current += part
        if current:
            chunks.append(current)
        return chunks if chunks else [text]
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_length = 0
    for para in paragraphs:
        para_length = len(para)
        if para_length > max_length:
            sentences = re.split(r'(?<=[.!?])\s+', para)
            for sent in sentences:
                if current_length + len(sent) > max_length and current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                    current_chunk = []
                    current_length = 0
                current_chunk.append(sent)
                current_length += len(sent)
        else:
            if current_length + para_length > max_length and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = []
                current_length = 0
            current_chunk.append(para)
            current_length += para_length
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    return chunks

def translate_text(texts, source_lang, target_lang):
    response = requests.post("https://api.deepl.com/v2/translate", data={'auth_key': API_KEY, 'text': texts, 'source_lang': source_lang, 'target_lang': target_lang, 'tag_handling': 'html', 'preserve_formatting': '1'})
    if response.status_code == 200:
        return [t['text'] for t in response.json()['translations']]
    print(f"Error DeepL: {response.text}")
    return None

def translate_single_text(text, source_lang, target_lang):
    length_threshold = 10000 if is_html_content(text) else 2000
    if len(text) > length_threshold:
        print(f"      Texto largo ({len(text)} chars), dividiendo...", end=" ")
        chunks = split_long_text(text, max_length=8000 if is_html_content(text) else 1500)
        print(f"{len(chunks)} partes")
        translated_chunks = []
        for i, chunk in enumerate(chunks):
            print(f"         Parte {i+1}/{len(chunks)}...", end=" ", flush=True)
            result = translate_text([chunk], source_lang, target_lang)
            if result:
                translated_chunks.append(result[0])
                print("OK")
            else:
                print("ERROR")
                return None
            time.sleep(0.3)
        separator = '' if is_html_content(text) else '\n\n'
        return separator.join(translated_chunks)
    else:
        result = translate_text([text], source_lang, target_lang)
        return result[0] if result else None

def has_translation(target_text):
    target_text = target_text.strip()
    if not target_text:
        return False
    if target_text in ['', ' ', '\n', '\r\n']:
        return False
    return True

def process_xliff(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    source_lang_raw, target_lang_raw = extract_languages(content)
    source_lang_deepl = normalize_deepl_lang(source_lang_raw)
    target_lang_deepl = normalize_deepl_lang(target_lang_raw)
    print(f"\nArchivo: {input_file}")
    print(f"Traduccion: {source_lang_raw} -> {target_lang_raw}")
    print(f"DeepL: {source_lang_deepl} -> {target_lang_deepl}\n")
    pattern = r'<source>(?:<!\[CDATA\[)?(.*?)(?:]]>)?</source>\s*<target[^>]*>(?:<!\[CDATA\[)?(.*?)(?:]]>)?</target>'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    sources = []
    targets = []
    skip_indices = []
    already_translated_indices = []
    long_text_indices = []
    for i, m in enumerate(matches):
        src_text = m.group(1).strip()
        target_text = m.group(2).strip()
        sources.append(src_text)
        targets.append(target_text)
        if has_translation(target_text) and target_text != src_text:
            already_translated_indices.append(i)
        elif should_skip_translation(src_text):
            skip_indices.append(i)
        elif len(src_text) > 1500:
            long_text_indices.append(i)
    print(f"Total segmentos: {len(sources)}")
    print(f"Ya traducidos: {len(already_translated_indices)}")
    print(f"A saltar: {len(skip_indices)}")
    print(f"Largos: {len(long_text_indices)}")
    total_to_skip = len(skip_indices) + len(already_translated_indices) + len(long_text_indices)
    print(f"Normales: {len(sources) - total_to_skip}\n")
    normal_to_translate = [(i, sources[i]) for i in range(len(sources)) if i not in skip_indices and i not in already_translated_indices and i not in long_text_indices]
    translations = {}
    for i in already_translated_indices:
        translations[i] = targets[i]
    if normal_to_translate:
        print("Traduciendo textos normales:")
        batch_size = 50
        texts_only = [t[1] for t in normal_to_translate]
        indices_only = [t[0] for t in normal_to_translate]
        for i in range(0, len(texts_only), batch_size):
            batch_texts = texts_only[i:i+batch_size]
            batch_indices = indices_only[i:i+batch_size]
            print(f"  Lote {i//batch_size + 1}/{(len(texts_only)-1)//batch_size + 1}...", end=" ", flush=True)
            result = translate_text(batch_texts, source_lang_deepl, target_lang_deepl)
            if result:
                for idx, trans in zip(batch_indices, result):
                    translations[idx] = trans
                print("OK")
            else:
                print("ERROR")
                return
            time.sleep(0.5)
    if long_text_indices:
        print(f"\nTraduciendo {len(long_text_indices)} textos largos:")
        for idx in long_text_indices:
            text = sources[idx]
            print(f"  Segmento {idx+1} ({len(text)} chars)...", end=" ", flush=True)
            trans = translate_single_text(text, source_lang_deepl, target_lang_deepl)
            if trans:
                translations[idx] = trans
                print("OK")
            else:
                print("ERROR")
                return
            time.sleep(0.5)
    for i in skip_indices:
        translations[i] = sources[i]
    result = content
    offset = 0
    for i, m in enumerate(matches):
        trans = translations.get(i, sources[i])
        original_match = m.group(0)
        has_cdata = '<![CDATA[' in original_match
        if has_cdata:
            new_match = f'<source><![CDATA[{sources[i]}]]></source>\n    <target><![CDATA[{trans}]]></target>'
        else:
            new_match = f'<source>{sources[i]}</source>\n    <target>{trans}</target>'
        start = m.start() + offset
        end = m.end() + offset
        result = result[:start] + new_match + result[end:]
        offset += len(new_match) - len(original_match)
    output_file = input_file.replace('.xliff', f'_traducido-{target_lang_raw}.xliff')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"\nGuardado: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python translate_xliff4.py archivo.xliff")
        sys.exit(1)
    process_xliff(sys.argv[1])
ENDOFPYTHON