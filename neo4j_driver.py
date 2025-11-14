# Import dependencies
from neo4j import GraphDatabase       # Python driver from Neo4j
from dotenv import load_dotenv        # Used to access enviormental variables
import os                             # Imports variables from .env file

# Loads environment varibles 
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
    MERGE (l:Language {code:$lang_code, name:$lang_name})
    MERGE (tr:Translation {text:$translation, verified:true})
    MERGE (tr)-[:OF_TERM]->(t)
    MERGE (tr)-[:IN_LANGUAGE]->(l)
    MERGE (b:Brand {name:$brand})
    MERGE (c:Country {iso2:$country, name:$country})
    MERGE (b)-[:SOLD_IN]->(c)
    MERGE (tr)-[:HAS_BRAND]->(b)
    """
    # Execute the Cypher query using the session
    session.run(query, canonical=canonical, brand=brand, country=country, lang_code=lang_code, lang_name=lang_name, translation=translation)

    # Just for comfirmation in console for verification
    print(f"Added {canonical} → {translation} ({lang_name}) / Brand: {brand} in {country}")

# Retrieves all translations and related info for a given term
def get_translation_data(session, canonical, lang=None, country=None):
    query = """
    MATCH (t:Term {canonical:$canonical})
    MATCH (tr:Translation)-[:OF_TERM]->(t)
    MATCH (tr)-[:IN_LANGUAGE]->(l:Language)
    OPTIONAL MATCH (tr)-[:HAS_BRAND]->(b:Brand)
    OPTIONAL MATCH (b)-[:SOLD_IN]->(c:Country)
    WHERE ($lang IS NULL OR l.code = $lang)
      AND ($country IS NULL OR c.iso2 = $country)
    RETURN tr.text AS translation, 
        l.name AS language,
        b.name AS brand, 
        c.name AS country
    ORDER BY l.name
    """
     # Runs the query and return the results as a list
    return list(session.run(query, canonical=canonical, lang=lang, country=country))
