# Initial code for ex4.
# You may change this code, but keep the functions' signatures
# You can also split the code to multiple files as long as this file's API is
# unchanged
import shutil
import numpy as np
import matplotlib.pyplot as plt
from imageio import imwrite
import os
from scipy.signal import convolve2d

from scipy.ndimage.morphology import generate_binary_structure
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage import label, center_of_mass, map_coordinates
import sol4_utils

DER_X_CONVOLUTION = np.array([[1, 0, -1]])
DER_Y_CONVOLUTION = DER_X_CONVOLUTION.T
HARRIS_CORNER_DETECTOR_K_FACTOR = 0.04
X_INDEX = 0
Y_INDEX = 1
BLURRING_FACTOR = 3
RADIUS = 3
LEVEL = 3


def harris_corner_detector(im):
    """
    Detects harris corners.
    Make sure the returned coordinates are x major!!!
    :param im: A 2D array representing an image.
    :return: An array with shape (N,2), where ret[i,:] are the [x,y]
    coordinates of the ith corner points.
    """
    # calculate derivatives
    Ix = convolve2d(im, DER_X_CONVOLUTION, mode='same', boundary='symm')
    Iy = convolve2d(im, DER_Y_CONVOLUTION, mode='same', boundary='symm')
    # calculate M
    Ixx = sol4_utils.blur_spatial(Ix * Ix, BLURRING_FACTOR)
    Ixy = sol4_utils.blur_spatial(Ix * Iy, BLURRING_FACTOR)
    Iyy = sol4_utils.blur_spatial(Iy * Iy, BLURRING_FACTOR)
    # calculate M det and M trace
    det = Ixx * Iyy - Ixy * Ixy
    trace = Ixx + Iyy
    # calculate R and the indexes
    R = det - HARRIS_CORNER_DETECTOR_K_FACTOR * (trace * trace)
    R = non_maximum_suppression(R)
    y, x = np.nonzero(R)

    return np.column_stack((x, y))


def sample_descriptor(im, pos, desc_rad):
    """
    Samples descriptors at the given corners.
    :param im: A 2D array representing an image.
    :param pos: An array with shape (N,2), where pos[i,:] are the [x,y]
    coordinates of the ith corner point.
    :param desc_rad: "Radius" of descriptors to compute.
    :return: A 3D array with shape (N,K,K) containing the ith descriptor at
    desc[i,:,:].
    """
    K = 1 + 2 * desc_rad
    N = len(pos)
    desc = np.zeros((N, K, K))
    for i in range(N):
        x, y = pos[i]
        x_range = np.arange(x - desc_rad, x + desc_rad + 1)
        y_range = np.arange(y - desc_rad, y + desc_rad + 1)
        x_coordinates, y_coordinates = np.meshgrid(x_range, y_range)
        mapping = [y_coordinates.reshape(-1), x_coordinates.reshape(-1)]
        descriptor = map_coordinates(im, mapping, order=1, prefilter=False)

        # normalize and update desc
        descriptor = descriptor - np.mean(descriptor)
        norm = np.linalg.norm(descriptor)
        if norm == 0:
            desc[i, :, :] = np.zeros((K, K))
        else:
            desc[i, :, :] = (descriptor / norm).reshape((K, K))

    return desc


def find_features(pyr):
    """
    Detects and extracts feature points from a pyramid.
    :param pyr: Gaussian pyramid of a grayscale image having 3 levels.
    :return: A list containing:
                1) An array with shape (N,2) of [x,y] feature location per row
                    found in the image.
                   These coordinates are provided at the pyramid level pyr[0].
                2) A feature descriptor array with shape (N,K,K)
    """
    K = 1 + 2 * RADIUS
    harris_corners = spread_out_corners(pyr[0], K, K, RADIUS)
    pyramid_points = 2 ** (-LEVEL + 1) * harris_corners
    harris_descriptor = sample_descriptor(pyr[LEVEL - 1], pyramid_points,
                                          RADIUS)
    return [harris_corners, harris_descriptor]


def find_N_largest_in_last_dim(array, N):
    """
    :param array: the array
    :param N: the amount of big elements of the array
    :return: the N biggest values in the array
    """
    return np.argpartition(array, -N)[:, -N:]


