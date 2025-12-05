# Codex Translation API

This is the backend API for "Project Codex", a medical terminology translation tool built with "Neo4j" and a python driver.

This app allows patients and doctors to translate medical terms offline, or online, using a local Neo4j database.

---

Features

- Translate medical terminology between multiple languages
- Neo4j graph database for terms, languages, and relationships
- Simple local environment setup

---

Requirements

Have the following installed:

- Python 3.10
- Virtual enviornment (venv)
- Neo4j Desktop
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

6. Run streamlit dashboard front end

   - pip install streamlit
   - streamlit run ./streamlit_app.py
   - running on python3.11.xx here

7. Project Structure:
   - codex-translation-api/
     - main.py # CLI for testing
     - streamlit_app.py # GUI/front end for our demo
     - neo4j_driver.py # Neo4j connection logic
     - requirements.txt # Python dependencies
     - .env (ignored) # Local database credentials
     - venv/ # Virtual enviornment
     - README.md # Setting up environment
