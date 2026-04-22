import subprocess
import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En prod, mets l'URL de ton front
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration des chemins
UPLOAD_DIR = "uploads"
BINARY_PATH = "./build/image_processor"

@app.post("/process/")
async def process_image(action: str, file: UploadFile = File(...)):
    # 1. Vérifier si l'action est valide
    if action not in ["gray", "rotate90"]:
        raise HTTPException(status_code=400, detail="Action non supportée")
    
    # 2. Créer des noms de fichiers uniques pour éviter les conflits
    name, ext = os.path.splitext(file.filename)
    input_path = os.path.join(UPLOAD_DIR, f"{file.filename}")
    output_path = os.path.join(UPLOAD_DIR, f"{name}_{action}{ext}")

    # 3. Sauvegarder l'image envoyée par l'utilisateur
    try:
        with open(input_path, "wb") as buffer:
            buffer.write(await file.read())

        # 4. APPEL DU BINAIRE C++ 
        # On passe : <input< <output> <action>
        result = subprocess.run(
            [BINARY_PATH, input_path, output_path, action],
            capture_output=True,
            text=True
        )

        # Vérifier si le C++ a renvoyé une erreur
        if result.returncode != 0:
            raise HTTPException(status_code=500, f="Erreur C++: {result.stderr}")
        
        # 5. Renvoyer l'image traitée au client
        return FileResponse(output_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/files")
async def list_files():
    # Liste tous les fichiers dans le dossier uploads
    files = os.listdir(UPLOAD_DIR)
    return {"count": len(files), "files": files}

@app.get("/image/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Vérifier si le fichier existe pour éviter de faire planter le serveur
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    raise HTTPException(status_code=404, detail="Image non trouvée")

@app.get("/health")
async def health_check():
    binary_exists = os.path.exists(BINARY_PATH)
    return {
        "status": "online",
        "binary_found": binary_exists,
        "opencv_support": True
    }