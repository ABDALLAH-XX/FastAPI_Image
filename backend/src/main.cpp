#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>

int main(int argc, char** argv) {
    // 1. Vérification des arguments
    if (argc < 4) {
        std::cout << "Usage: " << argv[0] << " <input_image> <output_image> <action: gray|rotate90>" << std::endl;
        return -1;
    }

    std::string inputPath = argv[1];
    std::string outputPath = argv[2];
    std::string action = argv[3];

    // 2. Chargement de l'image
    cv::Mat image = cv::imread(inputPath, cv::IMREAD_COLOR);
    if (image.empty()) {
        std::cerr << "Erreur: Impossible de charger l'image." << std::endl;
        return -1;
    }

    cv::Mat result;

    // 3. Logique de traitement
    if (action == "gray") {
        // Conversion en niveaux de gris
        cv::cvtColor(image, result, cv::COLOR_BGR2GRAY);
        std::cout << "Conversion en niveaux de gris terminée." << std::endl;
    } 
    else if (action == "rotate90") {
        // Rotation de 90 degrés (sens horaire)
        cv::rotate(image, result, cv::ROTATE_90_CLOCKWISE);
        std::cout << "Rotation 90° terminée." << std::endl;
    } 
    else {
        std::cerr << "Action inconnue: " << action << std::endl;
        return -1;
    }

    // 4. Sauvegarde du résultat
    if (cv::imwrite(outputPath, result)) {
        std::cout << "Image sauvegardée avec succès: " << outputPath << std::endl;
    } else {
        std::cerr << "Erreur lors de la sauvegarde." << std::endl;
        return -1;
    }

    return 0;
}