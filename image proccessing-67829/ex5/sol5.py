from copy import deepcopy

import tensorflow.keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, Add, Activation
from imageio import imread
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
import numpy as np
from . import sol5_utils
from scipy.ndimage.filters import convolve


REPRESENTATION_GRAY = 1  # the gray representation constant
REPRESENTATION_RGB = 2  # the rgb representation constant
MAX_COLOR_RANGE = 255
DENOISING_QUICK = {True: (10, 3, 2, 30), False: (100, 100, 5, 1000)} # (100, 100, 5, 1000)
DEBLURRING_QUICK = {True: (10, 3, 2, 30), False: (100, 100, 10, 1000)} # (100, 100, 10, 1000)


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


def get_random_image(filenames, read_files):
    """
    :param filenames: all the files to chosoe one from
    :param read_files: the current map of files to images
    :return: the image of the file chosen
    """
    filename = np.random.choice(filenames)
    if filename not in read_files:
        read_files[filename] = read_image(filename, REPRESENTATION_GRAY)
    return read_files[filename]


def choose_random_patch_boundaries(im, height, width):
    """
    :param im: the image
    :param height: the new height
    :param width: the new width
    :return: a random patch of size height, width of the image returned as:
            [[min_x, max_x], [min_y, max_y]]
    """
    im_height, im_width = im.shape
    rand_x = np.random.choice(im_width - width)
    rand_y = np.random.choice(im_height - height)
    return [[rand_x, rand_x + width], [rand_y, rand_y + height]]


def get_im_boundaries(im, boundaries):
    """
    :param im: the current image
    :param boundaries: the patch's boundaries
    :return: the image in the boundaries
    """
    [[min_x, max_x], [min_y, max_y]] = boundaries
    return im[min_y: max_y, min_x: max_x]


def create_random_patch(filenames, corruption_func, read_files, height, width):
    """
    :param filenames: the filenames of the images
    :param corruption_func: the corruption func to teach the network
    :param read_files: a dict of read files
    :param height: the height of the new patch
    :param width: the width of the new patch
    :return: source_im, target_im of this patch to add to the data set
    """
    im = get_random_image(filenames, read_files)

    boundaries = choose_random_patch_boundaries(im, 3 * height, 3 * width)
    patch_im = get_im_boundaries(im, boundaries)
    corrupted_im = corruption_func(deepcopy(patch_im))

    boundaries = choose_random_patch_boundaries(patch_im, height, width)

    source_im = get_im_boundaries(corrupted_im, boundaries) - 0.5
    target_im = get_im_boundaries(patch_im, boundaries) - 0.5

    return source_im, target_im


def load_dataset(filenames, batch_size, corruption_func, crop_size):
    """
    :param filenames: the filenames of the images
    :param batch_size: the size of the training data yields
    :param corruption_func: the corruption func to teach the network
    :param crop_size: a tuple of (height, width) of the patch to return
    :return: a generator for training data
    """
    read_files = {}
    height, width = crop_size
    output_tuple = (batch_size, height, width, 1)
    while True:
        source_batch = np.empty(output_tuple)
        target_batch = np.empty(output_tuple)
        for i in range(batch_size):
            source_im, target_im = create_random_patch(filenames,
                                                       corruption_func,
                                                       read_files,
                                                       height, width)
            source_batch[i] = source_im.reshape(height, width, 1)
            target_batch[i] = target_im.reshape(height, width, 1)

        yield (source_batch, target_batch)


def resblock(input_tensor, num_channels):
    """
    :param input_tensor: the input layer to the resblock
    :param num_channels: the num of channels in the convolution layer
    :return: the last layer after adding a resblock
    """
    layer1 = Conv2D(num_channels, (3, 3), padding='same')(input_tensor)
    layer2 = Activation('relu')(layer1)
    layer3 = Conv2D(num_channels, (3, 3), padding='same')(layer2)
    layer4 = Add()([input_tensor, layer3])
    return Activation('relu')(layer4)


