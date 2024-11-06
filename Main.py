import sqlite3
import pytesseract
from pdf2image import convert_from_path
import os
from tkinter import Tk, filedialog, Button, Label, Frame, messagebox, Entry, StringVar, Text


# Tesseract-OCR-Pfad
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# Funktion zur Extraktion von Daten aus einem Bild
def extract_data_from_image(image):
    # OCR auf das Bild anwenden
    text = pytesseract.image_to_string(image, lang='deu')
    return text

# Funktion zur Verarbeitung einer PDF-Datei
def process_pdf(pdf_path):
    # PDF in Bilder konvertieren
    images = convert_from_path(pdf_path)
    
    # Daten für die Datenbank sammeln
    schadensmeldung_data = {}
    
    for image in images:
        text = extract_data_from_image(image)

        for line in text.splitlines():
            if "Versicherungsnummer" in line:
                schadensmeldung_data["versicherungsnummer"] = line.split(":")[-1].strip()
            elif "Versicherungsnehmer" in line:
                schadensmeldung_data["versicherungsnehmer"] = line.split(":")[-1].strip()
            elif "Adresse" in line:
                schadensmeldung_data["adresse"] = line.split(":")[-1].strip()
            elif "Schadensdatum" in line:
                schadensmeldung_data["schadensdatum"] = line.split(":")[-1].strip()
            elif "Schadensart" in line:
                schadensmeldung_data["schadensart"] = line.split(":")[-1].strip()
            elif "Schadensort" in line:
                schadensmeldung_data["schadensort"] = line.split(":")[-1].strip()
            elif "Schadenbeschreibung" in line:
                schadensmeldung_data["beschreibung"] = line.split(":")[-1].strip()
            elif "Schadenssumme" in line:
                schadensmeldung_data["schadenssumme"] = float(line.split(":")[-1].strip().replace("EUR", "").replace(",", ".").strip())
            elif "Telefonnummer" in line:
                schadensmeldung_data["telefonnummer"] = line.split(":")[-1].strip()

    return schadensmeldung_data

