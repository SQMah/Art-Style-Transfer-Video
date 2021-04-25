import numpy as np
from utils import load_model, run, load_image, resize, get_dims
import cv2
from typing import Union
import os
import argparse

def run_video(src: Union[str, int], url: str, img_path: str, res: int, skip_frames: int = 1, write_out: bool = False):
    if type(src) == str and not os.path.isfile(src):
        raise ValueError(f"File path: {src} is not a valid video file path!")
    if not os.path.isfile(img_path):
        raise ValueError(f"File path: {img_path} is not a valid input style image path!")

    i = 0
    cap = cv2.VideoCapture(src)
    style_image: np.ndarray = load_image(img_path)
    model = load_model(url)
    if write_out:
        status, img = cap.read()
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video = cv2.VideoWriter("out.mp4", fourcc, 30 // skip_frames, get_dims(img, res))

    while cap.isOpened():
        status, img = cap.read()
        if i % skip_frames == 0:
            i = 0
            img = cv2.cvtColor(resize(img, res), cv2.COLOR_BGR2RGB) / 255
            img = np.expand_dims(img, axis=0)
            img = np.ndarray.astype(img, np.float32)
            out = run(src=style_image, transfer=img, model=model)
            out = cv2.cvtColor(np.ndarray.astype(out[0].numpy() * 255, np.uint8), cv2.COLOR_RGB2BGR)

            if write_out:
                video.write(out)
            cv2.imshow("Output", out)
            cv2.waitKey(1)
        i += 1

    if write_out:
        video.release()


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
    parser.add_argument('--s', '--src', default=0, help="Input source. 0 for web cam.")

    parser.add_argument('--u', '--url', default=HANDLE, help="URL to the tf hub model.")
    parser.add_argument('--r', '--resolution', type=int, default=360, help="Resolution of the smallest dimension of "
                                                                           "the input.")
    parser.add_argument('--w', '--write', type=bool, default=False, help="Whether or not to write the output.")
    parser.add_argument('--f', '--frame_skip', type=int, default=1, help="Number of frames to skip between processing.")
    args = parser.parse_args()
    run_video(args.s, args.u, get_img_url(args.i), args.r, args.f, args.w)
