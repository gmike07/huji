import matplotlib.pyplot as plt
import numpy as np
from imageio import imread
from skimage.color import rgb2gray
import cv2

REPRESENTATION_GRAY = 1  # the gray representation constant
REPRESENTATION_RGB = 2  # the rgb representation constant
RGB_TO_YIQ_MATRIX = np.array([
    [0.299, 0.587, 0.114],
    [0.596, -0.275, -0.321],
    [0.212, -0.523, 0.311]
])
YIQ_TO_RGB_MATRIX = np.linalg.inv(RGB_TO_YIQ_MATRIX)
MAX_COLOR_RANGE = 255


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


def rgb2yiq(imRGB):
    """
    :param imRGB: get a rgb img of range [0-1]
    :return: a yiq img of range [-1-1]
    """
    yiq = np.dot(imRGB, RGB_TO_YIQ_MATRIX.T).astype(np.float64)
    return yiq


def yiq2rgb(imYIQ):
    """
    :param imYIQ: get a yiq img of range [-1-1]
    :return: a rgb img of range [0-1]
    """
    rgb = np.dot(imYIQ, YIQ_TO_RGB_MATRIX.T).astype(np.float64)
    return rgb


def histogram_equalize(im_orig):
    """
    :param im_orig: get an img of range [0-1]
    :return: [im_eq, hist_orig, hist_eq] when the hist_orig is the histogram
    before change, hist_eq is the histogram after change, and im_eq is the
    changed image
    """
    if is_gray_img(im_orig):
        im_fixed, hist_orig, hist_eq = histogram_equalize_gray(im_orig)
        return [np.clip(im_fixed, 0, 1), hist_orig, hist_eq]
    # it is rgb
    yiq = rgb2yiq(im_orig)
    gray_im_fixed, hist_orig, hist_eq = histogram_equalize_gray(yiq[:, :, 0])
    yiq[:, :, 0] = gray_im_fixed
    rgb = yiq2rgb(yiq)
    return [np.clip(rgb, 0, 1), hist_orig, hist_eq]


def histogram_equalize_gray(im_orig, bin_number=256):
    """
    :param im_orig: get an img of range [0-1]
    :param bin_number: the number of bins
    :return: [im_eq, hist_orig, hist_eq] when the hist_orig is the histogram
    before change, hist_eq is the histogram after change, and im_eq is the
    changed image
    """
    fixed_im = convert_to_unit8_img(im_orig)  # [0-255] mapping
    hist_orig, bins = np.histogram(fixed_im, bin_number, (0, MAX_COLOR_RANGE))

    cumsum = hist_orig.cumsum()
    cumsum = cumsum * (MAX_COLOR_RANGE / cumsum[-1])  # normalize cumsum

    m = np.where(cumsum > 0)[0][0]  # the first non zero value
    # 0-1 mapping
    im_eq = (cumsum[fixed_im] - cumsum[m]) / (cumsum[-1] - cumsum[m])
    hist_eq, bins = np.histogram(convert_to_unit8_img(im_eq),
                                 bin_number, (0, MAX_COLOR_RANGE))
    return [im_eq, hist_orig, hist_eq]


def calculate_new_z(q, n_quant):
    """
    :param q: get the current q vector from values [0-255]
    :param n_quant: get the length of the q vector
    :return: the new z from values [0-255]
    """
    last_q = q[:-1]  # qi
    next_q = q[1:]  # q_(i+1)
    z = np.empty((n_quant + 1,), np.float64)
    z[0] = 0
    z[1:-1] = (last_q + next_q) / 2.0  # (qi + q_(i+1)) / 2
    z[-1] = MAX_COLOR_RANGE
    return np.rint(z).astype(np.int)


def calculate_new_q(z, probability_z, n_quant):
    """
    :param z: get the current z vector from values [0-255]
    :param probability_z: get the probability of z in the img
    :param n_quant: get the length of the q vector
    :return:
    """
    q = np.empty((n_quant,), np.float64)
    prod = probability_z * np.arange(MAX_COLOR_RANGE + 1)  # z * p(z)
    for i in range(n_quant):
        range_i = np.arange(z[i], z[i + 1] + 1)
        q[i] = sum(prod[range_i]) / sum(probability_z[range_i])
    return q


def calculate_error(z, q, probability_z, n_quant):
    """
    :param z: the z vector
    :param q: the q vector
    :param probability_z: the amount of pixels in z
    :param n_quant: the length of the q vector
    :return: the error of q on this probability
    """
    error = 0
    prob = probability_z
    for i in range(n_quant):
        range_i = np.arange(z[i], z[i + 1] + 1)
        squared = (range_i - q[i]) * (range_i - q[i])
        error += sum(prob[range_i] * squared)
    return error


