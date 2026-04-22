cmake_minimum_required(VERSION 3.10)
project(FastAPI_Image_Backend)

# Standard C++
set(CMAKE_CXX_STANDARD 17)

# Recherche d'OpenCV
find_package(OpenCV REQUIRED)

# Définition de l'exécutable
add_executable(image_processor src/main.cpp)

# Lien avec les bibliothèques OpenCV
target_link_libraries(image_processor ${OpenCV_LIBS})