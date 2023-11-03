import os
import openai
import fitz  # PyMuPDF
import spacy
import re
from pdfminer.high_level import extract_text
from pymongo import MongoClient

# Charger le modèle spaCy pour l'analyse sémantique
nlp = spacy.load('en_core_web_sm')

# Fonction pour extraire le texte du CV depuis un PDF
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# Initialiser la connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['cv_data']  # Nom de la base de données
collection = db['cv_collection']  # Nom de la collection

pdf_path = "resume.pdf"
pdf_text = extract_text_from_pdf(pdf_path)

# Configurer la clé API OpenAI
openai.api_key = "YOUR_API_KEY"

# Fonction pour poser des questions à GPT-3.5 Turbo et extraire les réponses
def ask_questions(prompt, text_to_analyze):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt + "from this resume:  " + text_to_analyze}]
    )
    return response['choices'][0]['message']['content']

# Prompt pour demander l'extraction des informations
prompt = """
    Please extract the following information from the CV:
    Name:
    Email:
    Address:
    Profile:
    Experience:
    Education:
    Skills:
    Projects:

   
    """

# Appeler la fonction pour extraire les réponses
extracted_information = ask_questions(prompt, pdf_text)

# Insérer les données extraites dans MongoDB
data_to_insert = {
    "
    "extracted_information": extracted_information
}

# Insérer dans la collection MongoDB
inserted_data = collection.insert_one(data_to_insert)

print("Data inserted into MongoDB with ID:", inserted_data.inserted_id)
