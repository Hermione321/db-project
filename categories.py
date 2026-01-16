CATEGORIES = {
    "PET-Flasche": {
        "description": "PET besteht aus Plastik. Es braucht sehr lange zum Zersetzen und kann Mikroplastik in die Umwelt abgeben.",
        "co2": "ca. 80g CO₂ pro Flasche",
        "points": 5,
        "tip": "Flasche zusammendrücken und Deckel drauflassen.",
        "score": 3,
        "materials": [
            {"name": "PET", "color": "#1e90ff", "present": True},
            {"name": "Aluminium", "color": "#f1c40f", "present": False},
            {"name": "Glas", "color": "#27ae60", "present": False},
            {"name": "Papier", "color": "#8e6e53", "present": False}
        ]
    },

    "Glasflasche": {
        "description": "Glas ist sehr gut recycelbar, aber schwer beim Transport.",
        "co2": "ca. 150g CO₂",
        "points": 3,
        "tip": "Nach Farben sortieren (weiß, grün, braun).",
        "score": 4,
        "materials": [
            {"name": "PET", "color": "#1e90ff", "present": False},
            {"name": "Aluminium", "color": "#f1c40f", "present": False},
            {"name": "Glas", "color": "#27ae60", "present": True},
            {"name": "Papier", "color": "#8e6e53", "present": True}
        ]
    },

    "Aluminiumdose": {
        "description": "Aluminiumherstellung ist sehr energieintensiv.",
        "co2": "ca. 170g CO₂",
        "points": 2,
        "tip": "Dose zusammendrücken spart Platz.",
        "score": 2,
        "materials": [
            {"name": "PET", "color": "#1e90ff", "present": False},
            {"name": "Aluminium", "color": "#f1c40f", "present": True},
            {"name": "Glas", "color": "#27ae60", "present": False},
            {"name": "Papier", "color": "#8e6e53", "present": True}
        ]
    },

    "Tetrapack": {
        "description": "Besteht aus mehreren Schichten – schwer zu recyceln.",
        "co2": "ca. 90g CO₂",
        "points": 1,
        "tip": "Ausspülen & flach drücken.",
        "score": 1,
        "materials": [
            {"name": "PET", "color": "#1e90ff", "present": True},
            {"name": "Aluminium", "color": "#f1c40f", "present": True},
            {"name": "Glas", "color": "#27ae60", "present": False},
            {"name": "Papier", "color": "#8e6e53", "present": True}
        ]
    }
}

BARCODES = {
    "7612345678901": "PET-Flasche",
    "4001234567890": "Aluminiumdose",
    "5009876543210": "Glasflasche",
    "1234567890123": "Tetrapack"
}
