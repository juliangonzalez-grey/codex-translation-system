import streamlit as st
from neo4j import GraphDatabase
from codex.services.translation_service import load_demo_data, translate, sync_translation_data, load_language_pack
from codex.neo4j_driver import get_translation_data, driver

st.title("Codex: Medical Term Translator")

# this allows you to drag and drop a language pack directly into the browser 
import_path = st.text_input("Load a language pack (enter path to JSON) or leave blank to skip:")
if st.button("Import Language Pack") and import_path:
    load_language_pack(import_path)
    st.success(f"Loaded language pack from {import_path}")
    
# input fields and buttons
term = st.text_input("Enter a medication term")
lang = st.selectbox("Target language", ["", "en", "ru", "es", "uk"])
country = st.selectbox("Target country", ["", "US", "GB", "CA", "FR", "ES", "RU", "UA", "PL"])

if st.button("Translate") and term:
    with driver.session() as session:
        results = get_translation_data(session, term, lang or None, country or None)
        if results:
            for r in results:
                st.write(f"- {r['translation']} ({r['language']}) | Brand: {r['brand']} | Country: {r['country']}")
        else:
            st.write("No translations found.")