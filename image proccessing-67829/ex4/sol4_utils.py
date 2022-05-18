from scipy.signal import convolve2d
from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from imageio import imread
from skimage.color import rgb2gray
from scipy import ndimage


REPRESENTATION_GRAY = 1  # the gray representation constant
REPRESENTATION_RGB = 2  # the rgb representation constant
MAX_COLOR_RANGE = 255
MINIMUM_SIZE = 16


def gaussian_kernel(kernel_size):
    conv_kernel = np.array([1, 1], dtype=np.float64)[:, None]
    conv_kernel = convolve2d(conv_kernel, conv_kernel.T)
    kernel = np.array([1], dtype=np.float64)[:, None]
    for i in range(kernel_size - 1):
        kernel = convolve2d(kernel, conv_kernel, 'full')
    return kernel / kernel.sum()


def blur_spatial(img, kernel_size):
    kernel = gaussian_kernel(kernel_size)
    blur_img = np.zeros_like(img)
    if len(img.shape) == 2:
        blur_img = convolve2d(img, kernel, 'same', 'symm')
    else:
        for i in range(3):
            blur_img[..., i] = convolve2d(img[..., i], kernel, 'same', 'symm')
    return blur_img


def is_gray_img(img):
    # if the im has only 2 dims, width height then it is gray
    return img.ndim == 2


def read_image(filename, representation):
    """
    :param filename: get a filename to an img
    :param representation: the type of the img (gray or rgb)
    :return: the img
    """
    im = np.array(imread(filename)).astype(np.float64)  # read the image
    im /= MAX_COLOR_RANGE  # normalise img
    if representation == REPRESENTATION_RGB:
        return im[:, :, 0:3]
    elif representation == REPRESENTATION_GRAY:
        if is_gray_img(im):
            return im
        # else it has 3 dims and needs to be converted to gray
        return rgb2gray(im)


def convert_to_unit8_img(img):
    """
    :param img: get an img of range [0-1]
    :return: the img to be in the range [0-255]
    """
    return (img * MAX_COLOR_RANGE).astype(np.uint8)


def display_img_rgb(img):
    """
    :param img: get a rgb img of range [0-1]
    displays the rgb img
    """
    plt.figure()
    plt.imshow(img)
    plt.axis('off')
    plt.show()


def display_img_gray(img):
    """
    :param img: get a gray img of range [0-1]
    displays the gray img
    """
    plt.figure()
    plt.imshow(img, cmap=plt.cm.gray)
    plt.axis('off')
    plt.show()


def imdisplay(filename, representation):
    """
    :param filename: get a filename to an img
    :param representation: the type of the img (gray or rgb)
    displays the img in gray or rgb as given
    """
    img = read_image(filename, representation)
    if representation == REPRESENTATION_GRAY:
        display_img_gray(img)
    elif representation == REPRESENTATION_RGB:
        display_img_rgb(img)


def display_img(img):
    """
    :param img: the current in
    displays it on the screen whether it is gray or rgb
    """
    if is_gray_img(img):
        display_img_gray(img)
    else:
        display_img_rgb(img)


def compress_image(im: np.ndarray, filter_image: np.ndarray) -> np.ndarray:
    """
    :param im: gets an img
    :param filter_image: gets a 2D filter
    :return: convolve the im with filter and filter.T and returns it in
    even indices
    """
    filtered = ndimage.filters.convolve(im, filter_image)
    filtered = ndimage.filters.convolve(filtered, filter_image.T)
    return filtered[::2, ::2]


def expand_image(im: np.ndarray, filter_image: np.ndarray,
                 new_shape: np.shape) -> np.ndarray:
    """
    :param im: gets an img
    :param filter_image: gets a 2D filter
    :param new_shape: gets the new shape of the image
    (bigger than the original)
    :return: creates an expansion of the im to be of shape new_shape
    """
    zeroed = np.zeros(new_shape)
    zeroed[::2, ::2] = im
    filtered = ndimage.filters.convolve(zeroed, 2 * filter_image)
    filtered = ndimage.filters.convolve(filtered, 2 * filter_image.T)
    return filtered


def create_filter(filter_size: int) -> np.ndarray:
    """
    :param filter_size: gets the filter size
    :return: the gaussian filter of that size
    """
    filter_image = create_filter_helper(filter_size)
    filter_image = filter_image / np.sum(filter_image)
    return np.array([filter_image])


def create_filter_helper(filter_size: int) -> np.ndarray:
    """
    :param filter_size: gets the filter size
    :return: the gaussian filter of that size
    """
    helper = np.array([1, 1])
    if filter_size == 1:
        return np.array([1])
    current = helper
    for i in range(filter_size - 2):
        current = np.convolve(current, helper, mode='full')
    return current


