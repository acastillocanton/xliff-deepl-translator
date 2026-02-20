import re
import sys
import requests
import time

API_KEY = "08a7d7e6-cd34-43cf-aafe-9e58416e2f0c"

# Vocabulario completo de Schema.org - NO traducir
SCHEMA_VOCABULARY = {
    # Tipos de Schema más comunes
    'Thing', 'Action', 'CreativeWork', 'Event', 'Intangible', 'Organization', 'Person', 'Place', 'Product',
    'WebPage', 'WebSite', 'Article', 'BlogPosting', 'NewsArticle', 'TechArticle', 'Report', 'ScholarlyArticle',
    'FAQPage', 'QAPage', 'Question', 'Answer', 'ItemPage', 'ContactPage', 'AboutPage', 'CheckoutPage',
    'CollectionPage', 'ProfilePage', 'SearchResultsPage', 'MediaObject', 'ImageObject', 'VideoObject',
    'AudioObject', 'DataDownload', 'SoftwareApplication', 'MobileApplication', 'WebApplication',
    'Game', 'VideoGame', 'Recipe', 'HowTo', 'HowToStep', 'HowToDirection', 'HowToTip', 'HowToSupply',
    'HowToTool', 'Review', 'AggregateRating', 'Rating', 'Offer', 'AggregateOffer', 'Demand',
    'PriceSpecification', 'UnitPriceSpecification', 'DeliveryEvent', 'BreadcrumbList', 'ListItem',
    'ItemList', 'LocalBusiness', 'Store', 'Restaurant', 'FoodEstablishment', 'Hotel', 'LodgingBusiness',
    'AutoDealer', 'AutomotiveBusiness', 'ChildCare', 'Dentist', 'DryCleaningOrLaundry',
    'EmergencyService', 'EmploymentAgency', 'EntertainmentBusiness', 'FinancialService',
    'HealthAndBeautyBusiness', 'HomeAndConstructionBusiness', 'LegalService', 'Library',
    'MedicalOrganization', 'ProfessionalService', 'RadioStation', 'RealEstateAgent', 'RecyclingCenter',
    'SelfStorage', 'ShoppingCenter', 'SportsActivityLocation', 'TouristInformationCenter',
    'TravelAgency', 'Corporation', 'EducationalOrganization', 'GovernmentOrganization',
    'LocalBusiness', 'NGO', 'PerformingGroup', 'SportsOrganization', 'SportsTeam',
    'PropertyValue', 'QuantitativeValue', 'StructuredValue', 'ContactPoint', 'PostalAddress',
    'GeoCoordinates', 'GeoShape', 'OpeningHoursSpecification', 'Photograph', 'ImageGallery',
    'VideoGallery', 'Comment', 'Message', 'EmailMessage', 'BroadcastEvent', 'OnDemandEvent',
    'PublicationEvent', 'SaleEvent', 'ScreeningEvent', 'SocialEvent', 'UserInteraction',
    'Duration', 'Distance', 'Energy', 'Mass', 'QuantitativeValueDistribution', 'MonetaryAmount',
    'Course', 'CourseInstance', 'EducationalOccupationalCredential', 'JobPosting', 'Occupation',
    'MedicalEntity', 'AnatomicalStructure', 'MedicalCondition', 'Drug', 'MedicalTest',
    'MedicalProcedure', 'MedicalStudy', 'Vehicle', 'Car', 'Motorcycle', 'BusOrCoach',
    'ApartmentComplex', 'Apartment', 'House', 'SingleFamilyResidence', 'Residence',
    'WebSite', 'SearchAction',
    
    # Propiedades Schema.org más usadas
    'name', 'alternateName', 'description', 'image', 'url', 'sameAs', 'mainEntityOfPage',
    'potentialAction', 'identifier', 'subjectOf', 'about', 'abstract', 'author', 'creator',
    'contributor', 'copyrightHolder', 'copyrightYear', 'dateCreated', 'dateModified',
    'datePublished', 'editor', 'headline', 'inLanguage', 'keywords', 'publisher', 'version',
    'aggregateRating', 'review', 'itemReviewed', 'ratingValue', 'bestRating', 'worstRating',
    'ratingCount', 'reviewCount', 'reviewRating', 'reviewBody', 'reviewAspect', 'positiveNotes',
    'negativeNotes', 'itemCondition', 'brand', 'manufacturer', 'model', 'productID', 'sku',
    'gtin', 'gtin8', 'gtin12', 'gtin13', 'gtin14', 'mpn', 'offers', 'price', 'priceCurrency',
    'priceValidUntil', 'availability', 'itemOffered', 'seller', 'validFrom', 'validThrough',
    'address', 'streetAddress', 'addressLocality', 'addressRegion', 'postalCode', 'addressCountry',
    'postOfficeBoxNumber', 'telephone', 'email', 'faxNumber', 'contactPoint', 'contactType',
    'areaServed', 'availableLanguage', 'hoursAvailable', 'openingHours', 'dayOfWeek',
    'opens', 'closes', 'geo', 'latitude', 'longitude', 'elevation', 'box', 'circle', 'line',
    'polygon', 'location', 'founder', 'foundingDate', 'foundingLocation', 'dissolutionDate',
    'employee', 'member', 'memberOf', 'numberOfEmployees', 'knowsAbout', 'knowsLanguage',
    'makesOffer', 'seeks', 'owns', 'alumni', 'award', 'sponsor', 'funder', 'parentOrganization',
    'subOrganization', 'department', 'logo', 'slogan', 'tagline', 'taxID', 'vatID', 'duns',
    'legalName', 'naics', 'globalLocationNumber', 'isicV4', 'keywords', 'jobTitle',
    'worksFor', 'affiliation', 'alumniOf', 'birthDate', 'birthPlace', 'deathDate', 'deathPlace',
    'familyName', 'givenName', 'additionalName', 'honorificPrefix', 'honorificSuffix',
    'gender', 'nationality', 'colleague', 'follows', 'relatedTo', 'sibling', 'parent', 'children',
    'spouse', 'performerIn', 'award', 'height', 'weight', 'hasOccupation', 'workLocation',
    'startDate', 'endDate', 'doorTime', 'duration', 'eventAttendanceMode', 'eventStatus',
    'organizer', 'performer', 'previousStartDate', 'recordedIn', 'remainingAttendeeCapacity',
    'superEvent', 'subEvent', 'typicalAgeRange', 'workFeatured', 'workPerformed',
    'acceptedAnswer', 'answerCount', 'downvoteCount', 'upvoteCount', 'suggestedAnswer',
    'text', 'dateCreated', 'parentItem', 'comment', 'commentCount', 'discussionUrl',
    'sharedContent', 'position', 'item', 'itemListElement', 'itemListOrder', 'numberOfItems',
    'mainEntity', 'mentions', 'citation', 'exampleOfWork', 'hasPart', 'isPartOf',
    'provider', 'audience', 'educationalLevel', 'learningResourceType', 'teaches',
    'assesses', 'competencyRequired', 'educationalAlignment', 'educationalUse',
    'timeRequired', 'typicalAgeRange', 'interactivityType', 'isAccessibleForFree',
    'encodingFormat', 'contentUrl', 'embedUrl', 'uploadDate', 'thumbnail', 'width', 'height',
    'caption', 'transcript', 'videoFrameSize', 'videoQuality', 'bitrate', 'contentSize',
    'encodesCreativeWork', 'playerType', 'productionCompany', 'regionsAllowed',
    
    # Estados y valores especiales
    'True', 'False', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
    'InStock', 'OutOfStock', 'PreOrder', 'SoldOut', 'LimitedAvailability', 'OnlineOnly',
    'InStoreOnly', 'Discontinued', 'BackOrder', 'Male', 'Female', 'Online', 'Offline',
    'Mixed', 'NewCondition', 'UsedCondition', 'RefurbishedCondition', 'DamagedCondition',
    
    # Valores técnicos de Rank Math y otros plugins SEO
    'custom',
    
    # Códigos de idioma ISO 639-1 (formato corto - 2 letras)
    'aa', 'ab', 'ae', 'af', 'ak', 'am', 'an', 'ar', 'as', 'av', 'ay', 'az',
    'ba', 'be', 'bg', 'bh', 'bi', 'bm', 'bn', 'bo', 'br', 'bs',
    'ca', 'ce', 'ch', 'co', 'cr', 'cs', 'cu', 'cv', 'cy',
    'da', 'de', 'dv', 'dz',
    'ee', 'el', 'en', 'eo', 'es', 'et', 'eu',
    'fa', 'ff', 'fi', 'fj', 'fo', 'fr', 'fy',
    'ga', 'gd', 'gl', 'gn', 'gu', 'gv',
    'ha', 'he', 'hi', 'ho', 'hr', 'ht', 'hu', 'hy', 'hz',
    'ia', 'id', 'ie', 'ig', 'ii', 'ik', 'io', 'is', 'it', 'iu',
    'ja', 'jv',
    'ka', 'kg', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'kr', 'ks', 'ku', 'kv', 'kw', 'ky',
    'la', 'lb', 'lg', 'li', 'ln', 'lo', 'lt', 'lu', 'lv',
    'mg', 'mh', 'mi', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'my',
    'na', 'nb', 'nd', 'ne', 'ng', 'nl', 'nn', 'no', 'nr', 'nv', 'ny',
    'oc', 'oj', 'om', 'or', 'os',
    'pa', 'pi', 'pl', 'ps', 'pt',
    'qu',
    'rm', 'rn', 'ro', 'ru', 'rw',
    'sa', 'sc', 'sd', 'se', 'sg', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw',
    'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ty',
    'ug', 'uk', 'ur', 'uz',
    've', 'vi', 'vo',
    'wa', 'wo',
    'xh',
    'yi', 'yo',
    'za', 'zh', 'zu',
    
    # Códigos de idioma en formato largo (ISO 639-1 + región ISO 3166-1)
    'es-ES', 'es-MX', 'es-AR', 'es-CO', 'es-CL', 'es-PE', 'es-VE', 'es-EC', 'es-GT', 'es-CU',
    'es-BO', 'es-DO', 'es-HN', 'es-PY', 'es-SV', 'es-NI', 'es-CR', 'es-PA', 'es-UY', 'es-PR',
    'en-US', 'en-GB', 'en-CA', 'en-AU', 'en-NZ', 'en-IE', 'en-ZA', 'en-IN', 'en-SG', 'en-PH',
    'bg-BG',
    'de-DE', 'de-AT', 'de-CH', 'de-LU', 'de-LI',
    'fr-FR', 'fr-BE', 'fr-CH', 'fr-CA', 'fr-LU', 'fr-MC',
    'it-IT', 'it-CH', 'it-SM',
    'pt-PT', 'pt-BR', 'pt-AO', 'pt-MZ',
    'nl-NL', 'nl-BE', 'nl-SR',
    'pl-PL',
    'ru-RU', 'ru-BY', 'ru-KZ', 'ru-KG',
    'ja-JP',
    'zh-CN', 'zh-TW', 'zh-HK', 'zh-SG',
    'ar-SA', 'ar-EG', 'ar-DZ', 'ar-MA', 'ar-TN', 'ar-OM', 'ar-PS', 'ar-SY', 'ar-JO', 'ar-LB',
    'ca-ES', 'ca-AD', 'ca-FR', 'ca-IT',
    'eu-ES',
    'gl-ES',
    'sv-SE', 'sv-FI',
    'da-DK',
    'fi-FI',
    'no-NO',
    'nb-NO',
    'nn-NO',
    'cs-CZ',
    'sk-SK',
    'hu-HU',
    'ro-RO', 'ro-MD',
    'el-GR', 'el-CY',
    'tr-TR', 'tr-CY',
    'uk-UA',
    'hr-HR',
    'sr-RS',
    'sl-SI',
    'et-EE',
    'lv-LV',
    'lt-LT',
    'sq-AL',
    'mk-MK',
    'bs-BA',
    'is-IS',
    'mt-MT',
    'ga-IE',
    'cy-GB',
    'ko-KR',
    'vi-VN',
    'th-TH',
    'id-ID',
    'ms-MY',
    'hi-IN',
    'bn-BD',
    'ur-PK',
    'fa-IR',
    'he-IL',
    'yi-001',
    'sw-KE', 'sw-TZ',
    'af-ZA',
    'am-ET',
    'hy-AM',
    'az-AZ',
    'be-BY',
    'ka-GE',
    'kk-KZ',
    'km-KH',
    'lo-LA',
    'mk-MK',
    'mn-MN',
    'my-MM',
    'ne-NP',
    'si-LK',
    'ta-IN', 'ta-LK',
    'te-IN',
    'uz-UZ',
    'zu-ZA',
}

