from PIL import Image
from io import BytesIO

def apply_watermark_to_image(base_image: Image.Image, watermark: Image.Image, position=(0, 0), size=(100, 100)) -> Image.Image:
    # Redimensionner le filigrane
    watermark = watermark.resize(size)

    # Convertir en mode RGBA pour la transparence
    if watermark.mode != 'RGBA':
        watermark = watermark.convert('RGBA')

    # Appliquer le filigrane à l'image de base
    base_image.paste(watermark, position, watermark)

    # Return the modified image as a PIL Image object
    return base_image
