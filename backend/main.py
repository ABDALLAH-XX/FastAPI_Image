import shutil
from pathlib import Path
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

app = FastAPI(title="PhotoLab API")

# --- CONFIGURATION ---

# Autoriser le futur Frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Indispensable pour que React puisse parler à FastAPI
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
PROCESSED_DIR = BASE_DIR / "processed"

UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

# Permettre au navigateur d'afficher les images : http://127.0.0.1:8000/static/nom.jpg
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

app.mount("/processed", StaticFiles(directory=PROCESSED_DIR), name="processed")

fake_db = {}

# --- ROUTES ---

@app.get("/images/")
async def list_images():
    # Retourne une liste d'objets (plus facile à traiter pour React)
    return list(fake_db.values())

@app.post("/images/")
async def create_image_info(file: UploadFile = File(...)):
    if not file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="Fichier non supporté.")

    dest_path = UPLOAD_DIR / file.filename

    try:
        with dest_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        with Image.open(dest_path) as img:
            new_id = max(fake_db.keys()) + 1 if fake_db else 1
            
            # Stockage avec URL pour le Frontend
            fake_db[new_id] = {
                "id": new_id,
                "filename": file.filename,
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "url": f"http://127.0.0.1:8000/static/{file.filename}"
            }
            return fake_db[new_id]
            
    except Exception:
        if dest_path.exists(): dest_path.unlink()
        raise HTTPException(status_code=400, detail="Erreur traitement image.")
    
@app.get("/images/{image_id}/process/{action}")
async def process_image(image_id: int, action: str):
    # 1. Vérifier si l'image existe dans la DB
    if image_id not in fake_db:
        raise HTTPException(status_code=404, detail="Image non trouvée")
    
    img_info = fake_db[image_id]
    input_path = UPLOAD_DIR / img_info["filename"]
    
    # Nom du nouveau fichier traité
    output_filename = f"{action}_{img_info['filename']}"
    output_path = PROCESSED_DIR / output_filename

    try:
        # 2. Ouvrir avec Pillow
        with Image.open(input_path) as img:
            if action == "grayscale":
                processed_img = img.convert("L")
            elif action == "rotate":
                processed_img = img.rotate(90, expand=True)
            else:
                raise HTTPException(status_code=400, detail="Action inconnue")

            # 3. Sauvegarder sur le disque Ubuntu
            processed_img.save(output_path)
            
        # 4. Retourner l'URL de l'image traitée
        return {
            "message": f"Traitement {action} réussi",
            "url_processed": f"http://127.0.0.1:8000/processed/{output_filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de traitement : {str(e)}")

@app.delete("/images/{image_id}")
async def delete_image(image_id: int):
    if image_id not in fake_db:
        raise HTTPException(status_code=404, detail="Image non trouvée")

    # 1. SUPPRESSION PHYSIQUE
    filename = fake_db[image_id]["filename"]
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        file_path.unlink() # Supprime le fichier sur Ubuntu

    # 2. SUPPRESSION DB
    del fake_db[image_id]
    return {"message": f"Image {image_id} supprimée du disque et de la DB"}