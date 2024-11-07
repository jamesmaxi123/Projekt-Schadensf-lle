from fpdf import FPDF

# Funktion zur Erstellung einer leeren PDF-Vorlage
def create_empty_template(file_name):
    pdf = FPDF()
    pdf.add_page()

    # Titel
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Versicherung Schadensmeldung", ln=True, align="C")
    pdf.ln(10)

    # Versicherungsdaten
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Versicherungsnehmer: _________________________", ln=True)
    pdf.cell(0, 10, "Adresse: ___________________________________________", ln=True)
    pdf.cell(0, 10, "Telefonnummer: _________________________", ln=True)
    pdf.cell(0, 10, "Versicherungsnummer: _________________________", ln=True)
    pdf.ln(5)

    # Schadensdetails
    pdf.cell(0, 10, "Schadensdatum: _________________________", ln=True)
    pdf.cell(0, 10, "Schadensart: _________________________", ln=True)
    pdf.cell(0, 10, "Schadensort: ___________________________________________", ln=True)
    pdf.cell(0, 10, "Schadenbeschreibung: ___________________________________________", ln=True)
    pdf.ln(5)

    # Schadenhöhe und Belege
    pdf.cell(0, 10, "Geschätzte Schadenssumme: _________________________ EUR", ln=True)
    pdf.cell(0, 10, "Belege vorhanden: _________________________", ln=True)  # ohne Ja/Nein
    pdf.ln(10)

    # Datum Unterschrift
    pdf.ln(10)
    pdf.cell(0, 10, "Ort und Datum: __________________________", ln=True)
    pdf.cell(0, 10, "Unterschrift: ____________________________", ln=True)

    pdf.output(file_name)

# Leere Vorlage speichern

# PDF-Generator-Funktion
def create_pdf(file_name, data):
    pdf = FPDF()
    pdf.add_page()

    # Titel
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Versicherung Schadensmeldung", ln=True, align="C")
    pdf.ln(10)

    # Versicherungsdaten
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Versicherungsnehmer: {data['Versicherungsnehmer']}", ln=True)
    pdf.cell(0, 10, f"Adresse: {data['Adresse']}", ln=True)
    pdf.cell(0, 10, f"Telefonnummer: {data['Telefonnummer']}", ln=True)
    pdf.cell(0, 10, f"Versicherungsnummer: {data['Versicherungsnummer']}", ln=True)
    pdf.ln(5)

    # Schadensdetails
    pdf.cell(0, 10, f"Schadensdatum: {data['Schadensdatum']}", ln=True)
    pdf.cell(0, 10, f"Schadensart: {data['Schadensart']}", ln=True)
    pdf.cell(0, 10, f"Schadensort: {data['Schadensort']}", ln=True)
    pdf.cell(0, 10, f"Schadenbeschreibung: {data['Schadenbeschreibung']}", ln=True)
    pdf.ln(5)

    # Schadenhöhe und Belege
    pdf.cell(0, 10, f"Geschätzte Schadenssumme: {data['Schadenssumme']} EUR", ln=True)
    pdf.cell(0, 10, f"Belege vorhanden: {data['Belege']}", ln=True)
    pdf.ln(10)

    # Unterschrift
    pdf.cell(0, 10, "Ort und Datum: __________________________", ln=True)
    pdf.cell(0, 10, "Unterschrift: ____________________________", ln=True)

    pdf.output(file_name)

# Beispiel-Daten für Schadensmeldungen
beispiel_daten = [
    {
        "Versicherungsnehmer": "Lukas Becker",
        "Adresse": "Beispielweg 45, 98765 Beispielhausen",
        "Telefonnummer": "+49 7736 168405",
        "Versicherungsnummer": "84782638",
        "Schadensdatum": "16.04.2024",
        "Schadensart": "Diebstahl",
        "Schadensort": "Beispielweg 45, 98765 Beispielhausen",
        "Schadenbeschreibung": "Eine Person wurde unabsichtlich verletzt, als eine Leiter umstürzte.",
        "Schadenssumme": "3190.00",
        "Belege": "Nein"
    },
    {
        "Versicherungsnehmer": "Anna Klein",
        "Adresse": "Musterallee 21, 56789 Musterdorf",
        "Telefonnummer": "+49 5586 447812",
        "Versicherungsnummer": "66748293",
        "Schadensdatum": "10.02.2024",
        "Schadensart": "Brand",
        "Schadensort": "Keller, Musterdorf",
        "Schadenbeschreibung": "Feuer im Kellerbereich verursachte Sachschäden.",
        "Schadenssumme": "8900.00",
        "Belege": "Ja"
    },
    {
        "Versicherungsnehmer": "Peter Schmidt",
        "Adresse": "Hauptstraße 100, 12345 Hauptstadt",
        "Telefonnummer": "+49 6063 128674",
        "Versicherungsnummer": "74623891",
        "Schadensdatum": "28.06.2024",
        "Schadensart": "Unfall",
        "Schadensort": "Parkplatz, Hauptstadt",
        "Schadenbeschreibung": "Zusammenstoß auf dem Parkplatz führte zu Fahrzeugschäden.",
        "Schadenssumme": "4500.00",
        "Belege": "Ja"
    },
    {
        "Versicherungsnehmer": "Julia Meyer",
        "Adresse": "Blumenweg 3, 34567 Blumendorf",
        "Telefonnummer": "+49 4471 987543",
        "Versicherungsnummer": "99876123",
        "Schadensdatum": "05.03.2024",
        "Schadensart": "Wasserschaden",
        "Schadensort": "Küche, Blumendorf",
        "Schadenbeschreibung": "Wasserschaden aufgrund defekter Leitung in der Küche.",
        "Schadenssumme": "3200.00",
        "Belege": "Nein"
    },
    {
        "Versicherungsnehmer": "Michael Wagner",
        "Adresse": "Waldstraße 8, 87654 Waldhausen",
        "Telefonnummer": "+49 8893 432187",
        "Versicherungsnummer": "32498176",
        "Schadensdatum": "15.11.2023",
        "Schadensart": "Diebstahl",
        "Schadensort": "Lagerhalle, Waldhausen",
        "Schadenbeschreibung": "Wertgegenstände aus Lagerhalle entwendet.",
        "Schadenssumme": "2750.00",
        "Belege": "Ja"
    }
]

# Erstellen der PDF-Dateien
file_names = []
for i, daten in enumerate(beispiel_daten, start=1):
    file_name = f"/Users/MaxiRo/Desktop/ATIW/5 Block/Projekt Schadensfälle/Schadensmeldung_Beispiel_{i}.pdf"
    create_pdf(file_name, daten)
    file_names.append(file_name)
create_empty_template("/Users/MaxiRo/Desktop/ATIW/5 Block/Projekt Schadensfälle/Schadensmeldung_Vorlage.pdf")
file_names.append(file_name)

file_names
