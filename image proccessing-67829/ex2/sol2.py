import matplotlib.pyplot as plt
import numpy as np
from imageio import imread
from skimage.color import rgb2gray
from scipy.io.wavfile import read, write
from scipy import signal
from scipy.ndimage.interpolation import map_coordinates


def stft(y, win_length=640, hop_length=160):
    fft_window = signal.windows.hann(win_length, False)

    # Window the time series.
    n_frames = 1 + (len(y) - win_length) // hop_length
    frames = [y[s:s + win_length] for s in np.arange(n_frames) * hop_length]

    stft_matrix = np.fft.fft(fft_window * frames, axis=1)
    return stft_matrix.T


def istft(stft_matrix, win_length=640, hop_length=160):
    n_frames = stft_matrix.shape[1]
    y_rec = np.zeros(win_length + hop_length * (n_frames - 1), dtype=np.float)
    ifft_window_sum = np.zeros_like(y_rec)

    ifft_window = signal.windows.hann(win_length, False)[:, np.newaxis]
    win_sq = ifft_window.squeeze() ** 2

    # invert the block and apply the window function
    ytmp = ifft_window * np.fft.ifft(stft_matrix, axis=0).real

    for frame in range(n_frames):
        frame_start = frame * hop_length
        frame_end = frame_start + win_length
        y_rec[frame_start: frame_end] += ytmp[:, frame]
        ifft_window_sum[frame_start: frame_end] += win_sq

    # Normalize by sum of squared window
    y_rec[ifft_window_sum > 0] /= ifft_window_sum[ifft_window_sum > 0]
    return y_rec


def phase_vocoder(spec, ratio):
    time_steps = np.arange(spec.shape[1]) * ratio
    time_steps = time_steps[time_steps < spec.shape[1]]

    # interpolate magnitude
    yy = np.meshgrid(np.arange(time_steps.size), np.arange(spec.shape[0]))[1]
    xx = np.zeros_like(yy)
    coordiantes = [yy, time_steps + xx]
    warped_spec = map_coordinates(np.abs(spec), coordiantes, mode='reflect',
                                  order=1).astype(np.complex)

    # phase vocoder
    # Phase accumulator; initialize to the first sample
    spec_angle = np.pad(np.angle(spec), [(0, 0), (0, 1)], mode='constant')
    phase_acc = spec_angle[:, 0]

    for (t, step) in enumerate(np.floor(time_steps).astype(np.int)):
        # Store to output array
        warped_spec[:, t] *= np.exp(1j * phase_acc)

        # Compute phase advance
        dphase = (spec_angle[:, step + 1] - spec_angle[:, step])

        # Wrap to -pi:pi range
        dphase = np.mod(dphase - np.pi, 2 * np.pi) - np.pi

        # Accumulate phase
        phase_acc += dphase

    return warped_spec


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


def DFT(signal):
    """
    :param signal: gets a signal
    :return: returns an array of the same size that the fourier transform was
    used on
    """
    length = signal.shape[0]
    coefficient = -2 * np.pi * 1j / length
    u = np.arange(length)[:, np.newaxis]  # u * u.T creates the table of powers
    exp = np.exp(coefficient * np.dot(u, u.T))
    return np.dot(exp, signal)


def IDFT(fourier_signal):
    """
    :param fourier_signal: gets a fourier signal
    :return: returns an array of the same size that the inverse fourier
    transform was used on
    """
    length = fourier_signal.shape[0]
    coefficient = 2 * np.pi * 1j / length
    u = np.arange(length)[:, np.newaxis]  # u * u.T creates the table of powers
    exp = np.exp(coefficient * np.dot(u, u.T))
    return np.dot(exp, fourier_signal) / length


def DFT2(image):
    """
    :param image: gets a 2D gray image
    :return: the fourier transform of the image
    """
    fourier = DFT(image.T)
    fourier = DFT(fourier.T)
    return fourier


def IDFT2(fourier_image):
    """
    :param fourier_image: gets a 2D fourier image
    :return: the real part of the inverse fourier transform of the image
    """
    image = IDFT(fourier_image.T)
    image = IDFT(image.T)
    return image


def change_rate(filename, ratio):
    """
    :param filename: gets a file path
    :param ratio: the change of the rate of audio in the file
    this creates a new file named change_rate.wav with the
    new rate = ratio * old rate
    """
    rate, data = read(filename)
    write("change_rate.wav", int(ratio * rate), data)


def change_samples(filename, ratio):
    """
    get the filename to a wav, resize it, save it and return the resized array
    :param filename: the path to a wav
    :param ratio: the ratio to scale the wav with
    :return: the resized data with ratio
    """
    rate, data = read(filename)
    if ratio != 1:
        new_data = resize(data.astype(np.float64), ratio).astype(np.int16)
    else:
        new_data = data
    write("change_samples.wav", rate, new_data)
    return new_data


