import sqlite3

# Verbindung zur SQLite-Datenbank herstellen (oder neue Datenbank erstellen)
conn = sqlite3.connect('datenbank.db')
cursor = conn.cursor()

# Tabelle erstellen (falls noch nicht vorhanden)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Schadensmeldung (
    id INTEGER PRIMARY KEY,
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

conn.commit()

# Beispiel für extrahierte Daten aus dem OCR
schadensmeldung_data = {
    "versicherungsnummer": "12345678",
    "versicherungsnehmer": "Max Mustermann",
    "adresse": "Musterstraße 1, 12345 Musterstadt",
    "schadensnummer": "SCH987654",
    "schadensdatum": "2023-10-25",
    "schadensart": "Diebstahl",
    "schadensort": "Lagerhalle A, Musterstadt",
    "beschreibung": "Einbruch in die Lagerhalle, mehrere Geräte gestohlen.",
    "schaedenssumme": 4500.00
}

# Daten in die Datenbank einfügen
cursor.execute('''
INSERT INTO Schadensmeldung 
(versicherungsnummer, versicherungsnehmer, adresse, schadensnummer, schadensdatum, schadensart, schadensort, beschreibung, schaedenssumme)
VALUES (:versicherungsnummer, :versicherungsnehmer, :adresse, :schadensnummer, :schadensdatum, :schadensart, :schadensort, :beschreibung, :schaedenssumme)
''', schadensmeldung_data)

conn.commit()

# Alle Schadensmeldungen abrufen
cursor.execute("SELECT * FROM Schadensmeldung")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