# Funktion zur Speicherung der Daten in die Datenbank
def save_data_to_db(data):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect('datenbank.db')
    cursor = conn.cursor()

    # Tabelle erstellen
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Versicherungsnehmer (
    Versicherungsnehmer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(100),
    Adresse VARCHAR(255),
    Telefonnummer VARCHAR(20)
);''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Schadensmeldung (
        Schadensnummer INTEGER PRIMARY KEY AUTOINCREMENT,
        Schadensdatum DATE,
        Schadensart TEXT,
        Schadensort TEXT,
        Beschreibung TEXT,
        Schadenssumme TEXT,
        Versicherungsnehmer_id INTEGER,
        FOREIGN KEY (Versicherungsnehmer_id) REFERENCES Versicherungsnehmer(Versicherungsnehmer_id)
    )
    ''')

    # Daten in die Datenbank einfügen
  
    cursor.execute('''
    INSERT INTO Schadensmeldung 
    (Schadensdatum, Schadensart, Schadensort, Beschreibung, Schadenssumme, Versicherungsnehmer_id)
    VALUES (:schadensdatum, :schadensart, :schadensort, :beschreibung, :schadenssumme, :versicherungsnummer)
    ''', data)
    
    cursor.execute('''
    INSERT OR IGNORE INTO Versicherungsnehmer 
    (Versicherungsnehmer_id, Name, Adresse, Telefonnummer)
    VALUES (:versicherungsnummer, :versicherungsnehmer, :adresse, :telefonnummer)
    ''', data)
    
    """
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
    pdf_folder = "/Users/MaxiRo/Desktop/ATIW/5 Block/Projekt Schadensfälle/PDF-Ordner"
    main(pdf_folder)
    
    cursor.execute('''
    INSERT INTO Versicherungspolice 
    (Versicherungsnummer, Versicherungsnehmer_id,)
    VALUES (:versicherungsnummer, :versicherungsnehmer)
    ''', data)
    """
    # Änderungen speichern
    conn.commit()
    conn.close()
    
#Einzelne PDF-Datei einlesen
def handle_single_pdf_processing():
    pdf_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_file:
        schadensmeldung_data = process_pdf(pdf_file)
        save_data_to_db(schadensmeldung_data)
        messagebox.showinfo("Erfolg", f"Daten aus {pdf_file} wurden erfolgreich in die Datenbank eingefügt.")
        
#Mehrere PDF-Dateien einlesen
def handle_folder_processing():
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Alle PDF-Dateien im Ordner finden
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_path, pdf_file)
            schadensmeldung_data = process_pdf(pdf_path)
            save_data_to_db(schadensmeldung_data)
        
        messagebox.showinfo("Erfolg", f"Alle PDF-Dateien im Ordner wurden erfolgreich in die Datenbank eingefügt.")
        
# Suchfunktion für Versicherungsnummer
def search_versicherungsnummer(versicherungsnummer):
    conn = sqlite3.connect('datenbank.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Versicherungsnehmer WHERE Versicherungsnehmer_ID = ?", (versicherungsnummer,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        messagebox.showinfo("Ergebnis", f"Versicherungsnummer: {result[0]}, Versicherungsnehmer: {result[1]}, Adresse: {result[2]}, Telefonnummer: {result[3]}")
    else:
        messagebox.showinfo("Ergebnis", "Keine Daten zur Versicherungsnummer gefunden.")
        
# Suchfunktion für Schadensnummer
def search_schadensnummer(schadensnummer):
    conn = sqlite3.connect('datenbank.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Schadensmeldung WHERE Schadensnummer = ?", (schadensnummer,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        messagebox.showinfo("Ergebnis", f"Schadensnummer: {result[0]}, Datum: {result[1]}, Art: {result[2]}, Ort: {result[3]}, Summe: {result[5]} EUR, Versicherungsnummer: {result[6]}")
    else:
        messagebox.showinfo("Ergebnis", "Keine Daten zur Schadensnummer gefunden.")

# Hauptfenster der Anwendung erstellen
def main():
    root = Tk()
    root.title("Schadensmeldung Verarbeitung")
    root.geometry("600x500")
    root.config(bg="#f4f4f9")
    
    # Titel-Label
    title_label = Button(root, text="Schadensmeldung Datenbank", font=("Arial", 18, "bold"), bg="#f4f4f9", fg="#333")
    title_label.pack(pady=20)

    # Rahmen für die Inhalte
    frame = Frame(root, bg="#f4f4f9", bd=2, relief="groove")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Button zur Auswahl einer einzelnen PDF
    single_pdf_button = Button(frame, text="Einzelne PDF-Datei verarbeiten", command=handle_single_pdf_processing, 
                               font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
    single_pdf_button.pack(pady=10)

    # Button zur Auswahl eines Ordners mit mehreren PDFs
    folder_button = Button(frame, text="Ganzen Ordner verarbeiten", command=handle_folder_processing, 
                           font=("Arial", 12), bg="#2196F3", fg="white", padx=10, pady=5)
    folder_button.pack(pady=10)

    # Versicherungsnummer Suche
    versicherung_entry = Entry(frame, font=("Arial", 12))
    versicherung_entry.pack(pady=5)
    search_versicherung_button = Button(frame, text="Versicherungsnummer suchen", command=lambda: search_versicherungsnummer(versicherung_entry.get()), 
                                        font=("Arial", 12), bg="#FF9800", fg="white")
    search_versicherung_button.pack(pady=5)

    # Schadensnummer Suche
    schaden_entry = Entry(frame, font=("Arial", 12), bg="#FF9800", fg="white")
    schaden_entry.pack(pady=5)
    search_schaden_button = Button(frame, text="Schadensnummer suchen", command=lambda: search_schadensnummer(schaden_entry.get()), 
                                   font=("Arial", 12), bg="#FF9800", fg="white")
    search_schaden_button.pack(pady=5)

    # Exit Button
    exit_button = Button(root, text="Beenden", command=root.quit, 
                         font=("Arial", 10), bg="#f44336", fg="white", padx=5, pady=2)
    exit_button.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()