def should_skip_translation(text):
    text = text.strip()
    
    # Proteger vocabulario completo de Schema.org
    if text in SCHEMA_VOCABULARY:
        return True
    
    # Proteger patrones CamelCase típicos de Schema (PropertyValue, GeoCoordinates, etc.)
    # Esto cubre términos nuevos que Schema.org pueda añadir en el futuro
    if re.match(r'^[A-Z][a-z]+([A-Z][a-z]+)+$', text) and len(text) > 3:
        return True
    
    # Shortcodes de WordPress/Divi
    if re.match(r'^\[[\w_-]+\s', text) or re.match(r'^\[[\w_-]+\]$', text):
        return True
    if re.match(r'^(\[[\w_-]+[^\]]*\])+$', text.replace('\n', '').replace('\r', '')):
        return True
    
    # URLs completas
    if re.match(r'^https?://[^\s]+$', text):
        return True
    if re.match(r'^https?://[^\s]+#[\w-]+$', text):
        return True
    
    # Rutas de archivos
    if re.match(r'^/[\w\-/\.]+$', text):
        return True
    
    # Fechas ISO
    if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', text):
        return True
    
    # Tamaños de página
    page_sizes = ['A3', 'A4', 'A5', 'B3', 'B4', 'B4-S', 'B5', 'Letter', 'Legal', 'Tabloid', 'Ledger']
    if text in page_sizes:
        return True
    
    # Nombres de fuentes tipográficas
    if re.match(r'^[A-Z][a-z]+(-[A-Z][a-z]+)*$', text) and len(text) < 20:
        return True
    
    # Códigos cortos técnicos
    if re.match(r'^[A-Z0-9]{1,3}(-[A-Z0-9]{1,3})?$', text):
        return True
    
    # Nombres técnicos sin puntuación
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
    response = requests.post("https://api.deepl.com/v2/translate", data={
        'auth_key': API_KEY, 
        'text': texts, 
        'source_lang': source_lang, 
        'target_lang': target_lang, 
        'tag_handling': 'html', 
        'preserve_formatting': '1'
    })
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

