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
$ git clone https://github.com/Photonomie/previewer
$ cd previewer
$ mkdir -p native/build && cd native/build
$ cmake .. \
-DPYTHON_DESIRED_VERSION=2.X \
-DPYTHON2_EXECUTABLE=/usr/local/bin/python \
-DBoost_INCLUDE_DIR=/usr/local/bin/python \
-DPYTHON2_LIBRARY=/usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/Current/lib/libpython2.7.dylib \
-DPYTHON2_INCLUDE_DIR=/usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/Current/include/python2.7/ \
-DPYTHON2_NUMPY_INCLUDE_DIRS=/usr/local/Cellar/numpy/1.12.0/lib/python2.7/site-packages/numpy/core/include/ \
-DBOOST_ROOT=/usr/local/Cellar/boost/1.63.0/ \
-DBoost_INCLUDE_DIR=/usr/local/Cellar/boost/1.63.0/include/
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


[build-status-image]: https://img.shields.io/travis/Photonomie/previewer.svg
[travis]: https://travis-ci.org/Photonomie/previewer

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
[github-dulaccc]: https://github.com/dulaccc
[twitter-dulaccc]: https://twitter.com/dulaccc
