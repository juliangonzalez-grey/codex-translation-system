# Import dependencies                                                             
from codex.services.translation_service import load_demo_data, translate, sync_translation_data, load_language_pack
from codex.neo4j_driver import find_missing_translations, find_missing_brands, get_equivalent_brands, resolve_to_base_term, driver

# Testing data
# print("\nLoading data")
# load_demo_data()

# All for testing purposes

no_translation_flag = False

choice = input("Load a language pack? (y/n): ")

if choice.lower() == "y":
    path = input("Enter path to JSON language pack: ")
    print(load_language_pack(path))



while True:
    term = input("\nEnter a medical term (or 'exit'): ")
    if term.lower() == "exit":
        break

    lang = input("Enter language code (en, es, fr, ru) or press Enter to skip: ")
    lang = lang if lang else None

    country = input("Enter country code (US, GB, MX, FR, ES, NG, RU) or press Enter to skip: ")
    country = country if country else None

    results = translate(term, lang=lang, country=country)

    print("\n Translation Results")
    if not results:
        print("No translations found.")
        continue
    for r in results:
        print(f"- {r['translation']} ({r['language']}) | Brand: {r['brand']} | Country: {r['country']}")
            
    for r in results:
        translated_term = r["translation"]
        test_more = input(f"\nRun full anaylsis on '{translated_term}'? (y/n): ")
        if test_more.lower() == "y":
            with driver.session() as session:
                base = resolve_to_base_term(session, translated_term)
                #print(f"\nChecking canonical term: {base} (input was '{translated_term}')\n")
                print(f"\nChecking term: {translated_term}\n")
                sync_translation_data(base)
        else:
            break