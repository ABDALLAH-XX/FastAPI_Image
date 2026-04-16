from fastapi import FastAPI, HTTPException

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

# DELETE : Supprimer un élément
@app.delete("/images/{image_id}")
async def delete_image(image_id: int):
    if image_id in fake_db:
        del fake_db[image_id]
        return {"message": f"Image {image_id} supprimée"}
    raise HTTPException(status_code=404, detail="Image non trouvée")