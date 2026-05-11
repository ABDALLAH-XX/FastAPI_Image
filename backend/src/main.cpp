#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>

int main(int argc, char** argv) {
    // 1. Check input arguments
    if (argc < 4) {
        std::cout << "Usage: " << argv[0] << " <input_image> <output_image> <action: gray|rotate90>" << std::endl;
        return -1;
    }

    std::string inputPath = argv[1];
    std::string outputPath = argv[2];
    std::string action = argv[3];

    // 2. LOading the image
    cv::Mat image = cv::imread(inputPath, cv::IMREAD_COLOR);
    if (image.empty()) {
        std::cerr << "Error: Image not found." << std::endl;
        return -1;
    }

    cv::Mat result;

    // 3. Imaghe operation
    if (action == "gray") {
        // Grayscale conversion
        cv::cvtColor(image, result, cv::COLOR_BGR2GRAY);
        std::cout << "Grayscale conversion done." << std::endl;
    } 
    else if (action == "rotate90") {
        // 90° clockwise rotation
        cv::rotate(image, result, cv::ROTATE_90_CLOCKWISE);
        std::cout << "90° Rotation done." << std::endl;
    } 
    else {
        std::cerr << "Unknown action: " << action << std::endl;
        return -1;
    }

    // 4. Save the results on the laptop
    if (cv::imwrite(outputPath, result)) {
        std::cout << "Image saved successfully: " << outputPath << std::endl;
    } else {
        std::cerr << "Error during the save." << std::endl;
        return -1;
    }

    return 0;
}