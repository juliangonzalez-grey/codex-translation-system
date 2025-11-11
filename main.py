#Import dependencies
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn 
from neo4j_driver import create_translation, get_translation_data, driver


# Create the FastAPI app instance 
app = FastAPI(title="Codex Translation API Demo")

@app.get("/status")
def status():
    return {"status": "API running and connected to Neo4j"}

@app.post("/demo_data")
def load_demo_data():
    with driver.session() as session:
        create_translation(session, "Paracetamol", "Panadol", "NG", "en", "English", "paracetamol")
        create_translation(session, "Ibuprofen", "Advil", "US", "en", "English", "ibuprofen")
        create_translation(session, "Ibuprofen", "Brufen", "FR", "fr", "French", "ibuprofène")
    return {"status": "Demo data added"}

@app.post("/translate/{term}")
def translate(term: str, lang: str = None, country: str = None):
    with driver.session() as session:
        records = get_translation_data(session, term, lang, country)
        if not records:
            raise HTTPException(status_code=404, detail=f"No translation found for '{term}'")
        response = []
        for r in records:
            response.append({
                "term": term,
                "translation": r["translation"],
                "language": r["language"],
                "brand": r["brand"],
                "country": r["country"]
            })
        return JSONResponse(content=response)
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


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
#with driver.session() as session:
    #create_translation(session, "ibuprofen","ibuprofène", "ibuprofeno")
    #create_translation(session, "acetaminophen", "paracétamol", "paracetamol")
    #create_translation(session, "aspirin", "aspirine", "aspirina")

    #get_translations(session, "acetaminophen")
    #create_translation(session, "Paracetamol", "Panadol", "NG", "en", "English", "paracetamol")
    #get_full_term_info(session, "Paracetamol")
    #get_translations(session, "Paracetamol")
    
# Close connection
#driver.close()


