from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de traitement d'image !"}

@app.post("/image-info/")
async def get_image_info(file: UploadFile = File(...)):
    # 1. Lire le contenu du fichier uploadé
    request_object_content = await file.read()
    
    # 2. Ouvrir l'image avec Pillow
    img = Image.open(io.BytesIO(request_object_content))
    
    # 3. Extraire les infos
    return {
        "filename": file.filename,
        "format": img.format,
        "mode": img.mode,
        "width": img.width,
        "height": img.height
    }