import sqlite3
import pytesseract
from pdf2image import convert_from_path
import os

# Tesseract-OCR-Pfad (anpassen, falls erforderlich)
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'  # Beispiel für macOS

# Funktion zur Extraktion von Daten aus einem Bild
def extract_data_from_image(image):
    # OCR auf das Bild anwenden
    text = pytesseract.image_to_string(image, lang='deu')  # 'deu' für Deutsch
    return text

# Funktion zur Verarbeitung einer PDF-Datei
def process_pdf(pdf_path):
    # PDF in Bilder konvertieren
    images = convert_from_path(pdf_path)
    
    # Daten für die Datenbank sammeln
    schadensmeldung_data = {}
    
    for image in images:
        text = extract_data_from_image(image)

        # Hier die Logik zur Extraktion relevanter Daten hinzufügen
        # Beispiel für die Extraktion von Daten durch reguläre Ausdrücke oder einfache String-Operationen:
        for line in text.splitlines():
            if "Versicherungsnummer" in line:
                schadensmeldung_data["versicherungsnummer"] = line.split(":")[-1].strip()
            elif "Versicherungsnehmer" in line:
                schadensmeldung_data["versicherungsnehmer"] = line.split(":")[-1].strip()
            elif "Adresse" in line:
                schadensmeldung_data["adresse"] = line.split(":")[-1].strip()
            elif "Schadensnummer" in line:
                schadensmeldung_data["schadensnummer"] = line.split(":")[-1].strip()
            elif "Schadensdatum" in line:
                schadensmeldung_data["schadensdatum"] = line.split(":")[-1].strip()
            elif "Schadensart" in line:
                schadensmeldung_data["schadensart"] = line.split(":")[-1].strip()
            elif "Schadensort" in line:
                schadensmeldung_data["schadensort"] = line.split(":")[-1].strip()
            elif "Schadenbeschreibung" in line:
                schadensmeldung_data["beschreibung"] = line.split(":")[-1].strip()
            elif "Schadenssumme" in line:
                schadensmeldung_data["schaedenssumme"] = float(line.split(":")[-1].strip().replace("EUR", "").replace(",", ".").strip())


    return schadensmeldung_data

# Funktion zur Speicherung der Daten in die Datenbank
def save_data_to_db(data):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect('datenbank.db')
    cursor = conn.cursor()

    # Tabelle erstellen (falls noch nicht vorhanden)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Schadensmeldung (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        versicherungsnummer TEXT,
        versicherungsnehmer TEXT,
        adresse TEXT,
        schadensnummer TEXT,
        schadensdatum TEXT,
        schadensart TEXT,
        schadensort TEXT,
        beschreibung TEXT,
        schaedenssumme REAL
    )
    ''')

    # Daten in die Datenbank einfügen
    cursor.execute('''
    INSERT INTO Schadensmeldung 
    (versicherungsnummer, versicherungsnehmer, adresse, schadensnummer, schadensdatum, schadensart, schadensort, beschreibung, schaedenssumme)
    VALUES (:versicherungsnummer, :versicherungsnehmer, :adresse, :schadensnummer, :schadensdatum, :schadensart, :schadensort, :beschreibung, :schaedenssumme)
    ''', data)

    # Änderungen speichern
    conn.commit()
    conn.close()

# Hauptfunktion
def main(pdf_folder):
    # Alle PDF-Dateien im angegebenen Ordner verarbeiten
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Verarbeite {pdf_path}...")
            schadensmeldung_data = process_pdf(pdf_path)
            save_data_to_db(schadensmeldung_data)
            print(f"Daten aus {pdf_path} wurden erfolgreich in die Datenbank eingefügt.")

# Aufruf der Hauptfunktion
if __name__ == "__main__":
    pdf_folder = "/Users/MaxiRo/Desktop/ATIW/5 Block/Projekt Schadensfälle/PDF-Ordner"  # Hier den Pfad zu deinem PDF-Ordner angeben
    main(pdf_folder)
