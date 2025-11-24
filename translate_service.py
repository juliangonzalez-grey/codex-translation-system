# Import dependencies
from neo4j_driver import create_translation, get_translation_data, find_missing_translations, find_missing_brands, get_equivalent_brands, driver
import json

# Loads sample translation data into the Neo4j database
def load_demo_data():
    with driver.session() as session:
        # Ibuprofen
        create_translation(session, "Ibuprofen", "Advil", "US", "en", "English", "ibuprofen")
        create_translation(session, "Ibuprofen", "Brufen", "FR", "fr", "French", "ibuprofène")
        create_translation(session, "Ibuprofen", "Nurofen", "GB", "en", "English", "ibuprofen")
        create_translation(session, "Ibuprofen", None, "NG", "en", "English", "ibuprofen")
        create_translation(session, "Ibuprofen", "Advil", "MX", "es", "Spanish", "ibuprofeno")
        create_translation(session, "Ibuprofen", "Espidifen", "ES", "es", "Spanish", "ibuprofeno")

        # Paracetamol
        create_translation(session, "Paracetamol", "Tylenol", "US", "en", "English", "acetaminophen")
        create_translation(session, "Paracetamol", "Calpol", "GB", "en", "English", "paracetamol")
        create_translation(session, "Paracetamol", "Doliprane", "FR", "fr", "French", "paracétamol")
        create_translation(session, "Paracetamol", "Panadol", "NG", "en", "English", "paracetamol")
        create_translation(session, "Paracetamol", None, "ES", "es", "Spanish", "paracetamol")

        # Amoxicillin
        create_translation(session, "Amoxicillin", "Amoxil", "US", "en", "English", "amoxicillin")
        create_translation(session, "Amoxicillin", "Clamoxyl", "FR", "fr", "French", "amoxicilline")
        create_translation(session, "Amoxicillin", "Amoxil", "MX", "es", "Spanish", "amoxicilina")
        create_translation(session, "Amoxicillin", None, "IN", "en", "English", "amoxicillin")
        

    return {"status": "Demo data added"}

# Retrieve all translations for a given term, including brand, country, and language information
def translate(term: str, lang: str = None, country: str = None):
    with driver.session() as session:
        records = get_translation_data(session, term, lang, country) 
        if not records:
            return None
        return [
            {
                "term": term,
                "translation": r["translation"],
                "language": r["language"],
                "brand": r["brand"],
                "country": r["country"]
            }
            for r in records
        ]

# Quality check to find missing translations and brand names
# Prints equivalent brands across countries
def sync_translation_data(term: str):
    with driver.session() as session:
        print(f"Checking term: {term}\n")

        missing_translations = find_missing_translations(session, term)
        print("Missing Translations: ")
        if missing_translations:
            for m in missing_translations:
                print(f" - {m['country']} ({m['country_name']}) -> {m['reason']}")
        else:
            print("All translations present")
        
        print("\nMissing Brand Names:")

        missing_brands = find_missing_brands(session, term)
        if missing_brands:
            for m in missing_brands:
                print(f" - {m['country']} ({m['country_name']}) -> {m['reason']}")
        else:
            print("All brand names present")
            
        print("\nEquivalent Brands Across Countries:")

        equivalents = get_equivalent_brands(session, term)
        for e in equivalents:
            print(f" - {e['brand']} ({e['country']} / {e['country_name']})")

# Loads language packs 
def load_language_pack(path_to_json):
    with open(path_to_json, "r") as file:
        pack = json.load(file)

    lang_code = pack["language"]["code"]
    lang_name = pack["language"]["name"]

    with driver.session() as session:
        for term in pack["terms"]:
            canonical = term["canonical"]

            for entry in term["entries"]:
                translation = entry["translation"]
                country = entry["country"]
                brand = entry.get("brand") # Could be None

                create_translation(
                    session,
                    canonical=canonical,
                    brand=brand,
                    country=country,
                    lang_code=lang_code,
                    lang_name=lang_name,
                    translation=translation
                )
    return f"Loaded language pack: {lang_name}"


