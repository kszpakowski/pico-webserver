import json
import random

# JSON data
data = '''
{
  "adjectives": [
    "Bright",
    "Shiny",
    "Warm",
    "Cool",
    "Colorful",
    "Muted",
    "Twinkling",
    "Cozy",
    "Elegant",
    "Modern",
    "Traditional",
    "Subtle",
    "Intense",
    "Harmonious",
    "Vivid",
    "Radiant",
    "Gleaming",
    "Luminous",
    "Soft",
    "Dazzling",
    "Glowing",
    "Flickering",
    "Ambient",
    "Crystalline",
    "Serene",
    "Gentle",
    "Sparkling",
    "Mellow",
    "Golden",
    "Pale",
    "Brilliant"
  ],
  "nouns": [
    "Lamp",
    "Bulb",
    "Spotlight",
    "Lighting",
    "Light",
    "Sconce",
    "Lantern",
    "Fluorescent",
    "Halogen",
    "LED",
    "Gloom",
    "Night",
    "Star",
    "Sun",
    "Moon",
    "Candle",
    "Chandelier",
    "Beacon",
    "Torch",
    "Orb",
    "Glow",
    "Beam",
    "Ray",
    "Flame",
    "Spark",
    "Glowstick",
    "Neon",
    "Phosphor",
    "Radiator",
    "Illumination",
    "Twilight"
  ]
}
'''

# Load JSON data
name_data = json.loads(data)

# Generate a random name
def generate_name():
    adjective = random.choice(name_data['adjectives'])
    noun = random.choice(name_data['nouns'])
    return f"{adjective} {noun}"


