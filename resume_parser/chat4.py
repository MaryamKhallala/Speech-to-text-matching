import os
import openai
import fitz  # PyMuPDF
import spacy
import re
from pdfminer.high_level import extract_text
from pymongo import MongoClient

# Initialiser la connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['cv_data']  # Nom de la base de données
collection = db['cv_collection']  # Nom de la collection

# Charger le modèle spaCy pour l'analyse sémantique
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using pdfminer.
    """
    return extract_text(pdf_path)
pdf_path = "resume.pdf"

    # Extraire le texte du PDF
pdf_text = extract_text_from_pdf(pdf_path)
openai.api_key = "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"

def ask_questions(prompt, text_to_analyze):
   
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt + "from this resume:  " + text_to_analyze}
            
        ]
    )
    answer = response['choices'][0]['message']['content']
    return answer
prompt = """
    Extract the following information from the CV:
    Name:
    Email:
    Address:
    Profile:
    Experience:
    Education:
    Skills:
    Projects:

    """
prompt1="""
    Extract the following information from the CV:
    Name:
    """
prompt2="""
    Extract the following information from the CV:
    Email:
    """
prompt3="""
    Extract the following information from the CV:
    Address:
    """
prompt4="""
    Extract the following information from the CV:
    Profile:
    """
prompt5="""
    Extract the following information from the CV:
    Experience:
    """
prompt6="""
    Extract the following information from the CV:
    Education:
    """
prompt7="""
    Extract the following information from the CV:
    Skills:
    """
prompt8="""
    Extract the following information from the CV:
    Projects:
    """
print(ask_questions(prompt, pdf_text))
# Appeler la fonction pour extraire les réponses
extracted_information= {
   'Name' :ask_questions(prompt1, pdf_text),
   'Email': ask_questions(prompt2, pdf_text),
   'Address': ask_questions(prompt3, pdf_text),
   'Profile': ask_questions(prompt4, pdf_text),
   'Experience': ask_questions(prompt5, pdf_text),
   'Education' : ask_questions(prompt6, pdf_text),
   'Skills': ask_questions(prompt7, pdf_text),
   'Projects' : ask_questions(prompt8, pdf_text)
}
# Insérer les données extraites dans MongoDB


# Insérer dans la collection MongoDB
collection.insert_one(extracted_information)

print("Data inserted into MongoDB ")