def filter_x_table(scoring_table):
    """
    :param scoring_table: the current scoring table
    :return: the scoring table after deleting everything that isn't top 2
    """
    filter_x = np.zeros(scoring_table.shape)
    x_range = np.arange(len(filter_x))
    largest_y = find_N_largest_in_last_dim(scoring_table, 2).T
    filter_x[x_range, largest_y[0]] = scoring_table[x_range, largest_y[0]]
    filter_x[x_range, largest_y[1]] = scoring_table[x_range, largest_y[1]]
    return filter_x


def match_features(desc1, desc2, min_score):
    """
    Return indices of matching descriptors.
    :param desc1: A feature descriptor array with shape (N1,K,K).
    :param desc2: A feature descriptor array with shape (N2,K,K).
    :param min_score: Minimal match score.
    :return: A list containing:
        1) An array with shape (M,) and dtype int of matching indices in desc1.
        2) An array with shape (M,) and dtype int of matching indices in desc2.
    """
    N1, N2, K = len(desc1), len(desc2), len(desc1[0])
    desc1 = desc1.reshape((N1, K * K))
    desc2 = desc2.reshape((N2, K * K))
    scoring_table = desc1 @ desc2.T
    scoring_table[scoring_table < min_score] = 0
    filter_x = filter_x_table(scoring_table)
    filter_y = filter_x_table(filter_x.T)
    index1, index2 = np.nonzero(filter_y.T)
    return [index1, index2]


def apply_homography(pos1, H12):
    """
    Apply homography to inhomogenous points.
    :param pos1: An array with shape (N,2) of [x,y] point coordinates.
    :param H12: A 3x3 homography matrix.
    :return: An array with the same shape as pos1 with [x,y] point coordinates
    obtained from transforming pos1 using H12.
    """
    N = len(pos1)
    result = np.ones((N, 3))
    result[:, : 2] = pos1
    result = np.dot(result, H12.T)  # (x,y,z) * H12^T = (H12 * (x,y,z)^T)^T
    result[:, 0] /= result[:, 2]  # normalize
    result[:, 1] /= result[:, 2]  # normalize
    return result[:, :2]


def ransac_homography(points1, points2, num_iter, inlier_tol,
                      translation_only=False):
    """
    Computes homography between two sets of points using RANSAC.
    :param points1: An array with shape (N,2) containing N rows of [x,y]
    coordinates of matched points in image 1.
    :param points2: An array with shape (N,2) containing N rows of [x,y]
    coordinates of matched points in image 2.
    :param num_iter: Number of RANSAC iterations to perform.
    :param inlier_tol: inlier tolerance threshold.
    :param translation_only: see estimate rigid transform
    :return: A list containing:
        1) A 3x3 normalized homography matrix.
        2) An Array with shape (S,) where S is the number of inliers,
            containing the indices in pos1/pos2 of the maximal set of
            inlier matches found.
    """
    N = len(points1)
    best_guess = np.array([])
    for _ in range(num_iter):
        indexes = np.random.choice(np.arange(N), 2)
        # calculate transform
        transform = estimate_rigid_transform(points1[indexes, :],
                                             points2[indexes, :],
                                             translation_only)
        # calculate the new points
        new_points = apply_homography(points1, transform)
        # all bad points = 0
        norm_matrix = np.linalg.norm(new_points - points2, axis=1) ** 2
        new_points[norm_matrix >= inlier_tol] = 0
        # normalize all good points
        new_points[new_points != 0] = 1
        guess, _ = np.nonzero(new_points)
        if len(best_guess) < len(guess):
            best_guess = guess

    transform = estimate_rigid_transform(points1[best_guess, :],
                                         points2[best_guess, :],
                                         translation_only)
    return [transform / transform[2, 2], best_guess]


