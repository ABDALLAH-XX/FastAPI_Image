from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse # <--- Pour renvoyer l'image
from PIL import Image
import io

app = FastAPI()

@app.post("/image-grayscale/")
async def make_grayscale(file: UploadFile = File(...)):
    # 1. Lire l'image uploadée
    content = await file.read()
    img = Image.open(io.BytesIO(content))
    
    # 2. Traitement : Convertir en Noir et Blanc (mode 'L')
    img_gray = img.convert("L")
    
    # 3. Préparer le flux de sortie pour renvoyer l'image
    img_buffer = io.BytesIO()
    # On sauvegarde dans le buffer au format PNG par exemple
    img_gray.save(img_buffer, format="PNG")
    img_buffer.seek(0) # On remet le curseur au début pour la lecture
    
    return StreamingResponse(img_buffer, media_type="image/png")