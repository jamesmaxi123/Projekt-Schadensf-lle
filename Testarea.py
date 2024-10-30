from PIL import Image
import pytesseract
import cv2
import re

image_path = '/Users/MaxiRo/Desktop/ATIW/5 Block/Projekt Schadensfälle/Schadensmeldung_Beispiel_1.pdf'  # Ersetzen Sie dies durch den Pfad zu einem Testbild
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Definiere den Bereich, der analysiert werden soll (ROI-Koordinaten)
# Beispiel-Koordinaten: (x, y, breite, höhe)
x, y, w, h = 100, 200, 300, 50  # Anpassen an den Bereich im Dokument
roi = gray[y:y+h, x:x+w]

text = pytesseract.image_to_string(roi, lang='deu')
print("Erkannter Text im Bereich:\n", text)


# Angenommen, "text" ist der erkannte Text aus OCR
text = "Schadentag / Schadenuhrzeit: 29.10.2024"

# Regex für ein Datum im Format "TT.MM.JJJJ"
date_pattern = r"\b\d{2}\.\d{2}\.\d{4}\b"
date_match = re.search(date_pattern, text)

if date_match:
    print("Gefundenes Datum:", date_match.group())