def display_matches(im1, im2, points1, points2, inliers):
    """
    Dispalay matching points.
    :param im1: A grayscale image.
    :param im2: A grayscale image.
    :param points1: An aray shape (N,2), containing N rows of [x,y]
    coordinates of matched points in im1.
    :param points2: An aray shape (N,2), containing N rows of [x,y]
    coordinates of matched points in im2.
    :param inliers: An array with shape (S,) of inlier matches.
    """
    # don't know what it does, but the exercise says to combine images this way
    combined_images = np.hstack((im1, im2))
    # show the images
    plt.imshow(combined_images, cmap=plt.cm.gray)

    movement_im2_x = len(im1[0])  # how much to move the x points
    good_points = inliers
    # bad points = all points - good points
    bad_points = np.arange(len(points1))
    bad_points = np.delete(bad_points, good_points.astype(np.int))

    draw_points(bad_points, movement_im2_x, points1, points2, False)
    draw_points(good_points, movement_im2_x, points1, points2, True)
    plt.show()


def draw_points(indexes, movement_im2_x, points1, points2, is_inlier):
    x1, y1 = points1[indexes, X_INDEX], points1[indexes, Y_INDEX]
    x2, y2 = points2[indexes, X_INDEX], points2[indexes, Y_INDEX]
    x_lst = [x1, x2 + movement_im2_x]
    y_lst = [y1, y2]
    if is_inlier:
        plt.plot(x_lst, y_lst, mfc='r', c='y', lw=.3, ms=1, marker='o',
                 markeredgewidth=0.0)
    else:
        plt.plot(x_lst, y_lst, mfc='r', c='b', lw=.1, ms=1, marker='o',
                 markeredgewidth=0.0)


def accumulate_homographies(H_succesive, m):
    """
    Convert a list of succesive homographies to a
    list of homographies to a common reference frame.
    :param H_succesive: A list of M-1 3x3 homography
      matrices where H_successive[i] is a homography which transforms points
      from coordinate system i to coordinate system i+1.
    :param m: Index of the coordinate system towards which we would like to
      accumulate the given homographies.
    :return: A list of M 3x3 homography matrices,
      where H2m[i] transforms points from coordinate system i to coordinate
      system m
    """
    H2m = [np.eye(3)] * (len(H_succesive) + 1)
    H2m[m] = np.eye(3)
    for i in range(m, len(H_succesive)):
        H2m[i + 1] = H2m[i] @ np.linalg.inv(H_succesive[i])
        H2m[i + 1] /= H2m[i + 1][2, 2]  # the free variable should be 1
    for i in range(m - 1, -1, -1):
        H2m[i] = H2m[i + 1] @ H_succesive[i]
        H2m[i] /= H2m[i][2, 2]  # the free variable should be 1
    return H2m


def find_boundaries(arr):
    """
    :param arr: the points to calculate
    :return: the boundaries of the points as int
    """
    return [np.floor(np.min(arr)).astype(np.int), np.ceil(np.max(arr)).astype(np.int)]


def compute_bounding_box(homography, w, h):
    """
    computes bounding box of warped image under homography, without actually
    warping the image
    :param homography: homography
    :param w: width of the image
    :param h: height of the image
    :return: 2x2 array, where the first row is [x,y] of the top left corner,
     and the second row is the [x,y] of the bottom right corner
    """
    corners = np.array([[0, 0], [w, 0], [0, h], [w, h]])
    new_corners = apply_homography(corners, homography)

    min_x, max_x = find_boundaries(new_corners[:, X_INDEX])
    min_y, max_y = find_boundaries(new_corners[:, Y_INDEX])

    return np.array([[min_x, min_y], [max_x, max_y]]).astype(np.int)


def warp_channel(image, homography):
    """
    Warps a 2D image with a given homography.
    :param image: a 2D image.
    :param homography: homograhpy.
    :return: A 2d warped image.
    """
    h, w = image.shape
    [[min_x, min_y], [max_x, max_y]] = compute_bounding_box(homography, w, h)
    length_x, length_y = int(max_x - min_x + 1), int(max_y - min_y + 1)

    x, y = np.meshgrid(np.arange(min_x, max_x + 1), np.arange(min_y, max_y + 1))
    xy_coordinates = np.column_stack((x.T.reshape(-1), y.T.reshape(-1)))

    # calculate where each point is supposed to be in the original image
    inverse_wrap = apply_homography(xy_coordinates, np.linalg.inv(homography))
    # in map coordinates to calculate value y should be before x
    mapper = [inverse_wrap[:, Y_INDEX], inverse_wrap[:, X_INDEX]]
    apply_wrap = map_coordinates(image, mapper, order=1, prefilter=False)
    # convert the 1D coordinates back to image
    return apply_wrap.reshape((length_x, length_y)).T


