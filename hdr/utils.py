# -*- coding: utf-8 -*-
#
# hdr: A Python API and CLI to create hdr images.
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


def echo_style(message, no_color, fg='yellow'):
    """
    Echo string with style if no_color is False.

    :param message: String to echo.
    :param no_color: If True echo without style.
    :param fg: String style color.
    """
    if no_color:
        click.echo(message)
    else:
        click.secho(message, fg=fg)


def style_string(message, no_color, fg='yellow'):
    """
    Add color style to string if no_color is False.

    :param message: String to style.
    :param no_color: If True return string without style.
    :param fg: The color for the string style.
    :return: Return string conditionally style.
    """
    if no_color:
        return message
    else:
        return click.style(message, fg=fg)
