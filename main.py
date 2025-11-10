#Import dependencies
from neo4j import GraphDatabase     # Python driver from Neo4j
import os                           # Used to access enviormental variables
from dotenv import load_dotenv      # Imports variables from .env file

# Load enviorment variables from .env file
load_dotenv()

# Get Neo4j connection info
uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(user, password))

# Create or update medication translation nodes
def create_translation(session, canonical, brand, country, lang_code, lang_name, translation):
    query = """
    MERGE (t:Term {canonical:$canonical, type:'medication'})
    MERGE (b:Brand {name:$brand})-[:BRAND_OF]->(t)
    MERGE (c:Country {iso2:$country, name:$country})
    MERGE (b)-[:SOLD_IN]->(c)
    MERGE (l:Language {code:$lang_code, name:$lang_name})
    MERGE (tr:Translation {text:$translation, verified:true})
    MERGE (tr)-[:OF_TERM]->(t)
    MERGE (tr)-[:IN_LANGUAGE]->(l)
    """
    session.run(query, canonical=canonical, brand=brand, country=country, lang_code=lang_code, lang_name=lang_name, translation=translation)
    print(f"Added {canonical} → {translation} ({lang_name}) / Brand: {brand} in {country}")

# Query translations for a medication term
def get_translations(session, canonical):
    query = """
    MATCH (t:Term {canonical:$canonical})<-[:OF_TERM]-(tr:Translation)-[:IN_LANGUAGE]->(l:Language)
    RETURN tr.text AS translation, l.name AS language
    ORDER BY l.name
    """
    results = session.run(query, canonical=canonical)
    print(f"\nTranslations for '{canonical}':")
    for record in results:
        print(f" - {record['translation']} ({record['language']})")

# Get all info for desired term
def get_full_term_info(session, canonical):
    query = """
    MATCH (t:Term {canonical:$canonical})
    OPTIONAL MATCH (t)<-[:OF_TERM]-(tr:Translation)-[:IN_LANGUAGE]->(l:Language)
    OPTIONAL MATCH (t)<-[:BRAND_OF]-(b:Brand)-[:SOLD_IN]->(c:Country)
    RETURN t.canonical AS term,
           collect(DISTINCT tr.text + ' (' + l.name + ')') AS translations,
           collect(DISTINCT b.name + ' in ' + c.name) AS brands
    """
    result = session.run(query, canonical=canonical).single()
    if result:
        print(f"\n {result['term']}")
        print("Translations:")
        for t in result["translations"]:
            if t: print(f" - {t}")
        print("\n Brands:")
        for b in result["brands"]:
            if b: print(f" - {b}")

# Main program
with driver.session() as session:
    #create_translation(session, "ibuprofen","ibuprofène", "ibuprofeno")
    #create_translation(session, "acetaminophen", "paracétamol", "paracetamol")
    #create_translation(session, "aspirin", "aspirine", "aspirina")

    #get_translations(session, "acetaminophen")
    #create_translation(session, "Paracetamol", "Panadol", "NG", "en", "English", "paracetamol")
    get_full_term_info(session, "Paracetamol")
    get_translations(session, "Paracetamol")
    
# Close connection
driver.close()


