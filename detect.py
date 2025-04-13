from transformers import pipeline
from PIL import Image

# Initialize Detector
detector = pipeline(
    "object-detection",
    model="facebook/detr-resnet-50",
    device_map="auto"
)

def detect_clothes(image):
    """Detect clothing items with enhanced accuracy"""
    results = detector(image)
    
    detected_items = []
    for result in results:
        if result['label'] in ['shirt', 'dress', 'pants', 'shoe']:
            detected_items.append({
                "label": result['label'],
                "score": result['score'],
                "box": result['box'],
                "image": image.crop((
                    result['box']['xmin'],
                    result['box']['ymin'],
                    result['box']['xmax'],
                    result['box']['ymax']
                ))
            })
    
    return detected_items