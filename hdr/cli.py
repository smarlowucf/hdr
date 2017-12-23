# -*- coding: utf-8 -*-
#
# hdr: A Python API and CLI for HDR images.
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

import click

from hdr import api
from hdr import utils


def print_license(ctx, param, value):
    """
    Eager option to print license information and exit.
    """
    if not value or ctx.resilient_parsing:
        return

    click.echo(
        'hdr Copyright (C) 2017 sean Marlow. (GPL-3.0+)\n\n'
        'This program comes with ABSOLUTELY NO WARRANTY.\n'
        'This is free software, and you are welcome to redistribute it'
        ' under certain conditions. See LICENSE for more information.'
    )
    ctx.exit()


@click.group()
@click.version_option()
@click.option(
    '--license',
    expose_value=False,
    is_eager=True,
    is_flag=True,
    callback=print_license,
    help='Display license information and exit.'
)
def main():
    """
    Create HDR images in your terminal.

    Leverages OpenCV.
    """
    pass


@click.command()
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.option(
    '-a',
    '--algorithm',
    default='debevec',
    type=click.choice(['debevec', 'robertson']),
    help='The HDR algorithm to use for merging images.'
)
@click.option(
    '-e',
    '--exposures',
    help='Comma separated list of image exposure times.'
)
@click.option(
    '-g',
    '--gamma',
    default=2.2,
    help='Positive gamma value to use in tonemap. Gamma value of 1.0 implies '
         'no correction, gamma equal to 2.2 is suitable for most displays.'
         ' Generally gamma > 1 brightens the image and gamma < 1 darkens it.'
)
@click.option(
    '-s',
    '--saturation',
    default=1.0,
    help='Positive aturation value to use in tonemap. Value of 1.0 preserves '
         'saturation, values greater than 1 increase saturation and '
         'values less than 1 decrease it.'
)
@click.option(
    '-b',
    '--bias',
    default=0.85,
    help='Value for bias function in [0, 1] range. Values from 0.7 to '
         '0.9 usually give best results, default value is 0.85.'
)
@click.option(
    '-o',
    '--output',
    help='Filename for HDR jpeg output.'
)
@click.argument('images', nargs=-1)
def drago(
    no_color, algorithm, exposures, gamma, saturation, bias, output, images
):
    """
    Create HDR image from a set of images using drago tonemap.

    Adaptive logarithmic mapping is a fast global tonemapping
    algorithm that scales the image in logarithmic domain.

    Since it’s a global operator the same function is applied to
    all the pixels, it is controlled by the bias parameter.

    Example:
        hdr drago image1.jpg image2.jpg image3.jpg
    """
    try:
        response = api.drago_hdr(
            images, algorithm, exposures, gamma, saturation, bias, output
        )
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        utils.echo_style(response, no_color)


@click.command()
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.option(
    '-a',
    '--algorithm',
    default='debevec',
    type=click.choice(['debevec', 'robertson']),
    help='The HDR algorithm to use for merging images.'
)
@click.option(
    '-e',
    '--exposures',
    help='Comma separated list of image exposure times.'
)
@click.option(
    '-g',
    '--gamma',
    default=2.2,
    help='Positive gamma value to use in tonemap. Gamma value of 1.0 implies '
         'no correction, gamma equal to 2.2 is suitable for most displays.'
         ' Generally gamma > 1 brightens the image and gamma < 1 darkens it.'
)
@click.option(
    '-c',
    '--contrast',
    default=4.0,
    help='Maximum and minimum luminance values of the resulting image.'
)
@click.option(
    '-s',
    '--saturation',
    default=1.0,
    help='Positive aturation value to use in tonemap. Value of 1.0 preserves '
         'saturation, values greater than 1 increase saturation and '
         'values less than 1 decrease it.'
)
@click.option(
    '--sigma-space',
    default=2.0,
    help='Bilateral filter sigma in color space.'
)
@click.option(
    '--sigma-color',
    default=2.0,
    help='Bilateral filter sigma in coordinate space.'
)
@click.option(
    '-o',
    '--output',
    help='Filename for HDR jpeg output.'
)
@click.argument('images', nargs=-1)
def durand(
    no_color, algorithm, exposures, gamma, contrast, saturation,
    sigma_space, sigma_color, output, images
):
    """
    Create HDR image from a set of images using durand tonemap.

    This algorithm decomposes image into two layers: base layer
    and detail layer using bilateral filter and compresses contrast
    of the base layer thus preserving all the details.

    Examples:
        hdr durand image1.jpg image2.jpg image3.jpg
    """
    try:
        response = api.durand_hdr(
            images, algorithm, exposures, gamma, contrast, saturation,
            sigma_space, sigma_color, output
        )
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        utils.echo_style(response, no_color)