def build_gaussian_pyramid(im: np.ndarray, max_levels: int, filter_size: int) \
        -> Tuple[List[np.ndarray], np.ndarray]:
    """
    :param im: the image to create the pyramid of
    :param max_levels: the amount of levels in the pyramid
    :param filter_size: the filter size of each level
    :return: the gaussian pyramid as a list of images and the filter used
    """
    filter_image = create_filter(filter_size)
    pyr = []
    while 0 < max_levels and MINIMUM_SIZE <= len(im) \
            and MINIMUM_SIZE <= len(im[0]):
        pyr.append(im)
        im = compress_image(im, filter_image)
        max_levels = max_levels - 1
    return pyr, filter_image


def build_laplacian_pyramid(im: np.ndarray, max_levels: int,
                            filter_size: int) \
        -> Tuple[List[np.ndarray], np.ndarray]:
    """
    :param im: the image to create the pyramid of
    :param max_levels: the amount of levels in the pyramid
    :param filter_size: the filter size of each level
    :return: the laplacian pyramid as a list of images and the filter used
    """
    pyr, filter_image = build_gaussian_pyramid(im, max_levels, filter_size)
    laplacian = [pyr[i] - expand_image(pyr[i + 1], filter_image, pyr[i].shape)
                 for i in range(len(pyr) - 1)]
    laplacian.append(pyr[-1])
    return laplacian, filter_image


def laplacian_to_image(lpyr: List[np.ndarray], filter_vec: np.ndarray, coeff) \
        -> np.ndarray:
    """
    :param lpyr: the laplacian pyramid to conve
    :param filter_vec:
    :param coeff:
    :return:
    """
    lpyr = [coeff[i] * lpyr[i] for i in range(len(lpyr))]
    im = lpyr[-1]
    for i in range(len(lpyr) - 2, -1, -1):
        im = lpyr[i] + expand_image(im, filter_vec, lpyr[i].shape)
    return im


def render_part_pyramid(old_im: np.ndarray, width: int):
    """
    :param old_im: the old image
    :param width: the new width
    :return: the im with the new width
    """
    old_width, old_height = old_im.shape
    old_im = (old_im - np.min(old_im)) / (np.max(old_im) - np.min(old_im))
    new_im = np.zeros((width, old_height))
    new_im[:old_width, :] = old_im
    return new_im


def render_pyramid(pyr: List[np.ndarray], levels: int) -> np.ndarray:
    """
    :param pyr: the pyramid to render
    :param levels: the amount of levels to render
    :return: the new image containing all the levels up to level
    """
    width, height = pyr[0].shape
    new_pyr = tuple(render_part_pyramid(pyr[i], width).T
                    for i in range(min(levels, len(pyr))))
    new_im = np.concatenate(new_pyr).T
    return new_im


def display_pyramid(pyr: List[np.ndarray], levels: int) -> None:
    """
    :param pyr: the pyramid to render
    :param levels: the amount of levels to render
    display the first levels of the pyramid
    """
    display_img(render_pyramid(pyr, levels))


def pyramid_blending_channel(im1: np.ndarray, im2: np.ndarray,
                             mask: np.ndarray, max_levels: int,
                             filter_size_im: int, filter_size_mask: int) \
        -> np.ndarray:
    """
    :param im1: the first im
    :param im2: the second im
    :param mask: the mask
    :param max_levels: the amount of levels in the pyramid
    :param filter_size_im: the filter for the images
    :param filter_size_mask: the filter for the mask
    :return: the created image
    """
    lpyr1, filter1 = build_laplacian_pyramid(im1, max_levels, filter_size_im)
    lpyr2, filter2 = build_laplacian_pyramid(im2, max_levels, filter_size_im)
    lpyr_mask, filter_mask = build_gaussian_pyramid(mask.astype(np.float64),
                                                    max_levels,
                                                    filter_size_mask)
    lpyr = [(lpyr1[i] * lpyr_mask[i] + (1 - lpyr_mask[i]) * lpyr2[i])
            for i in range(len(lpyr1))]
    return laplacian_to_image(lpyr, filter1, [1] * len(lpyr))


def pyramid_blending(im1: np.ndarray, im2: np.ndarray,
                     mask: np.ndarray, max_levels: int,
                     filter_size_im: int, filter_size_mask: int) \
        -> np.ndarray:
    """
    :param im1: image 1
    :param im2: image 2
    :param mask: the mask to combine
    :param max_levels: the max levels of the pyramid
    :param filter_size_im: the filter of the images
    :param filter_size_mask: the filter of the mask
    :return: the blended image
    """
    if is_gray_img(im1):
        return pyramid_blending_channel(im1, im2, mask, max_levels,
                                        filter_size_im, filter_size_mask)
    im = np.zeros(im1.shape)
    for i in range(3):
        im[:, :, i] = pyramid_blending_channel(im1[:, :, i], im2[:, :, i],
                                               mask, max_levels,
                                               filter_size_im,
                                               filter_size_mask)
    return im