def warp_image(image, homography):
    """
    Warps an RGB image with a given homography.
    :param image: an RGB image.
    :param homography: homograhpy.
    :return: A warped image.
    """
    return np.dstack(
        [warp_channel(image[..., channel], homography) for channel in
         range(3)])


def filter_homographies_with_translation(homographies,
                                         minimum_right_translation):
    """
    Filters rigid transformations encoded as homographies by the amount of
    translation from left to right.
    :param homographies: homograhpies to filter.
    :param minimum_right_translation: amount of translation below which the
     transformation is discarded.
    :return: filtered homographies..
    """
    translation_over_thresh = [0]
    last = homographies[0][0, -1]
    for i in range(1, len(homographies)):
        if homographies[i][0, -1] - last > minimum_right_translation:
            translation_over_thresh.append(i)
            last = homographies[i][0, -1]
    return np.array(translation_over_thresh).astype(np.int)


def estimate_rigid_transform(points1, points2, translation_only=False):
    """
    Computes rigid transforming points1 towards points2, using least squares
    method. points1[i,:] corresponds to poins2[i,:]. In every point,
    the first coordinate is *x*.
    :param points1: array with shape (N,
    2). Holds coordinates of corresponding points from image 1.
    :param points2: array with shape (N,2). Holds coordinates of corresponding
    points from image 2.
     :param translation_only: whether to compute translation only. False
     (default) to compute rotation as well.
     :return:  A 3x3 array with the computed homography.
    """
    centroid1 = points1.mean(axis=0)
    centroid2 = points2.mean(axis=0)

    if translation_only:
        rotation = np.eye(2)
        translation = centroid2 - centroid1

    else:
        centered_points1 = points1 - centroid1
        centered_points2 = points2 - centroid2

        sigma = centered_points2.T @ centered_points1
        U, _, Vt = np.linalg.svd(sigma)

        rotation = U @ Vt
        translation = -rotation @ centroid1 + centroid2

    H = np.eye(3)
    H[:2, :2] = rotation
    H[:2, 2] = translation
    return H


def non_maximum_suppression(image):
    """
    Finds local maximas of an image.
    :param image: A 2D array representing an image.
    :return: A boolean array with the same shape as the input image, where True
     indicates local maximum.
    """
    # Find local maximas.
    neighborhood = generate_binary_structure(2, 2)
    local_max = maximum_filter(image, footprint=neighborhood) == image
    local_max[image < (image.max() * 0.1)] = False

    # Erode areas to single points.
    lbs, num = label(local_max)
    centers = center_of_mass(local_max, lbs, np.arange(num) + 1)
    centers = np.stack(centers).round().astype(np.int)
    ret = np.zeros_like(image, dtype=np.bool)
    ret[centers[:, 0], centers[:, 1]] = True

    return ret


def spread_out_corners(im, m, n, radius):
    """
    Splits the image im to m by n rectangles and uses harris_corner_detector
    on each.
    :param im: A 2D array representing an image.
    :param m: Vertical number of rectangles.
    :param n: Horizontal number of rectangles.
    :param radius: Minimal distance of corner points from the
    boundary of the image.
    :return: An array with shape (N,2), where ret[i,:] are the [x,y]
    coordinates of the ith corner points.
    """
    corners = [np.empty((0, 2), dtype=np.int)]
    x_bound = np.linspace(0, im.shape[1], n + 1, dtype=np.int)
    y_bound = np.linspace(0, im.shape[0], m + 1, dtype=np.int)
    for i in range(n):
        for j in range(m):
            # Use Harris detector on every sub image.
            sub_im = im[y_bound[j]:y_bound[j + 1], x_bound[i]:x_bound[i + 1]]
            sub_corners = harris_corner_detector(sub_im)
            sub_corners += np.array([x_bound[i], y_bound[j]])[np.newaxis, :]
            corners.append(sub_corners)
    corners = np.vstack(corners)
    legit = ((corners[:, 0] > radius) & (
            corners[:, 0] < im.shape[1] - radius) &
             (corners[:, 1] > radius) & (corners[:, 1] < im.shape[0] - radius))
    ret = corners[legit, :]
    return ret