def init_z(histogram, n_quant):
    """
    :param histogram: a NORMALIZED histogram
    :param n_quant: the length of the q vector
    :return: an initialize guess of vector z
    """
    cumsum = histogram.cumsum()
    cumsum = (cumsum / cumsum[-1]) * MAX_COLOR_RANGE  # normalized cumsum
    z = np.empty(n_quant + 1).astype(np.int)
    z[0] = 0
    procent = MAX_COLOR_RANGE / n_quant
    for i in range(1, n_quant + 1):
        num = max(z[i - 1], round(i * procent))
        z[i] = np.where(cumsum >= num)[0][0]  # the first value bigger than
        # i*procent
    z[-1] = MAX_COLOR_RANGE
    return np.rint(z).astype(np.int)


def calculate_q(histogram, n_quant, n_iter):
    """
    :param histogram: a NORMALIZED histogram
    :param n_quant: the length of the q vector
    :param n_iter: the amount of iterations
    :return: [z, q, errors] when z, q are the calculated values and errors
    are the errors of all calculations up to now
    """
    z = init_z(histogram, n_quant)
    errors = np.array([])
    last_q = np.zeros((n_quant,))
    q = None
    for i in range(n_iter):
        q = calculate_new_q(z, histogram, n_quant)
        z = calculate_new_z(q, n_quant)
        errors = np.append(errors, np.array(
            [calculate_error(z, q, histogram, n_quant)]))
        if sum(abs(q - last_q)) == 0:  # q == last_q
            break
        last_q = q
    return [z, q, np.rint(errors).astype(np.int)]


def update_img_with_q(fixed_im, n_quant, q, z):
    """
    :param fixed_im: the original img to fix of range [0-255]
    :param n_quant: the length of the q vector
    :param q: the q vector that was found in the end
    :param z: the z vector that was found in the end
    :return: an updated img with q,z in range [0-1]
    """
    z = np.rint(z).astype(np.int)
    q = q.astype(np.uint8)
    new_range = np.zeros(MAX_COLOR_RANGE + 1)
    for i in range(n_quant):
        range_i = np.arange(z[i], z[i + 1] + 1)
        new_range[range_i] = q[i]
    fixed_im[:, :] = new_range[fixed_im[:, :]]
    return fixed_im.astype(np.float64) / MAX_COLOR_RANGE


def quantize_gray(im_orig, n_quant, n_iter, bin_number=256):
    """
    :param im_orig: the original img to fix of range [0-1]
    :param n_quant: the length of the q vector
    :param n_iter: the amount of iterations
    :param bin_number: the bin number of the histogram
    :return: [fixed_im, errors] when the errors is the errors of the img
    and the img is in range [0-1]
    """
    fixed_im = convert_to_unit8_img(im_orig)  # [0-255] mapping
    hist, bins = np.histogram(fixed_im, bin_number, (0, MAX_COLOR_RANGE))
    hist = hist / sum(hist)  # normalized histogram
    z, q, errors = calculate_q(hist, n_quant, n_iter)
    fixed_im = update_img_with_q(fixed_im, n_quant, q, z)
    return [fixed_im, errors]


def quantize(im_orig, n_quant, n_iter):
    """
    :param im_orig: the original img to fix of range [0-1]
    :param n_quant: the length of the q vector
    :param n_iter: the amount of iterations
    :return: [fixed_im, errors] when the errors is the errors of the img
    and the img is in range [0-1]
    """
    if is_gray_img(im_orig):
        return quantize_gray(im_orig, n_quant, n_iter)
    # it is rgb
    yiq = rgb2yiq(im_orig)
    gray_im_fixed, errors = quantize_gray(yiq[:, :, 0], n_quant, n_iter)
    yiq[:, :, 0] = gray_im_fixed
    rgb = yiq2rgb(yiq)
    return [rgb, errors]


def quantize_rgb(im_orig, n_quant):
    """
    i first found a code close to the required one,
    https://stackoverflow.com/questions/48222977/python-converting-an-image-to-use-less-colors
    understood it, and used it with the function from a different library (cv2)
    to check i understood how it works
    :param im_orig: the img to quantize in range [0-1]
    :param n_quant: the amount of colors to quantize with
    :return: the quantized img in range [0-1]
    """
    width, height, depth = im_orig.shape
    # flatten everything except RGB, i.e. 2D array of RGB values
    im = im_orig.reshape((width * height, depth))
    # the function expects float32
    im = im.astype(np.float32)
    # the maximum number that the kmeans will run
    max_iter = max(int(n_quant ** 1.3), 10 * n_quant)
    epsilon = 1.0  # the difference of which the algorithm will stop
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iter,
                epsilon)
    flags = cv2.KMEANS_RANDOM_CENTERS  # start from random guesses
    # find the best colors (minimize error of sqrt(x^2+y^2+z^2)
    # which is the same desire as quantization
    # save the best centers and labels, labels are the same shape as im
    # and contain arr[i] = the number of center that should be in pixel i
    algorithm_error, im_labels, im_centers = cv2.kmeans(im, n_quant, None,
                                                        criteria, max_iter,
                                                        flags)
    # index of the center
    im_labels = im_centers[im_labels]
    # transform the image to the shape of the input
    # i,e, back to 3D of (width, height, depth)
    im_labels = im_labels.reshape(im_orig.shape)
    # make sure the type is float64
    im_labels = im_labels.astype(np.float64)
    return im_labels