@click.command()
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.option(
    '-a',
    '--algorithm',
    default='debevec',
    type=click.choice(['debevec', 'robertson']),
    help='The HDR algorithm to use for merging images.'
)
@click.option(
    '-e',
    '--exposures',
    help='Comma separated list of image exposure times.'
)
@click.option(
    '-g',
    '--gamma',
    default=2.2,
    help='Positive gamma value to use in tonemap. Gamma value of 1.0 implies '
         'no correction, gamma equal to 2.2 is suitable for most displays.'
         ' Generally gamma > 1 brightens the image and gamma < 1 darkens it.'
)
@click.option(
    '--scale',
    default=0.7,
    help='Contrast scale factor. HVS response is multiplied by this '
         'parameter, thus compressing dynamic range. Values from 0.6 '
         'to 0.9 produce best results.'
)
@click.option(
    '-s',
    '--saturation',
    default=1.0,
    help='Positive aturation value to use in tonemap. Value of 1.0 preserves '
         'saturation, values greater than 1 increase saturation and '
         'values less than 1 decrease it.'
)
@click.option(
    '-o',
    '--output',
    help='Filename for HDR jpeg output.'
)
@click.argument('images', nargs=-1)
def mantiuk(
    no_color, algorithm, exposures, gamma, scale, saturation, output, images
):
    """
    Create HDR image from a set of images using mantiuk tonemap.

    This algorithm transforms image to contrast using gradients on all
    levels of gaussian pyramid, transforms contrast values to HVS response
    and scales the response. After this the image is reconstructed from
    new contrast values.

    Examples:
        hdr mantiuk image1.jpg image2.jpg image3.jpg
    """
    try:
        response = api.mantiuk_hdr(
            images, algorithm, exposures, gamma, scale, saturation, output
        )
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        utils.echo_style(response, no_color)


@click.command()
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.option(
    '-c',
    '--contrast',
    default=1.0,
    help='Contrast measure weight.'
)
@click.option(
    '-e',
    '--exposure',
    default=0.0,
    help='Well-exposedness measure weight.'
)
@click.option(
    '-g',
    '--gamma',
    default=2.2,
    help='Positive gamma value to use in tonemap. Gamma value of 1.0 implies '
         'no correction, gamma equal to 2.2 is suitable for most displays.'
         ' Generally gamma > 1 brightens the image and gamma < 1 darkens it.'
)
@click.option(
    '-s',
    '--saturation',
    default=1.0,
    help='Saturation measure weight.'
)
@click.option(
    '-o',
    '--output',
    help='Filename for HDR jpeg output.'
)
@click.argument('images', nargs=-1)
def mertens(
    no_color, contrast, exposure, gamma, saturation, output, images
):
    """
    Create HDR image from a set of images using mertens algorithm.

    Pixels are weighted using contrast, saturation and well-exposedness
    measures, than images are combined using laplacian pyramids.

    The resulting image weight is constructed as weighted average of contrast,
    saturation and well-exposedness measures.

    The resulting image doesn’t require tonemapping and can be converted to
    8-bit image by multiplying by 255, but it’s recommended to apply gamma
    correction and/or linear tonemapping.

    Examples:
        hdr mertens image1.jpg image2.jpg image3.jpg
    """
    try:
        response = api.mertens_hdr(
            images, contrast, exposure, gamma, saturation, output
        )
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        utils.echo_style(response, no_color)


@click.command()
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.option(
    '-a',
    '--algorithm',
    default='debevec',
    type=click.choice(['debevec', 'robertson']),
    help='The HDR algorithm to use for merging images.'
)
@click.option(
    '-e',
    '--exposures',
    help='Comma separated list of image exposure times.'
)
@click.option(
    '-g',
    '--gamma',
    default=2.2,
    help='Positive gamma value to use in tonemap. Gamma value of 1.0 implies '
         'no correction, gamma equal to 2.2 is suitable for most displays.'
         ' Generally gamma > 1 brightens the image and gamma < 1 darkens it.'
)
@click.option(
    '-l',
    '--light-adapt',
    default=1.0,
    help='Light adaptation in [0, 1] range. If 1 adaptation is based only'
         ' on pixel value, if 0 it’s global, otherwise it’s a weighted mean '
         'of this two cases.'
)
@click.option(
    '-c',
    '--color-adapt',
    default=0.0,
    help='chromatic adaptation in [0, 1] range. If 1 channels are treated '
         'independently, if 0 adaptation level is the same for each channel.'
)
@click.option(
    '-o',
    '--output',
    help='Filename for HDR jpeg output.'
)
@click.argument('images', nargs=-1)
def reinhard(
    no_color, algorithm, exposures, gamma, intensity,
    light_adapt, color_adapt, output, images
):
    """
    Create HDR image from a set of images using reinhard tonemap.

    This is a global tonemapping operator that models human visual system.

    Mapping function is controlled by adaptation parameter, that is
    computed using light adaptation and color adaptation.

    Examples:
        hdr reinhard image1.jpg image2.jpg image3.jpg
    """
    try:
        response = api.reinhard_hdr(
            images, algorithm, exposures, gamma, intensity,
            light_adapt, color_adapt, output
        )
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        utils.echo_style(response, no_color)


main.add_command(drago)
main.add_command(durand)
main.add_command(mantiuk)
main.add_command(mertens)
main.add_command(reinhard)
