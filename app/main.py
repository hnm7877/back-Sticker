from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
import zipfile
from typing import List

from app.services.image_service import apply_watermark_to_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/watermark-images/")
async def watermark_images(
    images: List[UploadFile] = File(...), 
    watermark: UploadFile = File(...),
):
    watermark_file = Image.open(watermark.file)
    
    # Create a BytesIO object to store the zip file in memory
    zip_buffer = BytesIO()

    # Create the zip archive in memory
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
        for idx, image in enumerate(images):
            image_file = Image.open(image.file)
            
            # Apply the watermark to each image
            watermarked_image = apply_watermark_to_image(image_file, watermark_file, position=(100, 100), size=(150, 150))

            # Save the watermarked image to a BytesIO buffer
            image_io = BytesIO()
            image_format = image.filename.split('.')[-1].upper()
            if image_format == "JPG":
                image_format = "JPEG"
            if image_format not in ['JPEG', 'PNG']:
                image_format = 'JPEG'
            watermarked_image.save(image_io, format=image_format)
            image_io.seek(0)

            # Add the image to the zip archive
            zip_archive.writestr(f"watermarked_image_{idx + 1}.{image_format.lower()}", image_io.getvalue())

    # Ensure the pointer is at the beginning of the buffer
    zip_buffer.seek(0)

    # Return the zip file as a StreamingResponse
    return StreamingResponse(
        zip_buffer, 
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": "attachment; filename=watermarked_images.zip"}
    )
