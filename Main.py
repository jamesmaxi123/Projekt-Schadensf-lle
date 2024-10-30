from PIL import Image
import pytesseract
import cv2

# Testbild laden
image_path = '/Users/MaxiRo/Desktop/ATIW/5 Block/Projekt Schadensfälle/schadensmeldungsformular_x.png'  # Ersetzen Sie dies durch den Pfad zu einem Testbild
image = Image.open(image_path)

# OCR auf das Bild anwenden
text = pytesseract.image_to_string(image, lang='deu')  # 'deu' für Deutsch, 'eng' für Englisch
print("Erkannter Text:\n", text)

