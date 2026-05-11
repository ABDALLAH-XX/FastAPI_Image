import subprocess
import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path Configuration
UPLOAD_DIR = "uploads"
BINARY_PATH = "./build/image_processor"

@app.post("/process/")
async def process_image(action: str, file: UploadFile = File(...)):
    # 1. Check if the action is valid
    if action not in ["gray", "rotate90"]:
        raise HTTPException(status_code=400, detail="Action is not supported")
    
    # 2. Create unique namefiles to avoid conflicts
    name, ext = os.path.splitext(file.filename)
    input_path = os.path.join(UPLOAD_DIR, f"{file.filename}")
    output_path = os.path.join(UPLOAD_DIR, f"{name}_{action}{ext}")

    # 3. Save the image sent by the user
    try:
        with open(input_path, "wb") as buffer:
            buffer.write(await file.read())

        # 4. CALL C++ BINARY
        # we pass : <input< <output> <action>
        result = subprocess.run(
            [BINARY_PATH, input_path, output_path, action],
            capture_output=True,
            text=True
        )

        # Check if the C++ has sent an error
        if result.returncode != 0:
            raise HTTPException(status_code=500, f="C++ Error: {result.stderr}")
        
        # 5. Send back the image processed to the client
        return FileResponse(output_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/files")
async def list_files():
    # List every files on the uploads folder
    files = os.listdir(UPLOAD_DIR)
    return {"count": len(files), "files": files}

@app.get("/image/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Chekc if the filename exists to prevent crashing the server
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    raise HTTPException(status_code=404, detail="Image not found")

@app.get("/health")
async def health_check():
    binary_exists = os.path.exists(BINARY_PATH)
    return {
        "status": "online",
        "binary_found": binary_exists,
        "opencv_support": True
    }