def has_valid_translation(source_text, target_text):
    """
    Verifica si el target tiene una traducción válida y completa.
    Retorna True solo si:
    1. El target tiene contenido
    2. El target NO es igual al source (no está sin traducir)
    3. El target tiene la misma estructura HTML que el source
    """
    target_text = target_text.strip()
    source_text = source_text.strip()
    
    # Si el target está vacío, necesita traducción
    if not target_text or target_text in ['', ' ', '\n', '\r\n']:
        return False
    
    # Si target es igual a source, no está traducido
    if target_text == source_text:
        return False
    
    # Extraer tags HTML del source y target para comparar estructura
    source_tags = re.findall(r'<[^>]+>', source_text)
    target_tags = re.findall(r'<[^>]+>', target_text)
    
    # Normalizar tags (eliminar atributos para comparar solo la estructura)
    def normalize_tag(tag):
        # Extraer solo el nombre del tag: <sup class="nota"> -> <sup>
        match = re.match(r'<(/?)(\w+)', tag)
        if match:
            return f"<{match.group(1)}{match.group(2)}>"
        return tag
    
    source_tag_names = [normalize_tag(t) for t in source_tags]
    target_tag_names = [normalize_tag(t) for t in target_tags]
    
    # Si la cantidad de tags es diferente, la estructura está rota
    if len(source_tag_names) != len(target_tag_names):
        return False
    
    # Si los nombres de los tags son diferentes, la estructura está rota
    if source_tag_names != target_tag_names:
        return False
    
    # Si llegamos aquí, el target tiene traducción válida con estructura correcta
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
        if has_valid_translation(src_text, target_text):
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