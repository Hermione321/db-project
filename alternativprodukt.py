"""
alternativprodukt.py

Beschreibung:
-------------
Dieses Python-Programm ermöglicht es, anhand eines gegebenen Strichcodes das zugehörige Produkt zu identifizieren
und eine umweltfreundlichere Alternative vorzuschlagen. Ziel des Programms ist es, den Benutzer dabei zu unterstützen,
Produkte zu wählen, die einfacher und ressourcenschonender entsorgt bzw. recycelt werden können.

Funktionsweise:
---------------
1. Eingabe: Ein Strichcode (als String) wird eingegeben.
2. Produkterkennung: Das Programm sucht in der Datenbasis (CATEGORIES & BARCODES) das passende Produkt.
3. Umweltfreundliche Bewertung: Jedes Produkt besteht aus verschiedenen Materialien (PET, Aluminium, Glas, Papier).
   Die Umweltfreundlichkeit wird anhand der Anzahl der Materialien bestimmt – je weniger Materialien vorhanden,
   desto leichter ist das Produkt zu entsorgen.
4. Vorschlag einer Alternative: Das Programm sucht andere Produkte aus der Datenbasis, die weniger Materialien enthalten
   und somit umweltfreundlicher sind, und gibt die beste Alternative zurück.

Datenbasis:
-----------
- CATEGORIES: Enthält alle Produkte mit den enthaltenen Materialien und deren Farbcodierung.
- BARCODES: Enthält die Zuordnung von Strichcodes zu Produktnamen.

Funktionen:
-----------
- material_count(product_name): Zählt, wie viele Materialien im Produkt enthalten sind.
- find_alternative_text(barcode): Gibt eine textuelle Auswertung zurück, inklusive Produktname, Materialanzahl
  und umweltfreundlicherer Alternative.

Verwendung:
-----------
- Direkt über die Konsole: python alternativprodukt.py
- Integration in eine Weboberfläche (z. B. über FastAPI) möglich, wobei die Funktion find_alternative_text
  die Ergebnisse als Text zurückliefert.

Beispiel:
---------
Eingabe: "1234567890123"
Ausgabe:
📦 Produkt erkannt: Papier
♻️ Materialanzahl: 3
🌱 Umweltfreundlichere Alternative: PET-Flasche (Materialanzahl: 1)

"""
from categories import CATEGORIES, BARCODES

def material_count(product_name: str) -> int:
    """Zählt die Anzahl enthaltener Materialien eines Produkts."""
    return sum(material["present"] for material in CATEGORIES[product_name])

def find_alternative_text(barcode: str) -> str:
    """Ermittelt das Produkt und gibt eine textuelle umweltfreundliche Alternative zurück."""
    if barcode not in BARCODES:
        return "❌ Unbekannter Barcode"

    current_product = BARCODES[barcode]
    current_score = material_count(current_product)

    result = f"📦 Produkt erkannt: {current_product}\n♻️ Materialanzahl: {current_score}\n"

    alternatives = []
    for product in CATEGORIES:
        if product != current_product:
            score = material_count(product)
            if score < current_score:
                alternatives.append((product, score))

    if not alternatives:
        result += "✅ Dieses Produkt ist bereits sehr umweltfreundlich."
        return result

    best_alternative = alternatives[0]
    for alternative in alternatives:
        if alternative[1] < best_alternative[1]:
            best_alternative = alternative

    result += f"🌱 Umweltfreundlichere Alternative: {best_alternative[0]} (Materialanzahl: {best_alternative[1]})"

    return result

if __name__ == "__main__":
    barcode_input = input("Bitte Strichcode eingeben: ")
    print(find_alternative_text(barcode_input))
