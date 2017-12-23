# -*- coding: utf-8 -*-
#
# hdr: A Python API and CLI for creating HDR images.
#
# Copyright (C) 2017 Sean Marlow
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cv2
import PIL.Image

from numpy import array, float32

from hdr.exceptions import HdrException


def align_images(images):
    align_mtb = cv2.createAlignMTB()
    align_mtb.process(images, images)


def drago_hdr(image_names,
              algo='debevec',
              exposures=None,
              gamma=1.0,
              saturation=1.0,
              bias=0.85,
              output=None):
    """
    Create an HDR image from the supplied images.

    :param images: List of images to process.
    :return: Returns name of new HDR image.
    """
    hdr_img = process_image(image_names, exposures, algo)

    tonemap_drago = cv2.createTonemapDrago(gamma, saturation, bias)
    ldr_drago = tonemap_drago.process(hdr_img)

    img_out = get_image_output(image_names[1], output)
    cv2.imwrite(img_out, ldr_drago * 255)


def durand_hdr(image_names,
               algo='debevec',
               exposures=None,
               gamma=1.0,
               contrast=4.0,
               saturation=1.0,
               sigma_space=2.0,
               sigma_color=2.0,
               output=None):
    """
    Create an HDR image from the supplied images.

    :param images: List of images to process.
    :return: Returns name of new HDR image.
    """
    hdr_img = process_image(image_names, exposures, algo)

    tonemap_durand = cv2.createTonemapDurand(
        gamma, contrast, saturation, sigma_space, sigma_color
    )
    ldr_durand = tonemap_durand.process(hdr_img)

    img_out = get_image_output(image_names[1], output)
    cv2.imwrite(img_out, ldr_durand * 255)


def mantiuk_hdr(image_names,
                algo='debevec',
                exposures=None,
                gamma=2.2,
                scale=0.7,
                saturation=1.0,
                output=None):
    """
    Create an HDR image from the supplied images.

    :param images: List of images to process.
    :return: Returns name of new HDR image.
    """
    hdr_img = process_image(image_names, exposures, algo)

    tonemap_mantiuk = cv2.createTonemapMantiuk(gamma, scale, saturation)
    ldr_mantiuk = tonemap_mantiuk.process(hdr_img)

    img_out = get_image_output(image_names[1], output)
    cv2.imwrite(img_out, ldr_mantiuk * 255)


def mertens_hdr(image_names,
                contrast=1.0,
                exposure=0.0,
                gamma=2.2,
                saturation=1.0,
                output=None):
    """
    Create an HDR image from the supplied images.

    :param images: List of images to process.
    :return: Returns name of new HDR image.
    """
    images = read_images(image_names)
    align_images(images)
    mertens_img = process_mertens(images, contrast, saturation, exposure)

    tonemap = cv2.createTonemap(gamma)
    ldr_mertens = tonemap.process(mertens_img)

    img_out = get_image_output(image_names[1], output)
    cv2.imwrite(img_out, ldr_mertens * 255)


def reinhard_hdr(image_names,
                 algo='debevec',
                 exposures=None,
                 gamma=1.0,
                 intensity=0.0,
                 light_adapt=1.0,
                 color_adapt=0.0,
                 output=None):
    """
    Create an HDR image from the supplied images.

    :param images: List of images to process.
    :return: Returns name of new HDR image.
    """
    hdr_img = process_image(image_names, exposures, algo)

    tonemap_reinhard = cv2.createTonemapReinhard(
        gamma, intensity, light_adapt, color_adapt
    )
    ldr_reinhard = tonemap_reinhard.process(hdr_img)

    img_out = get_image_output(image_names[1], output)
    cv2.imwrite(img_out, ldr_reinhard * 255)


def get_image_output(image, output):
    if output:
        return output
    else:
        return image.replace('.', '_hdr.')


def get_exposure(image):
    img = PIL.Image.open(image)
    exposure = img._getexif()[33434]
    return exposure[0] / exposure[1]


def get_exposures(exposures, image_names):
    if exposures:
        try:
            exposures = exposures.split(',')
        except Exception:
            raise HdrException('Exposures must be a comma separated list.')
    else:
        exposures = [get_exposure(image) for image in image_names]

    return array(exposures, dtype=float32)


def process_image(image_names, exposures, algo):
    images = read_images(image_names)
    exposures = get_exposures(exposures, image_names)
    align_images(images)

    if algo == 'debevec':
        hdr_img = process_debevec(images, exposures)
    elif algo == 'robertson':
        hdr_img = process_robertson(images, exposures)
    else:
        raise HdrException('The {0} algorithm is not supported.'.format(algo))

    return hdr_img


def process_debevec(images, exposures):
    calibrate_debevec = cv2.createCalibrateDebevec()
    response_debevec = calibrateDebevec.process(images, times=exposures)

    merge_debevec = cv2.createMergeDebevec()
    return merge_debevec.process(
        images,
        times=exposures,
        response=response_debevec
    )


def process_mertens(images, contrast, saturation, exposure):
    merge_mertens = cv2.createMergeMertens(contrast, saturation, exposure)
    return merge_mertens.process(images)


def process_roberston(images, exposures):
    calibrate_robertson = cv2.createCalibrateRobertson()
    response_robertson = calibrateRobertson.process(images, times=exposures)

    merge_robertson = cv2.createMergeRoberston()
    return merge_robertson.process(
        images,
        times=exposures,
        response=response_robertson
    )


def read_images(image_names):
    images = []
    for image_name in image_names:
        image = cv2.imread(image_name)
        images.append(image)
    return images


def write_image(image, name):
    cv2.imwrite(name, image)
