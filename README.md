# previewer

## Installation

```sh
$ brew install opencv3 --with-python
$ brew install boost --with-python
$ brew install boost-python
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
$ brew link --force opencv3
$ make
$ make install
$ pip install .
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
