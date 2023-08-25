import zipfile
from pprint import pprint
from typing import List

from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io
import os

from starlette.responses import FileResponse

app = FastAPI()

UPLOAD_FOLDER = "uploaded_images"
COMPRESSED_FOLDER = "compressed_images"
ZIP_FOLDER = "zip_files"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)
os.makedirs(ZIP_FOLDER, exist_ok=True)


@app.post("/upload/")
async def upload_and_compress_images(file_dir: str, files: List[UploadFile] = File(...)):
    compressed_file_paths = []

    if not os.path.exists(F"{COMPRESSED_FOLDER}/{file_dir}"):
        os.makedirs(F"{COMPRESSED_FOLDER}/{file_dir}", exist_ok=True)

    for file in files:
        # Read the uploaded image
        image = Image.open(file.file)

        # Convert to RGB mode if image is in RGBA mode
        if image.mode == "RGBA":
            image = image.convert("RGB")

        # Compress the image
        compressed_image = compress_image(image, max_size=1024)  # Maximum size in KB (1MB)

        # Save the compressed image to a file
        pprint(compressed_image)
        compressed_file_path = os.path.join(f"{COMPRESSED_FOLDER}/{file_dir}", file.filename)
        compressed_image.save(compressed_file_path, format="JPEG", quality=85)
        compressed_file_paths.append(compressed_file_path)

    return compressed_file_paths


def compress_image(image, max_size):
    # Reduce the quality of the image until its size is below the desired limit
    while True:
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85)  # Adjust quality as needed
        buffer_size = len(buffer.getvalue())

        if buffer_size <= max_size * 1024:  # Convert max_size to bytes
            break

        # Reduce quality further
        image = image.resize((int(image.width * 0.9), int(image.height * 0.9)))

    return image


@app.get("/download_zip/")
async def download_zip(file_dir: str):
    zip_file_path = os.path.join(ZIP_FOLDER, "compressed_images.zip")

    # Create a zip archive containing all compressed images
    with zipfile.ZipFile(zip_file_path, "w") as zipf:
        for root, _, files in os.walk(F"{COMPRESSED_FOLDER}/{file_dir}"):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, F"{COMPRESSED_FOLDER}/{file_dir}"))

    return FileResponse(zip_file_path, filename="compressed_images.zip")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
