#define PY_ARRAY_UNIQUE_SYMBOL pbcvt_ARRAY_API

#include <iostream>
#include <boost/python.hpp>
#include <pyboostcvconverter/pyboostcvconverter.hpp>

namespace projector {

    using namespace boost::python;

    std::ostream& operator<<(std::ostream& os, const boost::python::object& o) {
        return os << boost::python::extract<std::string>(boost::python::str(o))();
    }

    class Projector {
    private:
        double scale;
        double imageMidWidth;
        double imageMidHeight;
        int previewWidth;
        int previewHeight;
        cv::Mat R_Kinv;
        cv::Mat mapX;
        cv::Mat mapY;

        /**
         * Map backward the final preview image pixel (x,y) to the 
         * original equirectangular coords (u,v)
         */
        void mapBackward(double x, double y, double& u, double& v) {
            double x_ = R_Kinv.at<double>(0,0) * x + R_Kinv.at<double>(0,1) * y + R_Kinv.at<double>(0,2);
            double y_ = R_Kinv.at<double>(1,0) * x + R_Kinv.at<double>(1,1) * y + R_Kinv.at<double>(1,2);
            double z_ = R_Kinv.at<double>(2,0) * x + R_Kinv.at<double>(2,1) * y + R_Kinv.at<double>(2,2);

            // project on a spherical map

            // DEBUG
            // std::cout << "(x,y,z) = " << "(" << x_ << ", " << y_ << ", " << z_ << ")" << std::endl;
            // ENDDEBUG

            u = scale * atan2f(x_, z_) + imageMidWidth;
            v = scale * ((M_PI / 2.0) - acosf(y_ / sqrtf(x_ * x_ + y_ * y_ + z_ * z_))) + imageMidHeight;
        }

    public:
        Projector(int _imageWidth, int _imageHeight, int _previewWidth, int _previewHeight, cv::Mat _R_Kinv) : 
            imageMidWidth(static_cast<double>(_imageWidth)/2),
            imageMidHeight(static_cast<double>(_imageHeight)/2),
            previewWidth(_previewWidth),
            previewHeight(_previewHeight),
            R_Kinv(_R_Kinv) {
                scale = imageMidWidth / M_PI;

                // DEBUG
                // std::cout << std::endl;
                // std::cout << "scale = " << scale << std::endl;
                // std::cout << "R_Kinv[0] = " << R_Kinv.at<double>(0,0) << ", " << R_Kinv.at<double>(0,1) << ", " << R_Kinv.at<double>(0,2) << std::endl;
                // std::cout << "R_Kinv[1] = " << R_Kinv.at<double>(1,0) << ", " << R_Kinv.at<double>(1,1) << ", " << R_Kinv.at<double>(1,2) << std::endl;
                // std::cout << "R_Kinv[2] = " << R_Kinv.at<double>(2,0) << ", " << R_Kinv.at<double>(2,1) << ", " << R_Kinv.at<double>(2,2) << std::endl;
                // std::cout << std::endl;
                // ENDDEBUG
            }

        cv::Mat get_map_x() const { return mapX; }
        cv::Mat get_map_y() const { return mapY; }

        void unproject() {
            mapX = cv::Mat(previewHeight, previewWidth, CV_32FC1);
            mapY = cv::Mat(previewHeight, previewWidth, CV_32FC1);

            for (int x = 0; x < previewWidth; ++x) {
                for (int y = 0; y < previewHeight; ++y) {
                    double u,v;
                    mapBackward(static_cast<double>(x), static_cast<double>(y), u, v);
                    // std::cout << "u,v = " << u << "," << v << std::endl;
                    mapX.at<float>(y,x) = static_cast<float>(u);
                    mapY.at<float>(y,x) = static_cast<float>(v);
                }
            }
        }
    };

    /**
     * Unproject. Basic inner matrix product using implicit matrix conversion.
     * @param leftMat left-hand matrix operand
     * @param rightMat right-hand matrix operand
     * @return an NdArray representing the dot-product of the left and right operands
     */
    // cv::Mat unproject(cv::Mat leftMat, cv::Mat rightMat) {
    //     auto c1 = leftMat.cols, r2 = rightMat.rows;
    //     if (c1 != r2) {
    //         PyErr_SetString(PyExc_TypeError,
    //                         "Incompatible sizes for matrix multiplication.");
    //         throw_error_already_set();
    //     }
    //     cv::Mat result = leftMat * rightMat;

    //     return result;
    // }


#if (PY_VERSION_HEX >= 0x03000000)
    static void *init_ar() {
#else
    static void init_ar(){
#endif
        Py_Initialize();

        import_array();
        return NUMPY_IMPORT_ARRAY_RETVAL;
    }

    BOOST_PYTHON_MODULE (projector) {
        //using namespace XM;
        init_ar();

        //initialize converters
        to_python_converter<cv::Mat, pbcvt::matToNDArrayBoostConverter>();
        pbcvt::matFromNDArrayBoostConverter();

        //expose module-level functions
        class_<Projector>("Projector", init<int, int, int, int, cv::Mat>())
            .def("unproject", &Projector::unproject)
            .def("get_map_x", &Projector::get_map_x)
            .def("get_map_y", &Projector::get_map_y);
    }

} //end namespace projector
