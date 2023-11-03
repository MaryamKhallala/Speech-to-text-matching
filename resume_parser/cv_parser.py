import fitz  # PyMuPDF
import spacy
import re
from pdfminer.high_level import extract_text

# Charger le modèle spaCy pour l'analyse sémantique
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using pdfminer.
    """
    return extract_text(pdf_path)

def extract_name_from_resume(text):
    """
    Extract the name from the resume using regex.
    """
    name = None

    # Use regex pattern to find a potential name
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern, text)
    if match:
        name = match.group()

    return name

def extract_contact_info(text):
    """
    Extract contact information (phone number and email) from the resume using regex.
    """
    phone_pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    phone_match = re.search(phone_pattern, text)
    email_match = re.search(email_pattern, text)

    phone = phone_match.group() if phone_match else None
    email = email_match.group() if email_match else None

    return phone, email

def segment_cv_text_with_spacy(text):
    """
    Segment the CV text into different sections using spaCy for semantic analysis.
    """
    doc = nlp(text)

    # Initialize a dictionary to store the sections
    sections = {}

    # Define the section names and their associated keywords
    section_keywords = {
        'Experience': ['experience', 'work experience', 'professional experience'],
        'Skills': ['skills', 'technical skills', 'competences'],
        'Education': ['education', 'formation'],
        'Projects': ['projects', 'personal projects', 'side projects', 'projets academiques']
    }

    # Extract sections based on keywords
    for section_name, keywords in section_keywords.items():
        section_content = ""
        for token in doc:
            if any(keyword.lower() in token.text.lower() for keyword in keywords):
                section_content += token.sent.text + "\n"

        if section_content:
            sections[section_name] = section_content.strip()

    return sections

# Main
pdf_path = "resume.pdf"

try:
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Extract name from the resume
    name = extract_name_from_resume(pdf_text)

    # Extract contact information
    phone, email = extract_contact_info(pdf_text)

    # Print extracted information
    print("Name:", name)
    print("Phone:", phone)
    print("Email:", email)

    # Segment the CV text into sections using spaCy
    sections = segment_cv_text_with_spacy(pdf_text)

    # Display the sections
    print("\nSections of the CV:")
    for section_name, content in sections.items():
        print(f"Section: {section_name}")
        print(content)
        print("=" * 50)

except Exception as e:
    print("An error occurred:", str(e))
