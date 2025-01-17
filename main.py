#!/usr/bin/env python3

import os

import click
import cv2

from helpers import Helpers

helpers = Helpers()

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)
@click.option(
    "-s",
    "--source",
    type=click.Path(exists=True),
    required=True,
    help="Source image path.",
)
@click.option(
    "-d",
    "--destination",
    type=click.Path(),
    help="Destination image path. Default is <source>_obfuscated.<ext>",
)
@click.option(
    "-f",
    "--force",
    help="Overwrite the destination file if it exists.",
    is_flag=True,
    default=False,
)
def obfuscate_plate(source: str, destination: str | None, force: bool) -> None:
    """Obfuscate the number plate in the given image."""

    if not destination:
        fileparts = os.path.splitext(source)
        destination = fileparts[0] + "_obfuscated" + fileparts[1]

    # if not destination.startswith('/'):
    #     destination = os.path.abspath(destination)
    #     print(destination)

    # Open image
    imageCv = helpers.openImageCv(source)

    # Pre-processing
    gray = helpers.cvToGrayScale(imageCv)
    bilateral = helpers.cvApplyBilateralFilter(gray)

    # Detect edge contours
    edged = helpers.cvToCannyEdge(bilateral)

    # Dilate the contours to allow for unclosed contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    dilated = cv2.dilate(edged, kernel)

    # Find all contours
    contours = helpers.cvExtractContours(dilated)

    # Narrow down to rectangular contours
    rectangleContours = helpers.cvFilterRectangleContours(contours)

    # Pick first/largest rectangle as plate
    # NOTE: This is just picking the largest contour blindly, so it's open to failure if there are large road signs or anything like that.
    plateContour = helpers.cvResizeContour(rectangleContours[0], 1.0)

    # Crop down to the plate
    plateImage = helpers.cvCropByContour(imageCv, plateContour)

    # Find the plate's background color
    plateBackgroundColor = helpers.cvFindMostOccurringColor(plateImage)

    # For debug, enable this instead of the `result` variable below.
    # Draws all found rectangles in white on a black background.
    # import numpy
    # image = numpy.zeros(imageCv.shape, dtype=numpy.uint8)

    # result = cv2.drawContours(
    #     image, rectangleContours, -1, (255,255,255), -1
    # )

    # Draw over the plate
    result = cv2.drawContours(
        imageCv.copy(), [plateContour], -1, plateBackgroundColor, -1
    )

    # Save the result
    if os.path.exists(destination) and not force:
        click.echo(f"File already exists: {destination}")
        return

    cv2.imwrite(destination, result)
    click.echo(f"Obfuscated image saved as: {destination}")


if __name__ == "__main__":
    obfuscate_plate()