def build_nn_model(height, width, num_channels, num_res_blocks):
    """
    :param height: the input height
    :param width: the input width
    :param num_channels: the num of channels in the convolution
    :param num_res_blocks: the amount of res blocks
    :return: the res model of those inputs
    """
    # input part
    input_layer = Input((height, width, 1))
    layer1 = Conv2D(num_channels, (3, 3), padding='same')(input_layer)
    layer = Activation('relu')(layer1)
    # calculate resblocks
    for _ in range(num_res_blocks):
        layer = resblock(layer, num_channels)
    # output part
    layer2 = Conv2D(1, (3, 3), padding='same')(layer)
    output_layer = Add()([input_layer, layer2])
    return Model(inputs=input_layer, outputs=output_layer)


def train_model(model, images, corruption_func, batch_size, steps_per_epoch,
                num_epochs, num_valid_samples):
    """
    trains the model
    :param model: the current model
    :param images: the images to train with
    :param corruption_func: the corruption function on the images
    :param batch_size: the size of each batch
    :param steps_per_epoch: the amount of batchs per epoch
    :param num_epochs: the amount of epochs
    :param num_valid_samples: the amount of validation between epochs
    """
    crop_size = model.input_shape[1], model.input_shape[2]
    divide_index = int(0.8 * len(images))
    train_generator = load_dataset(images[:divide_index], batch_size, corruption_func, crop_size)
    valid_generator = load_dataset(images[divide_index:], batch_size, corruption_func, crop_size)

    model.compile(loss='mean_squared_error', optimizer=Adam(beta_2=0.9))
    model.fit_generator(train_generator,
                        steps_per_epoch=steps_per_epoch,
                        epochs=num_epochs,
                        validation_data=valid_generator,
                        validation_steps=num_valid_samples / batch_size,
                        use_multiprocessing=True)


def restore_image(corrupted_image, base_model):
    """
    :param corrupted_image: the corrupted image
    :param base_model: the base model for patches
    :return: the prediction of the model for the image
    """
    height, width = corrupted_image.shape
    input_layer = Input((height, width, 1))
    output_layer = base_model(input_layer)
    model = Model(inputs=input_layer, outputs=output_layer)
    processed_data = corrupted_image.reshape(1, height, width, 1) - 0.5
    prediction = model.predict(processed_data)[0].reshape(corrupted_image.shape)
    return (prediction + 0.5).clip(0, 1).astype(np.float64)


def random_number_uniform(min_value, max_value):
    """
    :param min_value: the min value in this range
    :param max_value: the max value in this range
    :return: a random value in range [min, max]
    """
    return np.random.uniform(min_value, max_value)


def add_gaussian_noise(image, min_sigma, max_sigma):
    """
    :param image: the image to add noise to
    :param min_sigma: the min variance of the noise
    :param max_sigma: the max variance of the noise
    :return: the noised image
    """
    sigma = random_number_uniform(min_sigma, max_sigma)
    random_noise = np.random.normal(0, sigma, image.shape)
    im = image + random_noise
    im = np.round(im * MAX_COLOR_RANGE) / MAX_COLOR_RANGE
    return im.clip(0, 1).astype(np.float64)


def learn_denoising_model(num_res_blocks=5, quick_mode=False):
    """
    :param num_res_blocks: the number of res blocks
    :param quick_mode: should learn quicky
    :return: the trained model
    """
    data = sol5_utils.images_for_denoising()
    model = build_nn_model(24, 24, 48, num_res_blocks)
    corruption_func = lambda image: add_gaussian_noise(image, 0, 0.2)
    batch_size, steps_per_epoch, num_epochs, num_valid_samples = DENOISING_QUICK[quick_mode]
    train_model(model, data, corruption_func, batch_size, steps_per_epoch,
                num_epochs, num_valid_samples)
    return model


def add_motion_blur(image, kernel_size, angle):
    """
    :param image: the image to motion blur
    :param kernel_size: the kernel to blur with
    :param angle: the angle to blur in
    :return: the convoled image with motion blur
    """
    return convolve(image, sol5_utils.motion_blur_kernel(kernel_size, angle))


