#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <opencv2/opencv.hpp>

namespace py = pybind11;

// Fonction utilitaire pour convertir un tableau NumPy 2D ou 3D en cv::Mat (Sans copie)
cv::Mat numpy_to_mat(py::array_t<uint8_t>& input_image) {
    py::buffer_info buf = input_image.request();
    int rows = buf.shape[0];
    int cols = buf.shape[1];
    
    if (buf.ndim == 3) { // Image couleur (BGR)
        int channels = buf.shape[2];
        return cv::Mat(rows, cols, CV_8UC(channels), (uint8_t*)buf.ptr);
    } else { // Image en niveaux de gris
        return cv::Mat(rows, cols, CV_8UC1, (uint8_t*)buf.ptr);
    }
}

// Fonction utilitaire pour convertir une cv::Mat en tableau NumPy (Avec copie pour la sécurité)
py::array_t<uint8_t> mat_to_numpy(const cv::Mat& mat) {
    std::vector<ptrdiff_t> shape;
    std::vector<ptrdiff_t> strides;
    
    if (mat.channels() == 3) {
        shape = { mat.rows, mat.cols, 3 };
        strides = { mat.step[0], mat.step[1], 1 };
    } else {
        shape = { mat.rows, mat.cols };
        strides = { mat.step[0], mat.step[1] };
    }
    
    auto result = py::array_t<uint8_t>(shape, strides);
    py::buffer_info buf_res = result.request();
    std::memcpy(buf_res.ptr, mat.data, mat.total() * mat.elemSize());
    return result;
}

// 1. Action : Niveaux de gris
py::array_t<uint8_t> to_grayscale(py::array_t<uint8_t> input_image) {
    cv::Mat image = numpy_to_mat(input_image);
    cv::Mat result;
    cv::cvtColor(image, result, cv::COLOR_BGR2GRAY);
    return mat_to_numpy(result);
}

// 2. Action : Rotation 90°
py::array_t<uint8_t> rotate_90(py::array_t<uint8_t> input_image) {
    cv::Mat image = numpy_to_mat(input_image);
    cv::Mat result;
    cv::rotate(image, result, cv::ROTATE_90_CLOCKWISE);
    return mat_to_numpy(result);
}

// 3. Action : Seuil binaire (Threshold)
py::array_t<uint8_t> apply_threshold(py::array_t<uint8_t> input_image, int threshold_val) {
    cv::Mat image = numpy_to_mat(input_image);
    cv::Mat result;
    // On s'assure que l'image est en gris avant le seuillage
    if (image.channels() == 3) {
        cv::cvtColor(image, image, cv::COLOR_BGR2GRAY);
    }
    cv::threshold(image, result, threshold_val, 255, cv::THRESH_BINARY);
    return mat_to_numpy(result);
}

// Déclaration du module pour Python
PYBIND11_MODULE(mon_traitement, m) {
    m.def("to_grayscale", &to_grayscale, "Convertit l'image en niveaux de gris");
    m.def("rotate_90", &rotate_90, "Pivote l'image à 90 degrés");
    m.def("apply_threshold", &apply_threshold, "Applique un seuil binaire");
}