def resize(data, ratio):
    """
    :param data: the data to resize
    :param ratio: the ratio to resize with
    :return: the resized data array with with ratio
    """
    fourier = DFT(data)
    shifted = np.fft.fftshift(fourier)
    new_length = int(len(data) / ratio)
    if ratio > 1:
        start = int(len(data) / (2 * ratio))
        shifted = shifted[start: start + new_length]
    elif ratio < 1:
        start = int((new_length - len(data)) / 2)
        end = new_length - len(data) - start
        shifted = np.pad(shifted, (start, end), 'constant')
    if data.dtype == np.float64:
        return IDFT(np.fft.ifftshift(shifted)).real.astype(data.dtype)
    return IDFT(np.fft.ifftshift(shifted)).astype(data.dtype)


def resize_spectrogram(data, ratio):
    """
    :param data: the data to resize
    :param ratio: the ratio to resize with
    :return: use the spec to resize the data for comparison
    """
    spec = stft(data)
    new_data = np.array([resize(spec[i], ratio) for i in range(len(spec))])
    return istft(new_data).real.astype(np.float64)


def resize_vocoder(data, ratio):
    """
    :param data: the data to resize
    :param ratio: the ratio to resize with
    :return: use the vocoder to resize the data for comparison
    """
    spec = stft(data)
    vocoder = phase_vocoder(spec, ratio)
    return istft(vocoder).real.astype(np.float64)


def conv_der(im):
    """
    :param im: gets a 2D gray image
    :return: the convolutional gradient of the image
    """
    # calculate dx
    x_convolution = np.array([[0.5, 0, -0.5]])
    dx = signal.convolve2d(im, x_convolution, mode='same')
    # calculate dy
    y_convolution = np.array([[0.5], [0], [-0.5]])
    dy = signal.convolve2d(im, y_convolution, mode='same')
    return magnitude(dx, dy)


def fourier_der(im):
    """
    :param im: gets a 2D gray image
    :return: the fourier gradient of the image
    """
    coefficient = 2 * np.pi * 1j
    fourier = coefficient * np.fft.fftshift(DFT2(im))
    length1, length2 = im.shape
    # calculate dx
    range_matrix = calculate_range_matrix(length1, length2)
    dx = IDFT2(np.fft.ifftshift(fourier * range_matrix)) / length1
    # calculate dy
    range_matrix = calculate_range_matrix(length2, length1).T
    dy = IDFT2(np.fft.ifftshift(fourier * range_matrix)) / length2
    return magnitude(dx, dy)


def calculate_range_matrix(length1, length2):
    """
    :param length1: the first length
    :param length2: the second length
    :return: a matrix of size length1 * length2 containing the values needed
    for the gradient
    """
    range1 = np.arange(int(-length1 / 2), int(length1 / 2))[:, np.newaxis]
    return range1 * np.ones((1, length2))


def magnitude(dx, dy):
    """
    :param dx: the dx matrix
    :param dy: the dy matrix
    :return: the magnitude of the matrices
    """
    abs_dx = np.abs(dx)
    abs_dy = np.abs(dy)
    return np.sqrt(abs_dx * abs_dx + abs_dy * abs_dy)


def display_fourier(fourier):
    """
    :param fourier: the fourier matrix
    displays the fourier matrix
    """
    display_img_gray(np.log(np.abs(np.fft.fftshift(fourier)) + 1))


# if __name__ == '__main__':
#     rate1, data1 = read("aria_4kHz.wav")
    # data2 = resize_vocoder(data1, 2)
    # write("aria_vocoder.wav", 9600, data2.astype(np.int16))
#     data2 = resize_spectrogram(data1, 0.5)
#     write("aria_spec.wav", 9600, data2.astype(np.int16))
#     print(len(change_samples("aria_4kHz.wav", 2)))
#     im1 = read_image("monkey.jpg", REPRESENTATION_GRAY)
#     display_fourier(DFT2(im1))
#     dft = DFT2(im1)
#     dft2 = np.fft.fft2(im1)
#     for i in range(len(im1)):
#         for j in range(len(im1[0])):
#             if dft2[i][j] - dft[i][j] > 0.00001:
#                 print(i, j)
#     display_img_gray(IDFT2(DFT2(im1)).real)
#     im2 = conv_der(im1)
#     im3 = fourier_der(im1)
#     f, arr = plt.subplots(2, 2)
#     print(im2 - im3)
#     arr[0, 0].imshow(im2 / np.max(im2), cmap=plt.cm.gray)
#     arr[0, 1].imshow(im3 / np.max(im3), cmap=plt.cm.gray)
#     arr[1, 0].imshow((im3 / np.max(im3) - im2 / np.max(im2)),
#      cmap=plt.cm.gray)
#     plt.show()
#     plt.imshow(im3, cmap=plt.cm.gray)
#     plt.show()
