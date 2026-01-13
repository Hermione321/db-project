CATEGORIES = {
    "PET-Flasche": [
        {"name": "PET", "color": "#1e90ff", "present": True},
        {"name": "Aluminium", "color": "#f1c40f", "present": False},
        {"name": "Glas", "color": "#27ae60", "present": False},
        {"name": "Papier", "color": "#8e6e53", "present": False}
    ],
    "Aluminiumdose": [
        {"name": "PET", "color": "#1e90ff", "present": False},
        {"name": "Aluminium", "color": "#f1c40f", "present": True},
        {"name": "Glas", "color": "#27ae60", "present": False},
        {"name": "Papier", "color": "#8e6e53", "present": True}
    ],
    "Glasflasche": [
        {"name": "PET", "color": "#1e90ff", "present": False},
        {"name": "Aluminium", "color": "#f1c40f", "present": False},
        {"name": "Glas", "color": "#27ae60", "present": True},
        {"name": "Papier", "color": "#8e6e53", "present": True}
    ],
    "Tetrapack": [
        {"name": "PET", "color": "#1e90ff", "present": True},
        {"name": "Aluminium", "color": "#f1c40f", "present": True},
        {"name": "Glas", "color": "#27ae60", "present": False},
        {"name": "Papier", "color": "#8e6e53", "present": True}
    ]
}

BARCODES = {
    "7612345678901": "PET-Flasche",
    "4001234567890": "Aluminiumdose",
    "5009876543210": "Glasflasche",
    "1234567890123": "Tetrapack"
}