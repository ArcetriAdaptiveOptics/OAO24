import numpy as np


class BaseMask():
    '''
    '''

    def __init__(self, mask_array):
        self._shape = mask_array.shape
        self._mask = mask_array

    def mask(self):
        '''
        Boolean mask of the mask

        Returns
        -------
        mask: boolean `~numpy.array`
            mask of the pupil. Array is True outside the pupil,
            and False inside the pupil
        '''
        return self._mask

    def as_masked_array(self):
        return np.ma.array(np.ones(self._shape),
                           mask=self.mask())

    def shape(self):
        '''
        Array shape

        Returns
        -------
        shape: list (2,)
            shape of the mask array
        '''
        return self._shape

    @staticmethod
    def from_masked_array(numpy_masked_array):
        return BaseMask(numpy_masked_array)

    def __eq__(self, other):
        if isinstance(other, BaseMask):
            return np.array_equal(self.mask(), other.mask())
        return False

    def __hash__(self):
        return hash(self.mask().tobytes())

    # TODO: funzione per verificare che tutti i punti di questa maschera stanno
    # dentro una maschera passata


class CircularMask(BaseMask):
    '''
    Represent a circular mask

    A `~numpy.array` representing a circular pupil. Frame shape, pupil radius
    and center can be specified.

    Use `mask` method to access the mask as boolean mask (e.g. to be used
    in a `~numpy.ma.masked_array` object) with False values where the frame is 
    not masked (i.e. within the pupil) and True values outside

    Use `asTransmissionValue` method to acces the mask as transmission mask, i.e. 
    1 within the pupil and 0 outside. Fractional transmission for edge pixels
    is not implemented

    If a `~numpy.ma.masked_array` having a circular mask is available, the static
    method `fromMaskedArray` can be used to create a `CircularMask` object having
    the same shape of the masked array and the same pupil center and radius


    Parameters
    ----------
        frameShape: tuple (2,)
            shape of the returned array

        maskRadius: real
            pupil radius in pixel

        maskCenter: list (2,) or `~numpy.array`
            Y-X coordinates of the pupil center in pixel
    '''

    def __init__(self,
                 frameShape,
                 maskRadius=None,
                 maskCenter=None):
        self._shape = frameShape
        self._maskRadius = maskRadius
        self._maskCenter = maskCenter
        self._mask = None
        self._computeMask()

    def __repr__(self):
        return "shape %s, radius %f, center %s" % (
            self._shape, self._maskRadius, self._maskCenter)

    def _computeMask(self):
        if self._maskRadius is None:
            self._maskRadius = min(self._shape) / 2.
        if self._maskCenter is None:
            self._maskCenter = 0.5 * np.array([self._shape[0],
                                               self._shape[1]])

        r = self._maskRadius
        cc = self._maskCenter
        y, x = np.mgrid[0.5: self._shape[0] + 0.5:1,
                        0.5: self._shape[1] + 0.5:1]
        self._mask = np.where(
            ((x - cc[1]) ** 2 + (y - cc[0]) ** 2) <= r ** 2, False, True)

    def asTransmissionValue(self):
        '''
        Mask as a transmission mask: 1 for non-masked elements,
        0 for masked elements.

        Returns
        -------
        transmission_value: ndarray[int]
            transmission mask as a numpy array with dtype int
        '''
        return np.logical_not(self._mask).astype(int)

    # def as_masked_array(self):
    #    return np.ma.array(np.array(self.asTransmissionValue(), dtype=float),
    #                       mask=self.mask())

    def radius(self):
        '''
        Radius of the mask 

        Returns
        -------
        radius: real
            mask radius in pixel

        '''
        return self._maskRadius

    def center(self):
        '''
        Y, X coordinates of the mask center

        Returns
        -------
        center: `~numpy.array` of shape (2,)
            Y, X coordinate of the mask center in the array reference system

        '''
        return self._maskCenter

    def in_mask_indices(self):
        return self.asTransmissionValue().flatten().nonzero()[0]


class AnnularMask(CircularMask):
    '''
    Inheritance of CircularMask class to provide an annular mask

    Added inRadius parameter, radius of central obstruction.
    Default inRadius values is 0 with AnnularMask converging to CircularMask
    '''

    def __init__(self,
                 frameShape,
                 maskRadius=None,
                 maskCenter=None,
                 inRadius=0):
        self._inRadius = inRadius
        super().__init__(frameShape, maskRadius, maskCenter)

    def __repr__(self):
        return "shape %s, radius %f, center %s, inradius %f" % (
            self._shape, self._maskRadius, self._maskCenter, self._inRadius)

    def inRadius(self):
        return self._inRadius

    def _computeMask(self):

        if self._maskRadius is None:
            self._maskRadius = min(self._shape) / 2.
        if self._maskCenter is None:
            self._maskCenter = 0.5 * np.array([self._shape[0],
                                               self._shape[1]])

        r = self._maskRadius
        cc = self._maskCenter
        y, x = np.mgrid[0.5: self._shape[0] + 0.5:1,
                        0.5: self._shape[1] + 0.5:1]

        tmp = ((x - cc[1]) ** 2 + (y - cc[0]) ** 2) <= r ** 2
        if self._inRadius == 0:
            self._mask = np.where(tmp, False, True)
        else:
            cc = CircularMask(self._shape, self._inRadius, self._maskCenter)
            tmp[cc.asTransmissionValue() > 0] = False
            self._mask = np.where(tmp, False, True)