class PanoramicVideoGenerator:
    """
    Generates panorama from a set of images.
    """

    def __init__(self, data_dir, file_prefix, num_images):
        """
        The naming convention for a sequence of images is file_prefixN.jpg,
        where N is a running number 001, 002, 003...
        :param data_dir: path to input images.
        :param file_prefix: see above.
        :param num_images: number of images to produce the panoramas with.
        """
        self.file_prefix = file_prefix
        self.files = [
            os.path.join(data_dir, '%s%03d.jpg' % (file_prefix, i + 1)) for i
            in range(num_images)]
        self.files = list(filter(os.path.exists, self.files))
        self.panoramas = None
        self.homographies = None
        print('found %d images' % len(self.files))

    def align_images(self, translation_only=False):
        """
        compute homographies between all images to a common coordinate system
        :param translation_only: see estimte_rigid_transform
        """
        # Extract feature point locations and descriptors.
        points_and_descriptors = []
        for file in self.files:
            image = sol4_utils.read_image(file, 1)
            self.h, self.w = image.shape
            pyramid, _ = sol4_utils.build_gaussian_pyramid(image, 3, 7)
            points_and_descriptors.append(find_features(pyramid))
        # Compute homographies between successive pairs of images.
        Hs = []
        for i in range(len(points_and_descriptors) - 1):
            points1, points2 = points_and_descriptors[i][0], \
                               points_and_descriptors[i + 1][0]
            desc1, desc2 = points_and_descriptors[i][1], \
                           points_and_descriptors[i + 1][1]

            # Find matching feature points.
            ind1, ind2 = match_features(desc1, desc2, .7)
            points1, points2 = points1[ind1, :], points2[ind2, :]

            # Compute homography using RANSAC.
            H12, inliers = ransac_homography(points1, points2, 100, 6,
                                             translation_only)

            # Uncomment for debugging: display inliers and outliers among
            # matching points.
            # In the submitted code this function should be commented out!
            # display_matches(self.images[i], self.images[i+1], points1 ,
            # points2, inliers)

            Hs.append(H12)

        # Compute composite homographies from the central coordinate system.
        accumulated_homographies = accumulate_homographies(Hs,
                                                           (len(Hs) - 1) // 2)
        self.homographies = np.stack(accumulated_homographies)
        self.frames_for_panoramas = filter_homographies_with_translation(
            self.homographies, minimum_right_translation=5)
        self.homographies = self.homographies[self.frames_for_panoramas]

    def generate_panoramic_images(self, number_of_panoramas):
        """
        combine slices from input images to panoramas.
        :param number_of_panoramas: how many different slices to take from each
         input image
        """
        assert self.homographies is not None

        # compute bounding boxes of all warped input images in the
        # coordinate system of the middle image (as given by the homographies)
        self.bounding_boxes = np.zeros((self.frames_for_panoramas.size, 2, 2))
        for i in range(self.frames_for_panoramas.size):
            self.bounding_boxes[i] = compute_bounding_box(self.homographies[i],
                                                          self.w, self.h)

        # change our reference coordinate system to the panoramas
        # all panoramas share the same coordinate system
        global_offset = np.min(self.bounding_boxes, axis=(0, 1))
        self.bounding_boxes -= global_offset

        slice_centers = np.linspace(0, self.w, number_of_panoramas + 2,
                                    endpoint=True, dtype=np.int)[1:-1]
        warped_slice_centers = np.zeros(
            (number_of_panoramas, self.frames_for_panoramas.size))
        # every slice is a different panorama, it indicates the slices of
        # the input images from which the panorama will be concatenated
        for i in range(slice_centers.size):
            slice_center_2d = np.array([slice_centers[i], self.h // 2])[None,
                              :]
            # homography warps the slice center to the coordinate system of
            # the middle image
            warped_centers = [apply_homography(slice_center_2d, h) for h in
                              self.homographies]
            # we are actually only interested in the x coordinate of each
            # slice center in the panoramas' coordinate system
            warped_slice_centers[i] = np.array(warped_centers)[:, :, 0] \
                                          .squeeze() - global_offset[0]

        panorama_size = np.max(self.bounding_boxes, axis=(0, 1)).astype(
            np.int) + 1

        # boundary between input images in the panorama
        x_strip_boundary = ((warped_slice_centers[:,
                             :-1] + warped_slice_centers[:, 1:]) / 2)
        x_strip_boundary = np.hstack([np.zeros((number_of_panoramas, 1)),
                                      x_strip_boundary,
                                      np.ones((number_of_panoramas, 1)) *
                                      panorama_size[0]])
        x_strip_boundary = x_strip_boundary.round().astype(np.int)

        self.panoramas = np.zeros(
            (number_of_panoramas, panorama_size[1], panorama_size[0], 3),
            dtype=np.float64)
        for i, frame_index in enumerate(self.frames_for_panoramas):
            # warp every input image once, and populate all panoramas
            image = sol4_utils.read_image(self.files[frame_index], 2)
            warped_image = warp_image(image, self.homographies[i])
            x_offset, y_offset = self.bounding_boxes[i][0].astype(np.int)
            y_bottom = y_offset + warped_image.shape[0]

            for panorama_index in range(number_of_panoramas):
                # take strip of warped image and paste to current panorama
                boundaries = x_strip_boundary[panorama_index, i:i + 2]
                image_strip = warped_image[:,
                              boundaries[0] - x_offset: boundaries[1]
                                                        - x_offset]
                x_end = boundaries[0] + image_strip.shape[1]
                self.panoramas[panorama_index, y_offset:y_bottom,
                boundaries[0]:x_end] = image_strip

        # crop out areas not recorded from enough angles assert will fail if
        #  there is overlap in field of view between the left most image and
        #  the right most image
        crop_left = int(self.bounding_boxes[0][1, 0])
        crop_right = int(self.bounding_boxes[-1][0, 0])
        assert crop_left < crop_right, \
            'for testing your code with a few images do not crop.'
        print(crop_left, crop_right)
        self.panoramas = self.panoramas[:, :, crop_left:crop_right, :]

    def save_panoramas_to_video(self):
        assert self.panoramas is not None
        out_folder = 'tmp_folder_for_panoramic_frames/%s' % self.file_prefix
        try:
            shutil.rmtree(out_folder)
        except:
            print('could not remove folder')
            pass
        os.makedirs(out_folder)
        # save individual panorama images to 'tmp_folder_for_panoramic_frames'
        for i, panorama in enumerate(self.panoramas):
            imwrite('%s/panorama%02d.png' % (out_folder, i + 1), panorama)
        if os.path.exists('%s.mp4' % self.file_prefix):
            os.remove('%s.mp4' % self.file_prefix)
        # write output video to current folder
        os.system('ffmpeg -framerate 3 -i %s/panorama%%02d.png %s.mp4' %
                  (out_folder, self.file_prefix))

    def show_panorama(self, panorama_index, figsize=(20, 20)):
        assert self.panoramas is not None
        plt.figure(figsize=figsize)
        plt.imshow(self.panoramas[panorama_index].clip(0, 1))
        plt.show()





# def display_interest_points(im):
#     arr, descriptor = find_features(
#         sol4_utils.build_gaussian_pyramid(im, 3, 7)[0])
#     plt.figure()
#     plt.imshow(descriptor[-1], cmap="gray")
#     plt.show()
#
#     plt.figure()
#     plt.imshow(im, cmap="gray")
#     plt.plot(arr[0], arr[1], mfc='r', c='b', lw=.4, ms=3, marker='o')
#     plt.show()
#
#     return arr, descriptor
#
#
# if __name__ == "__main__":
#     image1 = sol4_utils.read_image("externals\\oxford1.jpg", 1)
#     image2 = sol4_utils.read_image("externals\\oxford2.jpg", 1)
#     c1, d1 = display_interest_points(image1)
#     c2, d2 = display_interest_points(image2)
#     a, b = match_features(d1, d2, 0.8)
#     H, inliers = ransac_homography(c1[a, :], c2[b, :], 50, 10, False)
#     display_matches(image1, image2, c1[a, :], c2[b, :], inliers)
#     plt.figure()
#     plt.imshow(image1, cmap="gray")
#     plt.imshow(warp_channel(image1, H), cmap="gray")
#     plt.show()
