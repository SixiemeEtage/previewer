import cv2
import numpy as np
from PIL import Image

import libpreviewer


def clip(v, minv, maxv):
    return max(min(v, maxv), minv)


class BaseGenerator(object):

    def _setup(self, image_size, fov=50.0, latitude=0.0, longitude=0.0, preview_size=(1000, 750)):
        self.image_size = map(int, image_size)
        self.image_w2 = image_size[0] / 2
        self.image_h2 = image_size[1] / 2

        self._scale = self.image_w2 / np.math.pi
        self._fov = fov

        # NB: Force int casting since having floats here would fail with the C++ bindings.
        self.preview_size = map(int, preview_size)
        self.preview_w2 = preview_size[0] / 2
        self.preview_h2 = preview_size[1] / 2

        # rotation corresponding to the preview being generated
        # R = np.eye(3)
        lat_rad = -1.0 * latitude / 180.0 * np.pi
        lng_rad = -1.0 * longitude / 180.0 * np.pi
        Rx = np.array([
            [1,0,0],
            [0, np.math.cos(lat_rad), -np.math.sin(lat_rad)],
            [0, np.math.sin(lat_rad), np.math.cos(lat_rad)]
        ])
        Ry = np.array([
            [np.math.cos(lng_rad), 0, -np.math.sin(lng_rad)],
            [0, 1, 0],
            [np.math.sin(lng_rad), 0, np.math.cos(lng_rad)]
        ])
        R = np.dot(Ry, Rx)

        # intrinsic matrix for the projection
        # fov_dimension = max(*self.preview_size)
        fov_dimension = self.preview_size[1]
        fov_rad = float(fov) / 180 * np.pi
        fx = fy = (fov_dimension / 2) / np.math.tan(fov_rad / 2)
        ppx = preview_size[0] / 2
        ppy = preview_size[1] / 2
        K = np.array((fx, 0, ppx, 0, fy, ppy, 0, 0, 1)).reshape((3,3))

        # build the `R * Kinv` transform matrix
        Kinv = np.linalg.inv(K)
        self.R_Kinv = np.dot(R, Kinv)

    def _input_optimal_size(self):
        """NB: The fov determines the vertical fov of the output"""
        height = float(180) / self._fov * self.preview_size[1]
        height = min(height, self.image_size[1])  # bound the image height
        width = float(self.image_size[0]) / self.image_size[1] * height
        return tuple(map(int, (width, height)))

    def _map_backward(self, x, y):
        """Map backward the final preview image pixel (x,y) to the 
        original equirectangular coords (u,v)"""
        x_ = self.R_Kinv.item(0) * x + self.R_Kinv.item(1) * y + self.R_Kinv.item(2)
        y_ = self.R_Kinv.item(3) * x + self.R_Kinv.item(4) * y + self.R_Kinv.item(5)
        z_ = self.R_Kinv.item(6) * x + self.R_Kinv.item(7) * y + self.R_Kinv.item(8)

        # project on a spherical map
        u = self._scale * np.math.atan2(x_, z_) + self.image_w2
        v = self._scale * ((np.math.pi / 2) - np.math.acos(y_ / np.math.sqrt(x_ * x_ + + y_ * y_ + z_ * z_))) + self.image_h2

        return (u,v)

    def generate(self):
        raise NotImplementedError


class PreviewNativeProcessor(BaseGenerator):

    def __init__(self, image_path, **kwargs):
        self.image = Image.open(image_path)
        self._setup(self.image.size, **kwargs)

    def _bilinear_interpolation(self, xy):
        """Bilinear implementation"""
        im = self.image
        x,y = xy

        x0 = np.math.floor(x)
        x1 = x0 + 1
        y0 = np.math.floor(y)
        y1 = y0 + 1

        x0 = clip(x0, 0, im.size[0] - 1)
        x1 = clip(x1, 0, im.size[0] - 1)
        y0 = clip(y0, 0, im.size[1] - 1)
        y1 = clip(y1, 0, im.size[1] - 1)

        Ia = np.array(im.getpixel((x0, y0)))
        Ib = np.array(im.getpixel((x0, y1)))
        Ic = np.array(im.getpixel((x1, y0)))
        Id = np.array(im.getpixel((x1, y1)))

        wa = (x1 - x) * (y1 - y)
        wb = (x1 - x) * (y - y0)
        wc = (x - x0) * (y1 - y)
        wd = (x - x0) * (y - y0)

        return tuple(np.rint(wa * Ia + wb * Ib + wc * Ic + wd * Id).astype(int))

    def generate(self):
        """Generate the preview"""
        im = self.image
        out = Image.new(im.mode, self.preview_size)
        for x in xrange(self.preview_size[0]):
            for y in xrange(self.preview_size[1]):
                uv = self._map_backward(x, y)
                pix = self._bilinear_interpolation(uv)
                out.putpixel((x,y), pix)
        return out


class PreviewOpenCVProcessor(BaseGenerator):

    def __init__(self, image_path, **kwargs):
        self.image = cv2.imread(image_path)
        image_size = (self.image.shape[1], self.image.shape[0])
        self._setup(image_size, **kwargs)

    def generate(self):
        """Generate the preview"""
        # first we resize the input image
        # so that the remaping step produce a nice image
        optimal_size = self._input_optimal_size()
        if optimal_size != self.image_size:
            resized_image = cv2.resize(self.image, optimal_size)
        else:
            resized_image = self.image

        # build the remaping maps
        P = libpreviewer.Projector(
            optimal_size[0],
            optimal_size[1],
            self.preview_size[0],
            self.preview_size[1],
            self.R_Kinv
        )
        P.unproject()
        map_x = P.get_map_x()
        map_y = P.get_map_y()

        out = cv2.remap(resized_image, map_x, map_y, cv2.INTER_LANCZOS4)
        return out
