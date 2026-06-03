# 📸 PhotoLab - Computer Vision API & UI

Fullstack application for ultra-fast image management and processing. This version leverages native C++ bindings for real-time performance without disk I/O bottlenecks.

## 🚀 Project Structure
- **Backend**: FastAPI, OpenCV (C++ & Python), Pybind11, NumPy
- **Frontend**: React (Vite)

## 🛠 Installation & Compilation

### 1. Prerequisities (Ubuntu 22.04)
Ensure you have the C++ compiler and OpenCV development libraries installed on your system:
```bash
sudo apt update
sudo apt install build-essential libopencv-dev python3-dev
```

### 2. Backend Setup & C++ Compilation

Navigate to the backend folder, activate your virtual environment, install dependencies, and compile the C++ source code into a native Python module:

```bash
cd backend
pip install -r requirements.txt

# Compile the C++ main.cpp into a native .so module
python3 setup.py build_ext --inplace

# Start the FastAPI server
uvicorn main:app --reload
```

The server will run on `http://127.0.0.1:8000`.


### 3. Frontend Setup

Navigate to the frontend folder and start the Vite development server:
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## 🧪 Features
- In-Memory Processing: Images are processed directly in RAM using C++ and OpenCV, achieving sub-10ms response times.

- Asynchronous Actions:

    - Grayscale conversion.

    - 90° Clockwise rotation.

- Real-time Binary Thresholding: Dynamic slider integration in React with built-in client-side debouncing to prevent API flooding.

- File Management: Image upload with verification and a clean structured history layout (no UI layout shifts/shaking).

- Physical Clean-up: Tracks and stores processed images inside the uploads/ directory.

## 🐳 Docker Deployment

If you prefer to run the backend inside a isolated Docker container without polluting your host system with OpenCV libraries:

```bash
# Build the container (It will automatically compile the C++ bindings inside)
docker build -t photolab-backend .

# Run the container
docker run -p 8000:8000 -v $(pwd)/uploads:/app/uploads photolab-backend