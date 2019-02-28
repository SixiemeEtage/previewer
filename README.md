# previewer

[![build-status-image]][travis]

> Imagination is everything. It is the preview of life's coming attractions.  
> *Albert Einstein*

## Installation

### Install Requirements

```sh
$ brew install opencv3 --with-python
$ brew install boost --with-python
$ brew install boost-python
$ brew link --force opencv3
```

### Install the C++ native lib

```sh
$ git clone https://github.com/SixiemeEtage/previewer
$ cd previewer
$ mkdir -p native/build && cd native/build
$ cmake .. \
    -DCMAKE_C_COMPILER=/usr/bin/gcc \
    -DCMAKE_CXX_COMPILER=/usr/bin/g++ \
    -DPYTHON_DESIRED_VERSION=2.X \
    -DPYTHON2_EXECUTABLE=/usr/local/bin/python \
    -DPYTHON2_LIBRARY=/usr/local/Cellar/python@2/2.7.15_3/Frameworks/Python.framework/Versions/Current/lib/libpython2.7.dylib \
    -DPYTHON2_INCLUDE_DIR=/usr/local/Cellar/python@2/2.7.15_3/Frameworks/Python.framework/Versions/Current/include/python2.7/ \
    -DPYTHON2_NUMPY_INCLUDE_DIRS=/usr/local/Cellar/numpy/1.12.0/lib/python2.7/site-packages/numpy/core/include/ \
    -DBoost_INCLUDE_DIR=/usr/local/Cellar/boost/1.66.0/include/ \
    -DBOOST_LIBRARYDIR=/usr/local/Cellar/boost-python/1.66.0_1/lib
$ make
$ make install
```

### Install the python binding

```sh
$ pip install .
```

## Usage

```sh
$ previewer --preview-height=750 --preview-width=1000 ~/equirectangular.jpg
```

## Credits

Tools used in rendering this package:

*  [`Cookiecutter`][Cookiecutter]
*  [`cookiecutter-pypackage`][cookiecutter-pypackage]

## Contact

[Pierre Dulac][github-dulaccc]  
[@dulaccc][twitter-dulaccc]

## License

`previewer` is available under the MIT license. See the [LICENSE](LICENSE) file for more info.


[build-status-image]: https://img.shields.io/travis/SixiemeEtage/previewer.svg
[travis]: https://travis-ci.org/SixiemeEtage/previewer

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
[github-dulaccc]: https://github.com/dulaccc
[twitter-dulaccc]: https://twitter.com/dulaccc
