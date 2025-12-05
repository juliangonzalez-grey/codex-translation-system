import streamlit as st
from neo4j import GraphDatabase
from codex.services.translation_service import load_demo_data, translate, sync_translation_data, load_language_pack, find_missing_translations, find_missing_brands, get_equivalent_brands
from codex.neo4j_driver import get_translation_data, driver, resolve_to_base_term

if "current_translation" not in st.session_state:
    st.session_state["current_translation"] = None

apptitle = 'Codex Translator'

st.set_page_config(page_title=apptitle, page_icon="💊")
st.title("Codex: Medical Term Translator")

st.markdown("""
Use the left panel to input a medical term, target language and country, or import a language pack
            """)

# lists for the select boxes
langlist = ["", "en", "es", "fr", "ru", "uk", "pt", "pl"]
countrylist = ["", "US", "MX", "GB", "FR", "ES", "RU", "UA", "PL", "CA"]

st.sidebar.header("Translation Controls")
term = st.sidebar.text_input("Enter a medication")
if term.strip() == "":
    st.sidebar.warning = ("Please enter a medication name")

lang = st.sidebar.selectbox("Target language", langlist)
country = st.sidebar.selectbox("Target country", countrylist)

translate_button = st.sidebar.button(
    "Translate",
    disabled=term.strip() == ""
    )

st.sidebar.markdown("### Language Pack Loader")

import_path = st.sidebar.text_input("Drag and drop a language pack or leave empty to skip")

if st.sidebar.button("Import Language Pack") and import_path:
    try:
        load_language_pack(import_path)
        st.success(f"Loaded language pack from {import_path}")
    except Exception as e:
        st.error(f"Failed to load language pack: {e}")

st.markdown("### Translation Results")
if translate_button and term:

    lang = lang if lang != "" else None
    country = country if country != "" else None

    try:
        results = translate(term, lang=lang or None, country=country or None)
    
        st.session_state["current_translation"] = {
            "term": term,
            "lang": lang,
            "country": country,
            "results": results.get("results", []),
        }

        st.write(f"**Term:** {term}  |  **Requested Language:** {lang}  |  **Selected Country:** {country}")

        if results.get("fallback_used"):
            st.warning("Fallback Activated")
            st.write(f"**Fallback Type:** {results.get('fallback_type', 'unknown')}")
            st.write(f"**Fallback Chain:** {results.get('fallback_chain', [])}")
        else:
            st.success("Direct translation used. No fallback needed")

        if not results.get("results"):
            st.error("No translations found.")

    except Exception as e:
        st.error(f"Translation failed: {e}")

if st.session_state["current_translation"]:
    entry = st.session_state["current_translation"]
    st.write(f"**Term:** {entry['term']}  |  **Requested Language:** {entry['lang']}  |  **Selected Country:** {entry['country']}")
    
    if entry["results"]:
        for r in entry["results"]:
            st.write(f"- **{r['translation']}** ({r['language']}) | Brand: {r['brand']} | Country: {r['country']}")

current_translation = st.session_state.get("current_translation")
if current_translation and current_translation.get("results"):

    # same function as translation_service.py but altered it for streamlit
    full_analysis = st.button(f"Run full analysis on '{current_translation['term']}'?")

    if full_analysis and st.session_state["current_translation"]:
        with driver.session() as session:
            base_term = resolve_to_base_term(session, current_translation["term"])
            st.write(f"Running full analysis on: **{current_translation['term']}**")

            # Missing translations
            missing_translations = find_missing_translations(session, base_term)
            st.subheader("Missing Translations")
            if missing_translations:
                for m in missing_translations:
                    st.write(f" - {m['country']} ({m['country_name']}) → {m['reason']}")
            else:
                st.success("All translations present")

            # Missing brands
            missing_brands = find_missing_brands(session, base_term)
            st.subheader("Missing Brand Names")
            if missing_brands:
                for m in missing_brands:
                    st.write(f" - {m['country']} ({m['country_name']}) → {m['reason']}")
            else:
                st.success("All brand names present")

            # Equivalent brands
            equivalents = get_equivalent_brands(session, base_term)
            st.subheader("Equivalent Brands Across Countries")
            if equivalents:
                for e in equivalents:
                    st.write(f" - {e['brand']} ({e['country']} / {e['country_name']})")
            else:
                st.info("No equivalent brands found")