# Import dependencies                                                             
from translate_service import load_demo_data, translate, sync_translation_data, load_language_pack
from neo4j_driver import find_missing_translations, find_missing_brands, get_equivalent_brands, driver

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
        no_translation_flag = True
    else:
        for r in results:
            print(f"- {r['translation']} ({r['language']}) | Brand: {r['brand']} | Country: {r['country']}")
            
    if(no_translation_flag != True):
        test_more = input("\nRun full anaylsis on this term? (y/n): ")
        if test_more.lower() == "y":
            sync_translation_data(term)
        else:
            break