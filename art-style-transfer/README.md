# Art Style Transfer
<img src="./assets/in.gif" height="700px">            <img src="./assets/out.gif" height="700px">

## Setup
Use your choice of Python 3.9+ virtual environment or conda environment.

**Make sure environment is 3.9+**

Then run:

``pip install -r requirements.txt``

## Video
``python video.py``

Note the following arguments, which are all optional:

```
usage: video.py [-h] [--i I] [--s S] [--u U] [--r R] [--w W] [--f F]

optional arguments:
  -h, --help            show this help message and exit
  --i I, ---img_name I  Image name of the artwork to transfer the style from
                        in the art folder.
  --s S, --src S        Input source. Defaults to 0 for web cam.
  --u U, --url U        URL to the tf hub model.
  --r R, --resolution R
                        Resolution of the smallest dimension of the input.
  --w W, --write W      Whether or not to write the output.
  --f F, --frame_skip F
                        Number of frames to skip between processing.
                        
```

## Image
``python img.py [path to input image]``

Pass any image preprocessing logic (i.e. blurring) into the ``preprocess`` argument as a function. Note that the preprocessing function should return a ``numpy.ndarray``.

Note the following arguments, which are all optional except for src:
```
usage: img.py [-h] [--i I] [--u U] [--r R] [--w W] src

positional arguments:
  src                   Input image

optional arguments:
  -h, --help            show this help message and exit
  --i I, ---img_name I  Image name of the artwork to transfer the style from
                        in the art folder.
  --u U, --url U        URL to the tf hub model.
  --r R, --resolution R
                        Resolution of the smallest dimension of the input.
  --w W, --write W      Whether or not to write the output.
```
