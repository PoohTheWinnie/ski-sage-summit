import os
from pathlib import Path

# Define paths to your data directories
DATA_DIR = Path(__file__).parent
SKI_MAPS_DIR = DATA_DIR / "maps"
SKI_TEXTS_DIR = DATA_DIR / "texts"

# Configuration for different ski resorts' maps
SKI_MAPS = {
    "whistler": {
        "path": SKI_MAPS_DIR / "whistler.png",
        "metadata": {
            "resort_name": "Whistler Blackcomb",
            "location": "British Columbia, Canada",
            "vertical_drop": "1,530 meters",
            "total_runs": 200
        }
    },
    "vail": {
        "path": SKI_MAPS_DIR / "vail.png",
        "metadata": {
            "resort_name": "Vail",
            "location": "Colorado, USA",
            "vertical_drop": "1,127 meters",
            "total_runs": 195
        }
    },
    # Add more resorts as needed
}

# Configuration for ski encyclopedia texts
SKI_TEXTS = {
    "technique": {
        "path": SKI_TEXTS_DIR / "ski_technique.txt",
        "metadata": {
            "category": "Technique",
            "topics": ["carving", "parallel turns", "moguls", "powder skiing"]
        }
    },
    "equipment": {
        "path": SKI_TEXTS_DIR / "ski_equipment.txt",
        "metadata": {
            "category": "Equipment",
            "topics": ["skis", "boots", "bindings", "poles", "maintenance"]
        }
    },
    # Add more text categories as needed
} 