def random_motion_blur(image, list_of_kernel_sizes):
    """
    :param image: image
    :param list_of_kernel_sizes: the kernels to choose from
    :return: returns the image with motion blur in random angle with one of
    the given kernels
    """
    angle = random_number_uniform(0, np.pi)
    kernel = np.random.choice(list_of_kernel_sizes)
    im = add_motion_blur(image, kernel, angle)
    im = np.round(im * MAX_COLOR_RANGE) / MAX_COLOR_RANGE
    return im.clip(0, 1).astype(np.float64)


def learn_deblurring_model(num_res_blocks=5, quick_mode=False):
    """
    :param num_res_blocks: the number of res blocks
    :param quick_mode: should learn quicky
    :return: the trained model
    """
    data = sol5_utils.images_for_deblurring()
    model = build_nn_model(16, 16, 32, num_res_blocks)
    corruption_func = lambda image: random_motion_blur(image, [7])
    batch_size, steps_per_epoch, num_epochs, num_valid_samples = DEBLURRING_QUICK[quick_mode]
    train_model(model, data, corruption_func, batch_size, steps_per_epoch,
                num_epochs, num_valid_samples)
    return model


def plot_model_loss(training_model_func, plot_title, x_label="number of blocks", y_label="validation loss"):
    avg_losses = []
    last_losses = []
    for i in range(1, 6):
        model = training_model_func(i)
        history_losses = model.history.history['val_loss']
        avg_losses.append(sum(history_losses) / len(history_losses))
        last_losses.append(history_losses[-1])

    plt.title(plot_title + " average")
    plt.plot(np.arange(1, 6), avg_losses)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

    plt.title(plot_title + " last loss")
    plt.plot(np.arange(1, 6), last_losses)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def bonus_generator(corrupted_image):
    """
    :param corrupted_image: gets a corrupted image to clean
    :return: the current theta_i, the correct deblurring which is the corrupted_im
    """
    #initiale guess = theta0
    source_batch = np.random.uniform(0, 1, (1,) + current_im.shape) - 0.5
    target_batch = corrupted_image.reshape((1,) + current_im.shape) - 0.5
    while True:
        yield source_batch + np.random.normal(0, 0.3, source_batch.shape), \
              target_batch


def deep_prior_restore_image(corrupted_image):
    """
    :param corrupted_image: gets a corrupted image to clean
    :return: the cleaned image
    """
    height, width = corrupted_image.shape[:2]
    z_vector_length = 32
    # in the github they used num_scales=5
    model = build_nn_model(height, width, z_vector_length, 5)

    train_generator = bonus_generator(corrupted_image)
    model.compile(loss='mean_squared_error', optimizer=Adam(beta_2=0.9))
    model.fit_generator(train_generator, steps_per_epoch=1, epochs=2500,
                        use_multiprocessing=True)
    return restore_image(corrupted_image, model)


if __name__ == '__main__':
    # plot_model_loss(learn_denoising_model, "learning denoising model")
    # plot_model_loss(learn_deblurring_model, "learning deblurring model")

    # model = learn_deblurring_model()
    # model = tensorflow.keras.models.load_model('/cs/usr/mikeg/PycharmProjects/impr-ex5/ex5-mikeg/deblurringModel.h5')
    # im = random_motion_blur(read_image("/cs/usr/mikeg/PycharmProjects/impr-ex5/ex5-mikeg/text_dataset/train/0000006_orig.png", REPRESENTATION_GRAY), [7])
    # plt.figure()
    # plt.imshow(im, cmap='gray')
    # plt.show()
    #
    # im = restore_image(im, model)
    #
    # plt.figure()
    # plt.imshow(im, cmap='gray')
    # plt.show()
    #
    # model.save('/cs/usr/mikeg/PycharmProjects/impr-ex5/ex5-mikeg/deblurringModel.h5')
    # print("hello world!"
    pass
