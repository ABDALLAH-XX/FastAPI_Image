# ==========================================
# ÉTAPE 1 : Compilation du module C++
# ==========================================
FROM python:3.10-slim AS builder

WORKDIR /app

# Installation des dépendances système requises pour compiler OpenCV et Pybind11
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopencv-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python standards
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Force l'installation de pybind11 et des outils de build dans le builder
RUN pip install --no-cache-dir pybind11 setuptools wheel

# On recrée la structure exacte : le main.cpp va dans /app/src/
RUN mkdir -p src
COPY backend/src/main.cpp ./src/
COPY backend/setup.py .

# Compilation du binding C++ (.so)
RUN python3 setup.py build_ext --inplace

# ==========================================
# ÉTAPE 2 : Image finale stable
# ==========================================
FROM python:3.10-slim

WORKDIR /app

# On installe les dépendances graphiques ET libopencv-dev pour fournir les .so.410 manquants
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    libgomp1 \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les dépendances Python installées de l'étape précédente
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copier le code de l'application et le module C++ compilé (.so)
COPY backend/ /app/
COPY --from=builder /app/mon_traitement*.so /app/

# Créer le dossier pour les uploads d'images
RUN mkdir -p /app/uploads

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]