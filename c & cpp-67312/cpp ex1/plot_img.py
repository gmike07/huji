#! /usr/bin/env python3

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

IMG_EDGE = 28
IMG_LEN = IMG_EDGE * IMG_EDGE


def main(argv):
    if len(argv) != 2:
        print("Usage: ./plot_img.py <image_file>")
        return

    im_path = argv[1]
    if not os.path.exists(im_path):
        print("Error: invalid path given: ", im_path)
        return

    img = np.fromfile(im_path, dtype=np.float32)
    if img.size != IMG_LEN:
        print("Unknown img file len")
    
    plt.imshow(img.reshape(IMG_EDGE, IMG_EDGE),cmap='gray')
    plt.show()


if __name__ == "__main__":
    main(sys.argv)
