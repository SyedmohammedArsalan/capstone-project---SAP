# recommend.py

import requests
import base64
import numpy as np
from PIL import Image
from colorthief import ColorThief
from io import BytesIO

HF_TOKEN = "your_huggingface_api_token_here"  # Replace with your actual token

# Personalized Recommendation Engine
def get_personalized_recommendations(prefs, style_filter=None, price_range=None):
    query = {
        "styles": prefs.styles,
        "colors": prefs.colors,
        "budget": prefs.budget,
        "history": prefs.get_history()
    }

    response = requests.post(
        "https://api.example.com/recommend",
        json=query,
        headers={"Authorization": f"Bearer {HF_TOKEN}"}
    )

    return response.json().get('results', [])

# Color Palette Generator
def get_color_palette(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    ct = ColorThief(buffer)
    palette = ct.get_palette(color_count=5)

    palette_img = Image.new('RGB', (300, 50))
    x = 0
    for color in palette:
        palette_img.paste(color, (x, 0, x+60, 50))
        x += 60

    return palette_img

# Virtual Try-On Integration
def virtual_try_on(user_image, garment_image):
    user_b64 = image_to_base64(user_image)
    garment_b64 = image_to_base64(garment_image)

    response = requests.post(
        "https://api-inference.huggingface.co/models/viton-hd",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"user": user_b64, "garment": garment_b64}
    )

    return Image.open(BytesIO(response.content))

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Item Description Generator
def get_item_description(item):
    category = item.get('category', 'item')
    color = item.get('color', 'a unique color')
    style = item.get('style', 'modern')
    price = item.get('price', 'N/A')

    return f"A {style} {category} in {color}, priced at ${price}."

# Style Feedback Generator
def get_style_feedback(style_profile):
    """
    Provide feedback based on the user's style profile.
    Example: Highlight consistency, versatility, or areas to explore.
    """
    feedback = []

    if not style_profile:
        return "No style profile provided."

    if "minimalist" in style_profile:
        feedback.append("You're rocking a clean, minimalist vibe—timeless and versatile.")
    if "bold" in style_profile:
        feedback.append("Bold choices! Don’t be afraid to mix patterns and textures.")
    if "vintage" in style_profile:
        feedback.append("Vintage elements bring personality and charm to your outfits.")

    if not feedback:
        feedback.append("Keep exploring to define your unique style!")

    return " ".join(feedback)
