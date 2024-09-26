import numpy as np
import matplotlib.pyplot as plt
from oao24 import package_data


def make_master_image(raw_data_cube, background_image, want_display=False):
    ''' 
    Compute the master image from a raw cube data and the background image.
    
    1. Dark image is subtracted to each image of the raw cube
    2. Cube is cumulated (without shift and add)
    
    Dark_image must have the same camera setting
    (i.e. exposure and filter) of each image of the raw cube
    '''

    Nframes = raw_data_cube.shape[-1]

    # create the background master
    master_background = np.median(np.atleast_3d(background_image), axis=-1)

    # subtracting background from raw data
    # make sure new array is float !!! to avoid integer overflows
    background_subtracted_data_cube = np.zeros(
        raw_data_cube.shape, dtype=float)
    for frame in np.arange(Nframes):
        background_subtracted_data_cube[:, :,
                                        frame] = raw_data_cube[:, :, frame] - master_background

    # Computing master image
    # Sum along the NDIT dimension to obtain a single (512,640) image
    # Must know total integration time
    #
    # Advanced: shift & add. Detects every image's maximum and shift
    # every image before stacking to eliminate residual tip-tilt
    ###########
    master_image = background_subtracted_data_cube.sum(axis=-1)
    print_roi_mean_values(master_image, label='Master image')

    if want_display:
        plt.figure()
        plt.imshow(master_background, vmin=0, vmax=2000)
        plt.colorbar(label='ADU')
        plt.title("Background image")
        print_roi_mean_values(master_background, label='Background')

        # display one frame of the raw data cube
        plt.figure()
        plt.imshow(raw_data_cube[:, :, 0], vmin=0, vmax=2000)
        plt.colorbar(label='ADU')
        plt.title("Raw data image #0")
        print_roi_mean_values(raw_data_cube[:, :, 0], label='Raw image #0')

        plt.figure()
        plt.imshow(master_image, vmin=-10, vmax=100)
        plt.title('Master image (linear scale, clipped)')
        plt.colorbar()

    #########
    # Display image log scale
    # Dark area should be around 0
    ######
    plt.figure()
    arr = master_image
    plt.imshow(np.log10(np.clip(arr, 0, None)+1), cmap='inferno')
    plt.title('Master image (log scale)')
    plt.colorbar()

    return master_image


def print_roi_mean_values(image, label=''):
    '''
    Print mean values of 4 Region Of Interest in the corners 
    of the image.
    Return average value in the ROIs
    We use it as background value indicator
    '''
    bkg_roi1 = image[50:100, 50:100].mean()
    bkg_roi2 = image[50:100, -100:-50].mean()
    bkg_roi3 = image[-100:-50, 50:100].mean()
    bkg_roi4 = image[-100:-50, -100:-50].mean()
    bkg = np.mean([bkg_roi1, bkg_roi2, bkg_roi3, bkg_roi4])
    print("%s : ROIs mean values %g %g %g %g - Average %g ADU" %
          (label, bkg_roi1, bkg_roi2, bkg_roi3, bkg_roi4, bkg))
    return bkg
