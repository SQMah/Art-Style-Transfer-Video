import numpy as np
from utils import load_model, run, load_image, resize
import cv2
import tensorflow as tf
import os
import argparse


def img_preprocess(img: np.ndarray) -> np.ndarray:
    """Put any image preprocessing logic here."""
    return img


def run_img(src: str, url: str, img_path: str, res: int, preprocess=img_preprocess, write_out: bool = False):
    if not os.path.isfile(src):
        raise ValueError(f"File path: {src} is not a valid video file path!")
    if not os.path.isfile(img_path):
        raise ValueError(f"File path: {img_path} is not a valid input style image path!")

    style_image: np.ndarray = load_image(img_path)
    img = preprocess(cv2.imread(src))

    model = load_model(url)

    img = cv2.cvtColor(resize(img, res), cv2.COLOR_BGR2RGB) / 255
    img = np.expand_dims(img, axis=0)
    img = np.ndarray.astype(img, np.float32)
    out = run(src=tf.constant(style_image), transfer=img, model=model)
    out = cv2.cvtColor(np.ndarray.astype(out[0].numpy() * 255, np.uint8), cv2.COLOR_RGB2BGR)
    if write_out:
        cv2.imwrite("out.jpg", out)
    cv2.imshow("Output", out)
    cv2.waitKey(10000)


if __name__ == "__main__":
    def get_img_url(name: str):
        return os.path.join(os.path.join(os.getcwd(), "art"), name)


    # Link to the tf hub of the model
    HANDLE: str = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
    DEFAULT_IMG: str = 'wave.jpg'

    parser = argparse.ArgumentParser()
    parser.add_argument('--i', '---img_name',
                        default=DEFAULT_IMG,
                        help="Image name of the artwork to transfer the style from in the art folder.")
    parser.add_argument('src', help="Input image")

    parser.add_argument('--u', '--url', default=HANDLE, help="URL to the tf hub model.")
    parser.add_argument('--r', '--resolution', type=int, default=360, help="Resolution of the smallest dimension of "
                                                                           "the input.")
    parser.add_argument('--w', '--write', type=bool, default=False, help="Whether or not to write the output.")
    args = parser.parse_args()
    run_img(args.src, args.u, get_img_url(args.i), args.r, write_out=args.w)
