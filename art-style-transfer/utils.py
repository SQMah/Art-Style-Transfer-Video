import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import functools
import matplotlib.pyplot as plt
import cv2

tf.config.run_functions_eagerly(False)


def load_model(handle: str):
    """Load a tensorflow model from tf hub.
    :param handle: the url of the model on Tensorflow hub
    :return tf model"""
    hub_module = hub.load(handle)
    return hub_module


def get_dims(img: np.ndarray, minor_dim: int) -> tuple:
    minor_dim: int = int(minor_dim)
    h, w, c = img.shape
    if w >= h:
        ratio: float = w / h
        w_prime: int = int(ratio * minor_dim)
        return w_prime, minor_dim
    else:
        ratio: float = h / w
        h_prime: int = int(ratio * minor_dim)
        return h_prime, minor_dim


def resize(img: np.ndarray, minor_dim: int) -> np.ndarray:
    """Resizes an image such that the smaller length of the image is minor_dim pixels
    in length, maintaining aspect ratio.
    :param img: input image
    :param minor_dim: length that minor dim is resized to
    :return resized image"""
    return cv2.resize(img, get_dims(img, minor_dim))


def crop_center(image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape)
    return image


@functools.lru_cache(maxsize=None)
def load_image(image_path: str, image_size: tuple[int, int] = (256, 256), preserve_aspect_ratio: bool = True):
    """Loads and preprocesses images."""
    # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
    img = plt.imread(image_path).astype(np.float32)[np.newaxis, ...]
    if img.max() > 1.0:
        img = img / 255.
    if len(img.shape) == 3:
        img = tf.stack([img, img, img], axis=-1)
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=preserve_aspect_ratio)
    return img


def run(src: np.ndarray, transfer: np.ndarray, model) -> tf.Tensor:
    """Returns a style transfered image
    :param src: source image to get styles from
    :param transfer: image to transfer style to
    :param model: preloaded tensorflow model
    :return style transferred image"""
    outputs = model(tf.constant(transfer), tf.constant(src))
    stylized_image = outputs[0]
    return stylized_image
