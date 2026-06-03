import os
import io
import numpy as np
import cv2
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import mon_traitement  # Importation de votre main.cpp compilé via pybind11

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration des dossiers (on les garde pour vos routes GET /files et /image)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process/")
async def process_image(
    action: str, 
    file: UploadFile = File(...),
    threshold_value: int = Form(127) # Reçu depuis le curseur React (Ignoré si action != threshold)
):
    # 1. Validation de l'action
    if action not in ["gray", "rotate90", "threshold"]:
        raise HTTPException(status_code=400, detail="L'action demandée n'est pas supportée.")
    
    name, ext = os.path.splitext(file.filename)
    input_path = os.path.join(UPLOAD_DIR, f"{file.filename}")
    output_path = os.path.join(UPLOAD_DIR, f"{name}_{action}{ext}")

    try:
        # 2. Lecture du fichier en mémoire (RAM)
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Fichier image invalide ou corrompu.")

        # Optionnel : Sauvegarder l'image originale sur le disque comme avant
        with open(input_path, "wb") as buffer:
            buffer.write(contents)

        # 3. APPEL DU CODE C++ EN MÉMOIRE (Fini subprocess !)
        if action == "gray":
            img_processed = mon_traitement.to_grayscale(img)
        elif action == "rotate90":
            img_processed = mon_traitement.rotate_90(img)
        elif action == "threshold":
            img_processed = mon_traitement.apply_threshold(img, threshold_value)

        # 4. Sauvegarde du résultat sur le disque (Pour que vos routes GET restent fonctionnelles)
        # OpenCV choisit automatiquement le format d'écriture en fonction de l'extension (ex: .png ou .jpg)
        cv2.imwrite(output_path, img_processed)
        
        # 5. Renvoi du fichier traité au client React
        return FileResponse(output_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de traitement : {str(e)}")
    

@app.get("/files")
async def list_files():
    # Liste tous les fichiers dans le dossier uploads
    files = os.listdir(UPLOAD_DIR)
    return {"count": len(files), "files": files}


@app.get("/image/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Vérification pour éviter un crash du serveur
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    raise HTTPException(status_code=404, detail="Image non trouvée")


@app.get("/health")
async def health_check():
    # On vérifie si le module C++ est bien chargé à la place du binaire autonome
    try:
        import mon_traitement
        binding_ok = True
    except ImportError:
        binding_ok = False

    return {
        "status": "online",
        "c++_binding_loaded": binding_ok,
        "opencv_support": True
    }