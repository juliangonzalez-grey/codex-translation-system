# Import dependencies
from neo4j_driver import create_translation, get_translation_data, driver

# Loads sample translation data into the Neo4j database
def load_demo_data():
    with driver.session() as session:
        create_translation(session, "Paracetamol", "Panadol", "NG", "en", "English", "paracetamol")
        create_translation(session, "Ibuprofen", "Advil", "US", "en", "English", "ibuprofen")
        create_translation(session, "Ibuprofen", "Brufen", "FR", "fr", "French", "ibuprofène")
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




