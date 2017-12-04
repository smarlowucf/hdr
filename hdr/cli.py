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
@click.argument('images', nargs=-1)
def create(no_color, images):
    """
    Create HDR image from a set of images.

    Examples:
        hdr create image1.jpg image2.jpg image3.jpg

    :param images: List of images to merge into HDR.
    :param no_color: If True do not style string output.
    """
    try:
        response = api.create_hdr(images)
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        utils.echo_style(response, no_color)


main.add_command(create)
