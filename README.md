# Codex Translation API

This is the backend API for "Project Codex", a medical terminology transaltion tool build with "FastAPI" and "Neo4j"

This API allows patients and doctors to translate medical terms offline or online using a local Neo4j database.

---

Features

- Translate medical terminology between multiple languages
- Fast API backedn with Swagger UI documentation
- Neo4j graph database for terms, languages, and relationships
- Simple local enviornment setup

---

Requirements

Have the following installed:

- Python 3.10
- Virtual enviornment (venv)
- Neo4j Desktop
- Neo4j APOC plug-in
- Git

---

Local Setup (Step-by-Step)

1. Clone the Repo
   - git clone https://github.com/YourUsername/codex-translation-api.git
   - cd codex-transaltion-api
2. Create and Activate Virtual Enviornment

   - python3 -m venv venv
   - source venv/bin/activate (for mac)

3. Install Dependencies

   - pip install -r requirements.txt

4. Create Your .env File in your project folder

   - NEO4J_URI=bolt://localhost:7687
   - NEO4J_USER=neo4j
   - NEO4J_PASSWORD=yourpassword
   - (Make sure to not commit .env, it's personal to you).

5. Set Up Neo4j Database

   - Open Neo4j Desktop
   - Create a new local database
   - Set the password (the same one inside your .env)
   - Start the database
   - Install the APOC plugin (for future fuzzy matching)

6. Run the API

   - uvicorn main:app --reload
   - You should then see:
     - INFO: Uvicorn running on http://127.0.0.1:8000
   - Copy and paste that URL into a browser with /docs at the end of it (http://127.0.0.1:8000/docs) to see Fast API's interactive documentation

7. Project Structure:
   - codex-translation-api/
     - main.py # FastAPI entrypoint
     - neo4j_driver.py # Neo4j connection logic
     - requirements.txt # Python dependencies
     - .env (ignored) # Local database credentials
     - venv/ # Virtual enviornment
     - README.md # Setting up enviornment
