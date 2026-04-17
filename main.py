from fastapi import FastAPI, HTTPException, File, UploadFile
from PIL import Image
import io

app = FastAPI()

# Notre base de données temporaire (s'efface si tu redémarres uvicorn)
fake_db = {
    1: {"filename": "vacances.jpg", "width": 1920, "height": 1080},
    2: {"filename": "logo.png", "width": 500, "height": 500}
}

# GET : Récupérer TOUS les éléments
@app.get("/images/")
async def list_images():
    return fake_db

# GET : Récupérer UN élément par son ID (Path Parameter)
@app.get("/images/{image_id}")
async def get_image_info(image_id: int):
    if image_id not in fake_db:
        raise HTTPException(status_code=404, detail="Image non trouvée")
    return fake_db[image_id]

@app.post("/images/") # On change le chemin pour être cohérent avec le GET
async def create_image_info(file: UploadFile = File(...)):
    # VALIDATION : Est-ce que c'est une image ? 
    if not file.content_type.startswith("image"):
        raise HTTPException(
            status_code=400,
            detail=f"Fichier non supporté ({file.content_type}). Veuillez envoyer un image."
        )

    # Si c'est bon on continue le traitement

    content = await file.read()

    try:
        img = Image.open(io.BytesIO(content))
    
        # Générer un nouvel ID
        new_id = max(fake_db.keys()) + 1 if fake_db else 1
    
        # AJOUT DANS LA DB
        fake_db[new_id] = {
            "filename": file.filename,
            "width": img.width,
            "height": img.height,
            "format": img.format
        }
    except Exception:
        # Au cas où le fichier a une expression d'image mais est corrompu
        raise HTTPException(status_code=400, detail="Image corrompue ou illisible")
    
    return {"message": "Image ajoutée", "id": new_id}

# DELETE : Supprimer un élément
@app.delete("/images/{image_id}")
async def delete_image(image_id: int):
    if image_id in fake_db:
        del fake_db[image_id]
        return {"message": f"Image {image_id} supprimée"}
    raise HTTPException(status_code=404, detail="Image non trouvée")